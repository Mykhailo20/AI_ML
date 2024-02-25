from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from main_project.models import User

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField("Confirm Password: ", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
        

class NoviceForm(FlaskForm):
    q1_choice = SelectField(u"Переживаєте за успіх в роботі?", 
                            choices=[(5, "сильно"), (3, "не дуже"), (2, "спокійний")])
    q2_choice = SelectField(u"Прагнете досягти швидко результату?", 
                            choices=[(5, "дуже"), (3, "якомога швидше"), (2, "поступово")])
    q3_choice = SelectField(u"Легко попадаєте в тупик при проблемах в роботі?", 
                            choices=[(5, "неодмінно"), (3, "поступово"), (2, "зрідка")])
    q4_choice = SelectField(u"Чи потрібен чіткий алгоритм для вирішення задач?", 
                            choices=[(5, "так"), (3, "в окремих випадках"), (2, "не потрібен")])
    submit_next = SubmitField("Next")


class AdvancedBeginnerForm(FlaskForm):
    q1_choice = SelectField(u"Чи використовуєте власний досвід при вирішенні задач?", 
                            choices=[(5, "зрідка"), (3, "частково"), (2, "ні")])
    q2_choice = SelectField(u"Чи користуєтесь фіксованими правилами  для вирішення задач?", 
                            choices=[(5, "не потрібні"), (3, "в окремих випадках"), (2, "так")])
    q3_choice = SelectField(u"Чи відчуваєте ви загальний контекст вирішення задачі?", 
                            choices=[(5, "в окремих випадках"), (3, "частково"), (2, "так")])
    submit_prev = SubmitField("Prev")
    submit_next = SubmitField("Next")
    
class CompetentForm(FlaskForm):
    q1_choice = SelectField(u"Чи можете ви побудувати модель вирішуваної задачі?", 
                            choices=[(5, "так"), (3, "не повністю"), (2, "в окремих випадках")])
    q2_choice = SelectField(u"Чи вистачає вам ініціативи при вирішенні задач?", 
                            choices=[(5, "так"), (3, "зрідка"), (2, "потрібне натхнення")])
    q3_choice = SelectField(u"Чи можете вирішувати проблеми, з якими ще не стикались?", 
                            choices=[(5, "ні"), (3, "в окремих випадках"), (2, "так")])
    submit_prev = SubmitField("Prev")
    submit_next = SubmitField("Next")

class ProficientForm(FlaskForm):
    q1_choice = SelectField(u"Чи необхідний вам весь контекст задачі?", 
                            choices=[(5, "так"), (3, "в окремих деталях"), (2, "в загальному")])
    q2_choice = SelectField(u"Чи переглядаєте ви свої наміри до вирішення задачі?", 
                            choices=[(5, "так"), (3, "зрідка"), (2, "коли є потреба")])
    q3_choice = SelectField(u"Чи здатні  ви  навчатись у інших?", 
                            choices=[(5, "так"), (3, "зрідка"), (2, "коли є потреба")])
    submit_prev = SubmitField("Prev")
    submit_next = SubmitField("Next")

class ExpertForm(FlaskForm):
    q1_choice = SelectField(u"Чи обираєте ви нові методи своєї роботи?", 
                            choices=[(5, "так"), (3, "вибірково"), (2, "вистачає досвіду")])
    q2_choice = SelectField(u"Чи допомагає власна інтуїція при вирішенні задач?", 
                            choices=[(5, "так"), (3, "частково"), (2, "при емоційному напруженні")])
    q3_choice = SelectField(u"Чи застовуєте рішення задач за аналогією?", 
                            choices=[(5, "часто"), (3, "зрідка"), (2, "тільки власний варіант")])
    submit = SubmitField("Submit")    