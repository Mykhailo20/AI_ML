from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, FieldList, FormField
from wtforms.validators import DataRequired

class DataForm(FlaskForm):
    parameter_name = StringField("Назва параметра: ", validators=[DataRequired()])
    parameter_value = FloatField("Значення параметра: ", validators=[DataRequired()])
    expert_evaluation = FloatField("Експертна оцінка: ", validators=[DataRequired()])
    submit = SubmitField("Результати")