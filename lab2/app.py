from flask import render_template, url_for, redirect, request, jsonify, session
from main_project import app
from main_project.forms import *
from main_project.utils.fuzzy_set import FuzzySet
from main_project.utils.display_data import prepare_graph_data

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
        
        graph_dict = prepare_graph_data(fuzzy_set.parameter_values, fuzzy_set.membership_function)
        return render_template('result.html', fuzzy_set=fuzzy_set, cols_no=(len(fuzzy_set.parameter_values) + 1), precision=3,
                               x_axis=graph_dict.keys(), y_axis=graph_dict.values())


@app.route('/update_parameters', methods=['POST'])
def update_parameters():
    updated_parameter_values = request.json
    print(f"updated_parameter_values = {updated_parameter_values}")

    if 'fuzzy_set_dict' in session:
        fuzzy_set_dict = session['fuzzy_set_dict']
        fuzzy_set = FuzzySet(fuzzy_set_dict['parameter_name'], updated_parameter_values, fuzzy_set_dict['expert_evaluations'])
        graph_dict = prepare_graph_data(fuzzy_set.parameter_values, fuzzy_set.membership_function)
        print(f"fuzzy_set.parameter_values = {fuzzy_set.parameter_values}")
        # Convert parameter values and graph data to JSON-serializable types
        parameter_values = [float(val) for val in fuzzy_set.parameter_values]
        graph_data = {
            'x_axis': list(map(float, graph_dict.keys())),
            'y_axis': list(map(float, graph_dict.values()))
        }

        # Return JSON data containing the updated parameter values and graph data
        return jsonify({
            'parameter_values': parameter_values,
            'graph_data': graph_data
        })

@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.run(debug=True)