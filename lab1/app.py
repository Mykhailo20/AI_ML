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

"""
@app.route('/quiz_novice', methods=["GET", "POST"])
@login_required
def quiz_novice():
    form = NoviceForm()
    if form.validate_on_submit():
        q1_answer = form.q1_choice.data
        q2_answer = form.q2_choice.data
        q3_answer = form.q3_choice.data
        q4_answer = form.q4_choice.data
        print(f"q1_answer = {q1_answer}; q2_answer={q2_answer}; q3_answer={q3_answer}; q4_answer={q4_answer}")
        return redirect(url_for('quiz_adv_beginner'))
    return render_template('quiz.html', form=form, block="Novice")
"""

@app.route('/quiz/<block>', methods=["GET", "POST"])
@login_required
def quiz(block):
    blocks_forms = {"novice": NoviceForm(), "advanced_beginner": AdvancedBeginnerForm(),
                   "competent": CompetentForm(), "proficient": ProficientForm(),
                   "expert": ExpertForm()}
    blocks = list(blocks_forms.keys())
    
    form = blocks_forms[block]
    if form.validate_on_submit():
        print(f"\nblock = {block}")
        if block != "novice":
            # Get last quiz
            quiz = Quiz.query.all()[-1]
            print(f"quiz.id = {quiz.id}")
            q1_answer = UserAnswer(quiz_id=quiz.id, block_name=block, question_no=1, answer_score=form.q1_choice.data)
            q2_answer = UserAnswer(quiz_id=quiz.id, block_name=block, question_no=2, answer_score=form.q2_choice.data)
            q3_answer = UserAnswer(quiz_id=quiz.id, block_name=block, question_no=3, answer_score=form.q3_choice.data)
            db.session.add_all([q1_answer, q2_answer, q3_answer])
            db.session.commit()
            print(f"q1_answer = {q1_answer.answer_score}; q2_answer={q2_answer.answer_score}; q3_answer={q3_answer.answer_score}")
        else:
            # if there is no prev buttons
            # Create a quiz table record
            print(f"current_user.id = {current_user.id}")
            quiz = Quiz(user_id=current_user.id, datetime=datetime.now())
            db.session.add(quiz)
            db.session.commit()

            q1_answer = UserAnswer(quiz_id=quiz.id, block_name='novice', question_no=1, answer_score=form.q1_choice.data)
            q2_answer = UserAnswer(quiz_id=quiz.id, block_name='novice', question_no=2, answer_score=form.q2_choice.data)
            q3_answer = UserAnswer(quiz_id=quiz.id, block_name='novice', question_no=3, answer_score=form.q3_choice.data)
            q4_answer = UserAnswer(quiz_id=quiz.id, block_name='novice', question_no=4, answer_score=form.q4_choice.data)
            db.session.add_all([q1_answer, q2_answer, q3_answer, q4_answer])
            db.session.commit()
            print(f"q1_answer = {q1_answer.answer_score}; q2_answer={q2_answer.answer_score}; q3_answer={q3_answer.answer_score}; q4_answer={q4_answer.answer_score}")


        if block != "expert":
            current_index = blocks.index(block)
            next_block = blocks[current_index + 1]
            return redirect(url_for('quiz', block=next_block))
        return redirect(url_for('quiz_results'))
    return render_template('quiz.html', form=form, block=block)


@app.route('/quiz_results', methods=["GET", "POST"])
@login_required
def quiz_results():
    current_quiz = Quiz.query.all()[-1]
    print(f"quiz.id = {current_quiz.id}")
    quiz_answers = UserAnswer.query.filter_by(quiz_id=current_quiz.id).all()
    print(f"len(quiz_answers) = {len(quiz_answers)}")
    for answer in quiz_answers:
        print(f"answer.id = {answer.id}, answer.quiz_id = {answer.quiz_id}, answer.block_name = {answer.block_name}")
        print(f"answer.question_no={answer.question_no}, answer.answer_score = {answer.answer_score}\n")
    
    quiz_answers_block = {}
    for answer in quiz_answers:
        block_name = answer.block_name
        if block_name not in quiz_answers_block:
            quiz_answers_block[block_name] = {'question_nos': [], 'answer_scores': []}
        quiz_answers_block[block_name]['question_nos'].append(answer.question_no)
        quiz_answers_block[block_name]['answer_scores'].append(answer.answer_score)
        
    return render_template("quiz_results.html", quiz_answers_block_dict=quiz_answers_block)


if __name__ == '__main__':
    app.run(debug=True)