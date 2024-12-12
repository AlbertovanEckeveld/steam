from flask import Blueprint, render_template, session, redirect, url_for

from app.connector.steam_api import get_player_summary, get_friend_list, get_owned_games
from app.models import UserProfile

# Dashboard blueprint
Dash = Blueprint('dashboard', __name__, static_folder='app/static', template_folder='app/templates')

def get_user_session_data():
    """
        Haal gebruikerssessiegegevens op.

        Returns:
        dict: Gebruikerssessiegegevens.
    """
    # Haal gebruikerssessiegegevens op uit de sessie
    return session.get('user', {})

def get_common_games(own_games, friend_games):
    """
        Bepaal gemeenschappelijke spellen en vergelijk speeltijden.

        Argumenten:
        own_games (list): Lijst van spellen die de gebruiker bezit.
        friend_games (list): Lijst van spellen die de vriend bezit.

        Returns:
        list: Lijst van gemeenschappelijke spellen met speeltijden.
    """
    # Maak dictionaries van de spellenlijsten
    own_game_dict = {game['appid']: game for game in own_games}
    friend_game_dict = {game['appid']: game for game in friend_games}

    # Maak een lijst van gemeenschappelijke spellen met speeltijden
    return [
        {
            'id': game_id,
            'name': own_game_dict[game_id]['name'],
            'own_playtime': own_game_dict[game_id].get('playtime_forever', 0),
            'friend_playtime': friend_game_dict[game_id].get('playtime_forever', 0)
        }
        for game_id in own_game_dict if game_id in friend_game_dict
    ]

@Dash.route('/')
def index():
    """
        Dashboard hoofdpagina.

        Returns:
        Response: Rendered template voor de dashboard hoofdpagina.
    """
    # Controleer of de gebruiker is ingelogd
    user = get_user_session_data()
    if not user:
        return redirect(url_for('index.index'))

    # Render de dashboard hoofdpagina met gebruikersgegevens
    return render_template("dashboard/dashboard.html",
                           display_name=user['display_name'],
                           url_avatar=user['url_avatar_small'])


@Dash.route('/library')
def library():
    """
        Bibliotheekpagina van de gebruiker.

        Returns:
        Response: Rendered template voor de bibliotheekpagina.
    """
    # Controleer of de gebruiker is ingelogd
    user = get_user_session_data()
    if not user:
        return redirect(url_for('index.index'))

    try:
        # Haal de spellen van de gebruiker op
        games = get_owned_games(user['steam_id'])
    except Exception as e:
        # Log de fout en stel de spellenlijst in op een lege lijst
        print(e)
        games = []

    # Render de bibliotheekpagina met gebruikersgegevens en spellenlijst
    return render_template("dashboard/dashboard-library.html",
                           display_name=user['display_name'],
                           url_avatar=user['url_avatar_small'],
                           games=games)


@Dash.route('/friends')
def friends():
    """
        Vriendenpagina van de gebruiker.

        Returns:
        Response: Rendered template voor de vriendenpagina.
    """
    # Controleer of de gebruiker is ingelogd
    user = get_user_session_data()
    if not user:
        return redirect(url_for('index.index'))

    # Haal de vriendenlijst op uit de sessiegegevens
    friendlist = user.get('friend_list', [])

    # Render de vriendenpagina met gebruikersgegevens en vriendenlijst
    return render_template("dashboard/dashboard-friends.html",
                           display_name=user['display_name'],
                           url_avatar=user['url_avatar_small'],
                           friends=friendlist,
                           total_friends=len(friendlist))


@Dash.route('/compare/<friend_id>')
def compare(friend_id):
    """
        Vergelijk spellen met een vriend.

        Argumenten:
        friend_id (str): Steam ID van de vriend.

        Returns:
        Response: Rendered template voor de spellenvergelijkingspagina.
    """
    # Controleer of de gebruiker is ingelogd
    user = get_user_session_data()
    if not user:
        return redirect(url_for('index.index'))

    # Haal de spellen van de gebruiker zelf op
    own_games = get_owned_games(user['steam_id'])
    # Haal de gegevens van de vriend op
    fetchdata = get_player_summary(friend_id)

    try:
        # Haal de spellen van vriend op
        friend_games = get_owned_games(friend_id)
    except Exception as e:
        # Log de fout en stel de spellenlijst van de vriend in op een lege lijst
        print(e)
        friend_games = []

    # Maak een UserProfile object voor de vriend
    friend = UserProfile(
        steam_id=friend_id,
        display_name=fetchdata['personaname'],
        url_avatar_small=fetchdata['avatar'],
        url_avatar_medium=fetchdata['avatarmedium'],
        url_avatar_full=fetchdata['avatarfull'],
        url_profile=fetchdata['profileurl'],
        game_list=friend_games
    )

    # Render de spellenvergelijkingspagina met gebruikers- en vriendgegevens
    return render_template("dashboard/dashboard-friends-compare.html",
                           display_name=user['display_name'],
                           url_avatar=user['url_avatar_small'],
                           own_games=own_games,
                           friend_display_name=friend.display_name,
                           friend_avatar=friend.get_avatar_small(),
                           friend_games=friend.game_list,
                           common_games=get_common_games(own_games, friend.game_list))