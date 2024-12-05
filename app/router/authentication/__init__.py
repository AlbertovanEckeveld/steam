from flask import Blueprint, session, redirect, url_for, request
from json import dumps
from urllib.parse import urlencode

from app.connector.steam_api import get_player_summary, get_friend_list, get_owned_games
from app.models import UserProfile

Auth = Blueprint('auth', __name__, static_folder='app/static', template_folder='app/templates')

@Auth.route('/')
def index():
    if not session.get('steam_id'):
        return '<a href="http://127.0.0.1:5000/auth/login">Login with steam</a>'
    else:
        return redirect(url_for('index.index'))

@Auth.route('/login')
def login():
    params = {
        'openid.ns': "http://specs.openid.net/auth/2.0",
        'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.mode': 'checkid_setup',
        'openid.return_to': 'http://127.0.0.1:5000/auth/authorize',
        'openid.realm': 'http://127.0.0.1:5000'
    }

    query_string = urlencode(params)
    auth_url = 'https://steamcommunity.com/openid/login' + "?" + query_string
    print(auth_url)
    return redirect(auth_url)


@Auth.route('/authorize')
def authorize():
    response = request.args
    steam_id = response['openid.identity'].split('/id/')[-1]
    session['steam_id'] = steam_id
    print(get_player_summary(steam_id)['response']['players'][0])
    fetchdata = get_player_summary(steam_id)['response']['players'][0]
    user = UserProfile(steam_id=steam_id,
                       display_name = fetchdata['personaname'],
                       url_avatar_small = fetchdata['avatar'],
                       url_avatar_medium = fetchdata['avatarmedium'],
                       url_avatar_full = fetchdata['avatarfull'],
                       url_profile = fetchdata['profileurl'],
                       friend_list = get_friend_list(steam_id),
                       game_list = get_owned_games(steam_id)
                       )

    session['steam_id'] = steam_id
    session['user'] = user

    return redirect(url_for('index.index'))


@Auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.index'))