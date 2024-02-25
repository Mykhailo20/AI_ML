from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, login_required, logout_user

from main_project import app, db
from main_project.models import User
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

@app.route('/quiz', methods=["GET", "POST"])
@login_required
def quiz():
    form = QuizForm()
    return render_template('quiz.html', form=form)

"""
@app.route('/quiz', methods=["GET", "POST"])
@login_required
def quiz():
    blocks_forms = {"Novice": NoviceForm(), "Advanced beginner": AdvancedBeginnerForm(),
                   "Competent": CompetentForm(), "Proficient": ProficientForm(),
                   "Expert": ExpertForm()}
    blocks = ["Novice", "Advanced beginner", "Competent", "Proficient", "Expert"]
    blocks_answers = {"Novice": [], "Advanced beginner": [], "Competent": [], "Proficient": [], "Expert": []}
    index = 0
    block = blocks[index]
    form = NoviceForm()
    if form.validate_on_submit():
        if block != "Novice":
            blocks_answers[block].extend((form.q1_choice.data,  form.q2_choice.data,  form.q3_choice.data))
        else:
            blocks_answers[block].extend((form.q1_choice.data,  form.q2_choice.data,  form.q3_choice.data, form.q4_choice.data))
        index += 1
        block = blocks[index]
        return render_template("quiz.html", form=blocks_forms[block], block=block, blocks_answers=blocks_answers)
    return render_template("quiz.html", form=form, block="Novice", blocks_answers=blocks_answers)
"""

if __name__ == '__main__':
    app.run(debug=True)