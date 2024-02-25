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
        if block != "novice":
            print(f"\nblock = {block}")
            q1_answer = form.q1_choice.data
            q2_answer = form.q2_choice.data
            q3_answer = form.q3_choice.data
            print(f"q1_answer = {q1_answer}; q2_answer={q2_answer}; q3_answer={q3_answer}")
        else:
            print(f"\nblock = {block}")
            q1_answer = form.q1_choice.data
            q2_answer = form.q2_choice.data
            q3_answer = form.q3_choice.data
            q4_answer = form.q4_choice.data
            print(f"q1_answer = {q1_answer}; q2_answer={q2_answer}; q3_answer={q3_answer}; q4_answer={q4_answer}")

        if block != "expert":
            current_index = blocks.index(block)
            next_block = blocks[current_index + 1]
            return redirect(url_for('quiz', block=next_block))
        return redirect(url_for('quiz_results'))
    return render_template('quiz.html', form=form, block=block)


@app.route('/quiz_results', methods=["GET", "POST"])
@login_required
def quiz_results():
    return "<h1>quiz_results</h1>"


if __name__ == '__main__':
    app.run(debug=True)