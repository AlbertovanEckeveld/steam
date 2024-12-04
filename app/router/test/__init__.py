from flask import Blueprint, render_template

from app.connector import get_database_info, get_user_info
from app.connector.database import get_version
from app.connector.steam_api import get_player_summary

Test = Blueprint('test', __name__, static_folder='app/static', template_folder='app/templates')

@Test.route('/')
def index():

    DB_version = get_version()
    database = get_database_info()
    user = get_user_info()
    player = get_player_summary("76561198273359778")
    username = player["response"]["players"][0]["personaname"]
    user_id = player["response"]["players"][0]["steamid"]


    return render_template("test.html", version=DB_version, database=database, user=user, player=username, user_id=user_id)