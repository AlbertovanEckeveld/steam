from flask import Blueprint, render_template, session, redirect, url_for

from app.connector.steam_api import get_player_summary, get_friend_list, get_owned_games
from app.models import UserProfile

Dash = Blueprint('dashboard', __name__, static_folder='app/static', template_folder='app/templates')


def get_common_games(own_games, friend_games):
    """Bepaalt de gemeenschappelijke games en vergelijkt speeltijden."""
    own_game_dict = {game['appid']: game for game in own_games}
    friend_game_dict = {game['appid']: game for game in friend_games}

    common_games = []
    for game_id in own_game_dict:
        if game_id in friend_game_dict:
            own_time = own_game_dict[game_id].get('playtime_forever', 0)
            friend_time = friend_game_dict[game_id].get('playtime_forever', 0)
            common_games.append({
                'id': game_id,
                'name': own_game_dict[game_id]['name'],
                'own_playtime': own_time,
                'friend_playtime': friend_time
            })
    return common_games


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
        games = get_owned_games(session.get('user')['steam_id'])

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
        own_games = get_owned_games(session.get('user')['steam_id'])

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
                               friend_games=friend.game_list,
                               common_games=get_common_games(own_games, friend.game_list)
                               )