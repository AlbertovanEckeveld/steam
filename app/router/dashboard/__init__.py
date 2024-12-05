from flask import Blueprint, render_template, session, redirect, url_for

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

