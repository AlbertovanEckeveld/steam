from flask import Blueprint, render_template, session, redirect, url_for

from app.connector.steam_api import get_player_summary, get_friend_list, get_owned_games
from app.models import UserProfile

Dash = Blueprint('dashboard', __name__, static_folder='app/static', template_folder='app/templates')


@Dash.route('/')
def index():
    if not session.get('user'):
        return redirect(url_for('index.index'))
    else:
        display_name = session.get('user')['display_name']
        url_avatar = session.get('user')['url_avatar_small']

        return render_template("dashboard/dashboard.html",
                               display_name=display_name,
                               url_avatar=url_avatar
                               )


@Dash.route('/library')
def library():
    if not session.get('user'):
        return redirect(url_for('index.index'))
    else:
        display_name = session.get('user')['display_name']
        url_avatar = session.get('user')['url_avatar_small']
        games = session.get('user')['game_list']

        return render_template("dashboard/dashboard-library.html",
                               display_name=display_name,
                               url_avatar=url_avatar,
                               games=games
                               )


@Dash.route('/friends')
def friends():
    if not session.get('user'):
        return redirect(url_for('index.index'))
    else:
        display_name = session.get('user')['display_name']
        url_avatar = session.get('user')['url_avatar_small']

        friendlist = session.get('user')['friend_list']
        total_friends = len(friendlist)

        return render_template("dashboard/dashboard-friends.html",
                               display_name=display_name,
                               url_avatar=url_avatar,
                               friends=friendlist,
                               total_friends=total_friends
                               )


@Dash.route('/compare/<friend_id>')
def compare(friend_id):
    if not session.get('user'):
        return redirect(url_for('index.index'))
    else:
        display_name = session.get('user')['display_name']
        url_avatar = session.get('user')['url_avatar_small']
        own_games = session.get('user')['game_list']

        fetchdata = get_player_summary(friend_id)['response']['players'][0]

        try:
            friend_games = get_owned_games(friend_id)
        except KeyError as e:
            print(f"KeyError: {e}. The 'games' key was not found in the response. Perhaps this user has no games.")
            friend_games = []
        except Exception as e:
            print(f"An error occurred: {e}")
            friend_games = []  # Handle any other exceptions gracefully


        friend = UserProfile(steam_id=friend_id,
                           display_name=fetchdata['personaname'],
                           url_avatar_small=fetchdata['avatar'],
                           url_avatar_medium=fetchdata['avatarmedium'],
                           url_avatar_full=fetchdata['avatarfull'],
                           url_profile=fetchdata['profileurl'],
                           game_list=friend_games
                           )

        return render_template("dashboard/dashboard-friends-compare.html",
                               display_name=display_name,
                               url_avatar=url_avatar,
                               own_games=own_games,
                               friend_display_name=friend.display_name,
                               friend_avatar=friend.get_avatar_small(),
                               friend_games=friend.game_list
                               )