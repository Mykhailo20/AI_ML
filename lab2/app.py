from flask import render_template, url_for, redirect, request
import numpy as np
from main_project import app
from main_project.forms import *
from main_project.utils.fuzzy_set import FuzzySet

@app.route('/', methods=['GET', 'POST'])
def home():
    form = DataForm()
    if form.validate_on_submit():
        parameter_name = form.parameter_name.data
        parameter_values = request.form.getlist('parameter_value_td')
        expert_evaluations = request.form.getlist('expert_evaluation_td')
        print(f"parameter_name = {parameter_name}")
        print(f"parameter_values = {parameter_values}")
        print(f"expert_evaluations = {expert_evaluations}")
        return redirect(url_for('result'))
    return render_template('home.html', form=form, max_parameter_values=6)


@app.route('/result')
def result():
    parameter_values = np.array((170, 175, 180, 185, 190, 195))
    expert_evaluations = np.array((9, 7, 5, 3, 1))
    fuzzy_set = FuzzySet(parameter_name='ріст', parameter_values=parameter_values, expert_evaluations=expert_evaluations)
    return render_template('result.html', fuzzy_set=fuzzy_set, cols_no=(len(fuzzy_set.parameter_values) + 1), precision=3)


@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.run(debug=True)