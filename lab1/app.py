from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, login_required, logout_user

from main_project import app, db
from main_project.models import User
from main_project.forms import LoginForm, RegisterForm

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


if __name__ == '__main__':
    app.run(debug=True)