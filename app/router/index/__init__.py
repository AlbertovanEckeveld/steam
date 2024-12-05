from flask import Blueprint, render_template, session

Index = Blueprint('index', __name__, static_folder='app/static', template_folder='app/templates')

@Index.route('/')
def index():
    if not session.get('steam_id'):
        signed_in = False
    else:
        signed_in = True

    return render_template("index.html", signed_in=signed_in, user=session.get('user'))