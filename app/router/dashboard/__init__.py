from flask import Blueprint, render_template, session, redirect, url_for

from app.connector.steam_api import get_user_profile, get_owned_games
from app.models import UserProfile

# Dashboard blueprint
Dash = Blueprint('dashboard', __name__, static_folder='app/static', template_folder='app/templates')

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
    if not session.get('user'):
        return redirect(url_for('index.index'))

    # Haal de profile object van de gebruiker op
    user_profile_data = session.get('user_profile')
    user = UserProfile(**user_profile_data) if user_profile_data else None

    # Render de dashboard hoofdpagina met gebruikersgegevens
    return render_template("dashboard/dashboard.html",
                           display_name=user.get_displayname() if user else "",
                           url_avatar=user.get_avatar_small() if user else "")


@Dash.route('/library')
def library():
    """
        Bibliotheekpagina van de gebruiker.

        Returns:
        Response: Rendered template voor de bibliotheekpagina.
    """
    # Controleer of de gebruiker is ingelogd
    if not session.get('user'):
        return redirect(url_for('index.index'))

    # Haal de profile object van de gebruiker op
    user_profile_data = session.get('user_profile')
    user = UserProfile(**user_profile_data) if user_profile_data else None

    games = get_owned_games(user.get_steam_id()) if user else []

    # Render de bibliotheekpagina met gebruikersgegevens en spellenlijst
    return render_template("dashboard/dashboard-library.html",
                           display_name=user.get_displayname() if user else "",
                           url_avatar=user.get_avatar_small() if user else "",
                           games=games
                           )


@Dash.route('/friends')
def friends():
    """
        Vriendenpagina van de gebruiker.

        Returns:
        Response: Rendered template voor de vriendenpagina.
    """
    # Controleer of de gebruiker is ingelogd
    if not session.get('user'):
        return redirect(url_for('index.index'))

    # Haal de profile object van de gebruiker op
    user_profile_data = session.get('user_profile')
    user = UserProfile(**user_profile_data) if user_profile_data else None

    # Render de vriendenpagina met gebruikersgegevens en vriendenlijst
    return render_template("dashboard/dashboard-friends.html",
                           display_name=user.get_displayname() if user else "",
                           url_avatar=user.get_avatar_small()  if user else "",
                           friends=user.get_friendlist() if user else [],
                           total_friends=user.get_total_friends() if user else 0
                           )


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
    if not session.get('user'):
        return redirect(url_for('index.index'))

    # Haal de profile object van de gebruiker op
    user_profile_data = session.get('user_profile')
    user = UserProfile(**user_profile_data) if user_profile_data else None

    # Haal de spellenlijst van de gebruiker op
    games = get_owned_games(user.get_steam_id())

    # Maak een UserProfile object voor de vriend
    friend = get_user_profile(friend_id, incl_friends=False, incl_games=True)

    print(friend.get_games())
    print(f"Friend: {friend.get_steam_id()} Naam: {friend.get_displayname()}")

    # Render de spellenvergelijkingspagina met gebruikers- en vriend spelgegevens
    return render_template("dashboard/dashboard-friends-compare.html",
                           display_name=user.get_displayname() if user else "",
                           url_avatar=user.get_avatar_small() if user else "",
                           own_games=games if user else [],
                           friend_display_name=friend.get_displayname() if friend else "",
                           friend_avatar=friend.get_avatar_small() if friend else "",
                           friend_games=friend.get_games() if friend else [],
                           common_games=get_common_games(games, friend.get_games())
                           )