from datetime import datetime
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, login_required, logout_user, current_user

from main_project import app, db
from main_project.models import User, Quiz, UserAnswer
from main_project.forms import *

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=["GET", "POST"])
def login():

    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user.validate_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login flask saves that URL as 'next'.
            next = request.args.get('next')

            # Check if 'next' exists, otherwise go to the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('home')

            return redirect(next)
        
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/quiz/<block>', methods=["GET", "POST"])
@login_required
def quiz(block):
    url_block = {
         "novice": "новачок", "advanced_beginner": "твердий початківець", "competent": "компетентний",
         "proficient": "досвідчений", "expert": "експерт"
    }
    blocks_forms = {"новачок": NoviceForm(), "твердий початківець": AdvancedBeginnerForm(),
                   "компетентний": CompetentForm(), "досвідчений": ProficientForm(),
                   "експерт": ExpertForm()}
    blocks = list(url_block.keys())

    block_ukr = url_block[block]
    form = blocks_forms[block_ukr]
    if form.validate_on_submit():
        if block_ukr != "новачок":
            # Get last quiz
            quiz = Quiz.query.all()[-1]

            q1_answer = UserAnswer(quiz_id=quiz.id, block_name=block, question_no=1, answer_score=form.q1_choice.data)
            q2_answer = UserAnswer(quiz_id=quiz.id, block_name=block, question_no=2, answer_score=form.q2_choice.data)
            q3_answer = UserAnswer(quiz_id=quiz.id, block_name=block, question_no=3, answer_score=form.q3_choice.data)
            db.session.add_all([q1_answer, q2_answer, q3_answer])
            db.session.commit()
        else:
            # if there is no prev buttons
            # Create a quiz table record
            quiz = Quiz(user_id=current_user.id, datetime=datetime.now())
            db.session.add(quiz)
            db.session.commit()

            q1_answer = UserAnswer(quiz_id=quiz.id, block_name='novice', question_no=1, answer_score=form.q1_choice.data)
            q2_answer = UserAnswer(quiz_id=quiz.id, block_name='novice', question_no=2, answer_score=form.q2_choice.data)
            q3_answer = UserAnswer(quiz_id=quiz.id, block_name='novice', question_no=3, answer_score=form.q3_choice.data)
            q4_answer = UserAnswer(quiz_id=quiz.id, block_name='novice', question_no=4, answer_score=form.q4_choice.data)
            db.session.add_all([q1_answer, q2_answer, q3_answer, q4_answer])
            db.session.commit()

        if block_ukr != "експерт":
            current_index = blocks.index(block)
            next_block = blocks[current_index + 1]
            return redirect(url_for('quiz', block=next_block))
        return redirect(url_for('quiz_results'))
    return render_template('quiz.html', form=form, block=block_ukr)


@app.route('/quiz_results', methods=["GET", "POST"])
@login_required
def quiz_results():
    current_quiz = Quiz.query.all()[-1]
    quiz_answers = UserAnswer.query.filter_by(quiz_id=current_quiz.id).all()
    url_block = {
         "novice": "новачок", "advanced_beginner": "твердий початківець", "competent": "компетентний",
         "proficient": "досвідчений", "expert": "експерт"
    }
    quiz_answers_block = {}
    general_score = 0
    programmer_level = { 
        'level': 'Новачок', 
        'description': 'Новачок (Novice). Новачки дуже переживають за свою успішність; їх досвіду замало, щоб повести їх у правильному напрямку і вони не знають чи їх вчинки будуть правильними. Новачки зазвичай не хочуть вчитися, зате хочуть досягти миттєвого результату. Вони не знають як реагувати на помилки і тому легко збиваються з пантелику, коли щось іде “не так”. Зате вони можуть бути досить ефективними, коли їм дати набір контекстно незалежних правил у формі “у випадку ХХХ, роби УУУ”. Іншими словами їм необхідний рецепт або алгоритм.'
    }
    for answer in quiz_answers:
        block_name = url_block[answer.block_name]
        if block_name not in quiz_answers_block:
            quiz_answers_block[block_name] = {'question_nos': [], 'answer_scores': []}
        general_score += answer.answer_score
        quiz_answers_block[block_name]['question_nos'].append(answer.question_no)
        quiz_answers_block[block_name]['answer_scores'].append(answer.answer_score)
    quiz_block_score = {'block_names': list(quiz_answers_block.keys()), 'block_scores': []}
    for block_name in quiz_block_score['block_names']:
        quiz_block_score['block_scores'].append(sum(quiz_answers_block[block_name]['answer_scores']))  

    if (general_score > 16) and (general_score <= 32):
        programmer_level['level'] = 'Твердий початківець'
        programmer_level['description'] = 'Тверді початківці починають вже потроху відступати від фіксованих правил. Вони можуть спробувати якісь задачі самостійно, але у них все ще є труднощі із усуненням проблем, які виникають. Початківці можуть скористатись порадами в правильному контексті, врахувавши свій досвід подібних ситуацій, але ледь-ледь. І хоч вони вже починають формулювати якісь загальні принципи, вони все ще не бачать “всієї картини”. Якщо спробувати надати їм ширший контекст – вони відмахнуться від нього як від недоречного.'
    
    elif (general_score > 32) and (general_score <= 48):
        programmer_level['level'] = 'Компетентний'
        programmer_level['description'] = 'Компетентні будують правильні моделі проблемної області та ефективно нею користуються. Здатні усувати проблеми з якими раніше не стикались. Про людей на цьому рівні часто кажуть, що вони “мають ініціативу”. Вони можуть вчити новачків і не задовбують експертів. Щоправда їм ще бракує досвіду аби вдало розставити пріоритети при рішенні задач. Власне кажучи, саме з цього рівня людину можна вже назвати інженером – компетентні вирішують задачі, а не працюють за алгоритмом.'
    
    elif (general_score > 48) and (general_score <= 64):
        programmer_level['level'] = 'Досвідчений'
        programmer_level['description'] = 'Досвідченим необхідна “повна картина” проблемної області, адже вони хочуть розуміти весь концепт. Вони роблять значний прорив в рамках моделі братів Дрейфус, адже постійно оцінюють виконану роботу і переглядають свої підходи, аби наступного разу бути ще ефективнішими. Вони також можуть навчатись використовуючи чужий досвід. І найголовніше – вони завжди беруть до уваги контекст задачі. Якщо повернутись до програмування, то чудовий приклад ілюстрації – це використання патернів проектування. Лише досвідчені використовують їх виключно там де треба, а не бездумно і повсюдно, бо це круто і модно.'
    
    elif (general_score > 64) and (general_score <= 80):
        programmer_level['level'] = 'Експерт'
        programmer_level['description'] = 'Експерти – основне джерело знань та інформації в будь-якій сфері. Вони безперестану шукають все кращі і кращі методи роботи. Вони завжди застосовують весь свій велетенський багаж знань у правильному контексті. Вони пишуть книжки, статті та проводять семінари. Це сучасні чаклуни. Експерти керуються інтуїцією . Доктор Хаус, який з одного погляду на пацієнта (або взагалі на його медичну картку) міг поставити діагноз – типовий приклад експерта. Експерти працюють за допомогою несвідомого “порівняння з взірцем” (“pattern matching”) у базі свого досвіду. От тільки проблема в тому, що функція “порівняння з взірцем” асинхронна і знаходиться в частині мозку, яка не підконтрольна свідомості.'
    
    return render_template("quiz_results.html", quiz_answers_block_dict=quiz_answers_block, 
                           general_score=general_score, programmer_level=programmer_level, 
                           quiz_block_score=quiz_block_score)


if __name__ == '__main__':
    app.run(debug=True)