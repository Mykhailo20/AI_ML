from flask import render_template, url_for, redirect, request, session
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
        parameter_values = [int(param) for param in parameter_values]
        expert_evaluations = [int(eval) for eval in expert_evaluations]

        fuzzy_set_dict = {
            'parameter_name': parameter_name, 
            'parameter_values': parameter_values, 
            'expert_evaluations': expert_evaluations
        }

        session['fuzzy_set_dict'] = fuzzy_set_dict
        return redirect(url_for('result'))
    return render_template('home.html', form=form, max_parameter_values=6)


@app.route('/result')
def result():
    if 'fuzzy_set_dict' in session:
        fuzzy_set_dict = session['fuzzy_set_dict']
        fuzzy_set = FuzzySet(fuzzy_set_dict['parameter_name'], fuzzy_set_dict['parameter_values'], fuzzy_set_dict['expert_evaluations'])
        graph_dict = {}
        for i in range(len(fuzzy_set.parameter_values)):
            par_value = fuzzy_set.parameter_values[i]
            membership_function_value = fuzzy_set.membership_function[i]
            graph_dict[par_value] = membership_function_value
        print(f"graph_dict = {graph_dict}")
        sorted_graph_list = sorted(graph_dict.items(), key=lambda x:x[0])
        print(f"sorted_graph_list = {sorted_graph_list}")

        sorted_graph_dict = {}
        for i in range(len(sorted_graph_list)):
            par_value = sorted_graph_list[i][0]
            membership_function_value = sorted_graph_list[i][1]
            sorted_graph_dict[par_value] = membership_function_value
        print(f"sorted_graph_dict = {sorted_graph_dict}")
        return render_template('result.html', fuzzy_set=fuzzy_set, cols_no=(len(fuzzy_set.parameter_values) + 1), precision=3,
                               x_axis=sorted_graph_dict.keys(), y_axis=sorted_graph_dict.values())
    else:
        print("No fuzzy_set_dict in session")


@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.run(debug=True)