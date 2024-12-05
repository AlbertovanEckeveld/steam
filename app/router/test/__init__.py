from flask import Blueprint, render_template, session

from app.connector import get_database_info, get_user_info
from app.connector.database import get_version

Test = Blueprint('test', __name__, static_folder='app/static', template_folder='app/templates')

@Test.route('/')
def index():
    DB_version = get_version()
    database_info = get_database_info()
    DB_host = database_info.get('DB_HOST')
    DB_port = database_info.get('DB_PORT')
    DB_database = database_info.get('DB_DATABASE')
    DB_user = get_user_info()['DB_USER']
    if session.get('user'):
        Steam_user = [session.get('user')['display_name'], session.get('user')['steam_id'], session.get('user')['url_avatar_small']]
        logged_in = True
        return render_template("test.html",
                               version=DB_version,
                               DB_host=DB_host,
                               DB_port=DB_port,
                               DB_database=DB_database,
                               DB_user=DB_user,
                               logged_in=logged_in,
                               display_name=Steam_user[0],
                               steam_id=Steam_user[1],
                               steam_avater=Steam_user[2]
                               )
    else:
        logged_in = False
        return render_template("test.html",
                               version=DB_version,
                               DB_host=DB_host,
                               DB_port=DB_port,
                               DB_database=DB_database,
                               DB_user=DB_user,
                               logged_in=logged_in,
                               )
