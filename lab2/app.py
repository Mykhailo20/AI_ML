from flask import render_template, url_for, redirect
from main_project import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == "__main__":
    app.run(debug=True)