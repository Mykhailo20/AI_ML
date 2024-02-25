from main_project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    quizes = db.relationship('Quiz', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Quiz(db.Model):
    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    datetime = db.Column(db.DateTime)
    answers = db.relationship('UserAnswer', backref='quiz', lazy='dynamic')

    def __init__(self, user_id, datetime):
        self.user_id = user_id
        self.datetime = datetime

class UserAnswer(db.Model):
    __tablename__ = 'user_answer'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    block_name = db.Column(db.String(64))
    question_no = db.Column(db.Integer)
    answer_score = db.Column(db.Integer)

    def __init__(self, quiz_id, block_name, question_no, answer_score):
        self.quiz_id = quiz_id
        self.block_name = block_name
        self.question_no = question_no
        self.answer_score = answer_score