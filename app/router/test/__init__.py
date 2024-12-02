from flask import Blueprint, render_template

from app.connector.database import get_version, load_environment_variables

Test = Blueprint('test', __name__, static_folder='app/static', template_folder='app/templates')

@Test.route('/')
def index():

    DB_version = get_version()
    env_data = load_environment_variables()

    return render_template("test.html", version=DB_version, env_data=env_data)