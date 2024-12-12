from flask import Blueprint, session, redirect, url_for, request
from urllib.parse import urlencode

from app.connector import get_address
from app.connector.steam_api import get_user_profile

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
        'openid.return_to': f'http://{get_address()}/auth/authorize',
        'openid.realm': f'http://{get_address()}'
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
    # Haal de Steam ID op uit de response
    response = request.args
    steam_id = response['openid.claimed_id'].split('/id/')[-1]

    # Maak een User object met de Steam ID
    user_profile = get_user_profile(steam_id)
    session['user_profile'] = user_profile.__dict__

    # Stel de sessiegegevens in voor de ingelogde gebruiker
    session['user'] = steam_id

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