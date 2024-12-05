from flask import Blueprint, render_template, session, redirect, url_for

Dash = Blueprint('dashboard', __name__, static_folder='app/static', template_folder='app/templates')


@Dash.route('/')
def index():
    if not session.get('steam_id'):
        return redirect(url_for('index.index'))
    else:
        return render_template("dashboard.html", user=session.get('user'))


@Dash.route('/library')
def library():
    if not session.get('steam_id'):
        return redirect(url_for('index.index'))
    else:
        games = session.get('user')['game_list']
        return render_template("dashboard-library.html", user=session.get('user'), games=games)


@Dash.route('/friends')
def friends():
    if not session.get('steam_id'):
        return redirect(url_for('index.index'))
    else:
        friendlist = session.get('user')['friend_list']
        total_friends = len(friendlist)
        return render_template("dashboard-friends.html", user=session.get('user'), friends=friendlist, total_friends=total_friends)

