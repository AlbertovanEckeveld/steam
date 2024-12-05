from flask import Blueprint, render_template, session, redirect, url_for

Index = Blueprint('index', __name__, static_folder='app/static', template_folder='app/templates')

@Index.route('/')
def index():
    if not session.get('user'):
        return render_template("index.html")
    else:
        return redirect(url_for('dashboard.index'))

