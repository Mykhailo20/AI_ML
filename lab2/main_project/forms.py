from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired

class DataForm(FlaskForm):
    parameter_name = StringField("Назва параметра: ", validators=[DataRequired()])
    parameter_value = FloatField("Значення параметра: ", validators=[DataRequired()])
    expert_evaluation = SelectField(u"Експертна оцінка: ", choices=[(i, i) for i in range(1, 10)])
    submit = SubmitField("Результати")