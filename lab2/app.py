from flask import render_template, url_for, redirect
import numpy as np
from main_project import app
from main_project.utils.fuzzy_set import FuzzySet

@app.route('/')
def home():
    parameter_values = np.array((170, 175, 180, 185, 190, 195))
    expert_evaluations = np.array((9, 7, 5, 3, 1))
    fuzzy_set = FuzzySet(parameter_name='ріст', parameter_values=parameter_values, expert_evaluations=expert_evaluations)
    return render_template('home.html', fuzzy_set=fuzzy_set, cols_no=(len(fuzzy_set.parameter_values) + 1), precision=3)


@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.run(debug=True)