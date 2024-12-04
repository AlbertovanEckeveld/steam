from flask import Blueprint, render_template

Login = Blueprint('Login', __name__, static_folder='app/static', template_folder='app/templates')

@Login.route('/')
def index():
    return render_template("login.html")