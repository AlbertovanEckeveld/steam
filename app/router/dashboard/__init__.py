from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request 

from app.connector.steam_api import get_user_profile, get_owned_games, get_common_games, get_recent_playtime
from app.connector.afstandsensor import measure_distance
from app.models import UserProfile
import random
from app.connector.ai.prediction import visualize_creation_dates_with_regression
from app.connector.ai.gemiddelde import gemiddelde_functie
from app.connector.ai.mediaan import mediaan_functie


# Dashboard blueprint
Dash = Blueprint('dashboard', __name__, static_folder='app/static', template_folder='app/templates')

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

    recent = get_recent_playtime(user.get_steam_id())

    afstand = round(measure_distance(), 2)

    # Render de dashboard hoofdpagina met gebruikersgegevens
    return render_template("dashboard/dashboard.html",
                            display_name=user.get_displayname() if user else "",
                            url_avatar=user.get_avatar_small() if user else "",
                            games=recent['games'],
                            playtime=recent['total_playtime_2weeks'],
                            afstand=afstand if afstand else 0
                           )


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

    # Haal de spellenlijst van de gebruiker op
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
                           friends=user.get_friendlist(),
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

    # Render de spellenvergelijkingspagina met gebruikers- en vriend spelgegevens
    return render_template("dashboard/dashboard-friends-compare.html",
                           display_name=user.get_displayname() if user else "",
                           url_avatar=user.get_avatar_small() if user else "",
                           own_games=games,
                           friend_display_name=friend.get_displayname() if friend else "",
                           friend_avatar=friend.get_avatar_small() if friend else "",
                           friend_games=friend.get_games(),
                           common_games=get_common_games(games, friend.get_games())
                           )

@Dash.route('/statistics')
def statistics():
    """
        Statistieken van de gebruiker en steam.

        Returns:
        Response: Rendered template voor de statistiekenpagina.
    """
    # Controleer of de gebruiker is ingelogd
    if not session.get('user'):
        return redirect(url_for('index.index'))

    # Haal de profile object van de gebruiker op
    user_profile_data = session.get('user_profile')
    user = UserProfile(**user_profile_data) if user_profile_data else None

    img_prediction = f'{user.display_name}-{random.randrange(0, 99999)}'
    prediction = visualize_creation_dates_with_regression(user.get_steam_id(), img_prediction)

    img_gemiddelde = 'gemiddelde'
    gemiddelde_functie(img_gemiddelde)

    img_mediaan = 'mediaan'
    mediaan_functie(img_mediaan)


    # Render de statistiekenpagina met gebruikersgegevens
    return render_template("dashboard/dashboard-statistics.html",
                           display_name=user.get_displayname() if user else "",
                           url_avatar=user.get_avatar_small() if user else "",
                           img_prediction=img_prediction,
                           img_gemiddelde=img_gemiddelde if img_gemiddelde else "",
                           img_mediaan=img_mediaan if img_mediaan else "",
                           prediction = prediction
                           )


@Dash.route('/afstand', methods = ['GET'])
def afstand():
    """
        Afstand van de gebruiker tussen het beeldscherm.

        Returns:
        Response: Rendered template voor de afstandpagina.
    """
    if(request.method == 'GET'): 
        afstand = round(measure_distance(), 2)
        return jsonify({'afstand': afstand if afstand else 0})