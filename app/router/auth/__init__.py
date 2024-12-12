from flask import Blueprint, session, redirect, url_for, request
from urllib.parse import urlencode

from app.models import UserProfile
from app.connector import get_ipv4_address
from app.connector.steam_api import get_player_summary, get_friend_list


# Auth blueprint
Auth = Blueprint('auth', __name__, static_folder='app/static', template_folder='app/templates')

@Auth.route('/')
def index():
    """
        Index route voor authenticatie.

        Returns:
        Response: Redirect naar de juiste pagina op basis van de sessiestatus.
    """
    # Controleer of de gebruiker is ingelogd
    if not session.get('user'):
        # Redirect naar de indexpagina als de gebruiker niet is ingelogd
        return redirect(url_for('index.index'))
    else:
        # Redirect naar de dashboardpagina als de gebruiker is ingelogd
        return redirect(url_for('dashboard.index'))


@Auth.route('/login')
def login():
    """
        Login route voor Steam.

        Returns:
        Response: Redirect naar de Steam login pagina.
    """
    # Stel de parameters in voor de Steam OpenID login
    params = {
        'openid.ns': "http://specs.openid.net/auth/2.0",
        'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.mode': 'checkid_setup',
        'openid.return_to': f'http://{get_ipv4_address()}/auth/authorize',
        'openid.realm': f'http://{get_ipv4_address()}'
    }

    # Maak de query string en de volledige URL voor de Steam login
    query_string = urlencode(params)
    auth_url = 'https://steamcommunity.com/openid/login' + "?" + query_string

    # Redirect naar de Steam login pagina
    return redirect(auth_url)


@Auth.route('/authorize')
def authorize():
    """
        Authorize route voor Steam login callback.

        Returns:
        Response: Redirect naar de dashboard pagina.
    """
    # Haal de response parameters op
    response = request.args

    # Haal de Steam ID op uit de response
    steam_id = response['openid.claimed_id'].split('/id/')[-1]

    # Haal de gebruikersgegevens op van Steam
    fetchdata = get_player_summary(steam_id)

    try:
        # Haal de vriendenlijst op van de gebruiker van Steam
        friend_list = get_friend_list(steam_id)
    except Exception as e:
        # Log de fout en stel de vriendenlijst in op een lege lijst
        print(e)
        friend_list = []

    # Maak een UserProfile object voor de gebruiker
    user = UserProfile(steam_id=steam_id,
                       display_name = fetchdata['personaname'],
                       url_avatar_small = fetchdata['avatar'],
                       url_avatar_medium = fetchdata['avatarmedium'],
                       url_avatar_full = fetchdata['avatarfull'],
                       url_profile = fetchdata['profileurl'],
                       friend_list = friend_list
                       )

    # Stel de sessiegegevens in voor de ingelogde gebruiker
    session['user'] = user

    # Redirect naar de dashboard pagina
    return redirect(url_for('dashboard.index'))


@Auth.route('/logout')
def logout():
    """
        Logout route voor de gebruiker.

        Returns:
        Response: Redirect naar de indexpagina.
    """
    # Verwijder alle sessiegegevens
    session.clear()

    # Redirect naar de indexpagina
    return redirect(url_for('index.index'))