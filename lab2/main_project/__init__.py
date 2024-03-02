from flask import Flask
from jinja2 import Environment

def format_precision(value, precision):
    return f"{value:.{precision}f}"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.jinja_env.filters['format_precision'] = format_precision