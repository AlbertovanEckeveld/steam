from flask import Blueprint, render_template, session

Index = Blueprint('index', __name__, static_folder='app/static', template_folder='app/templates')

@Index.route('/')
def index():
    if not session.get('steam_id'):
        steam_id = False
    else:
        steam_id = True

    return render_template("index.html", steam_id=steam_id, user=session.get('user'))