from flask import Blueprint, render_template

Index = Blueprint('index', __name__, static_folder='app/static', template_folder='app/templates')

@Index.route('/')
def index():
    return render_template("index.html")