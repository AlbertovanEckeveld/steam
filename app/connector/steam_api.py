import requests
from app.models import UserProfile
from app.connector import get_steam_API

API_KEY = get_steam_API()

def get_player_summary(steam_id):
    """
        Haal gebruiker(s) informatie op van de Steam API.

        Argumenten:
        steam_id (str of list): Steam ID of lijst van Steam IDs.

        Returns:
        dict: gebruikers informatie.
    """
    id = steam_id

    # Controleer of steam_id een lijst is en converteer naar een string
    if isinstance(steam_id, list):
        steam_id = ",".join(steam_id)
    elif not isinstance(steam_id, str):
        raise ValueError("steam_id moet een string of een lijst zijn.")

    # Stel de URL en parameters in voor de API-aanroep
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = { "key": API_KEY, "steamids": steam_id }

    # Voer de API-aanroep uit en controleer de status code van de response
    response = requests.get(url, params=params)
    if response.status_code == 200:

        # Return de spelersgegevens op uit de response
        if isinstance(id, str):
            return response.json()['response']['players'][0]

        return response.json()['response']['players']
    else:
        raise Exception(f"API request mislukt met status code {response.status_code}")


def get_player_displayname(steam_id):
    """
        Haal gebruikersweergavenaam op van de Steam API.

        Argumenten:
        steam_id (str of list): één Steam ID of lijst van Steam IDs.

        Returns:
        str of dict: Gebruikersweergavenaam of dict van weergavenamen.
    """
    # Haal de spelersgegevens op van de Steam API
    player_data = get_player_summary(steam_id)

    # Controleer of steam_id een string is en retourneer de weergavenaam
    if isinstance(steam_id, str):
        return player_data[0]['personaname'] if player_data else None

    # Maak een dict van weergavenamen voor een lijst van Steam IDs
    return {player['steamid']: player['personaname'] for player in player_data}


def get_friend_list(steam_id: str):
    """
        Haal vriendenlijst op van de Steam API.

        Argumenten:
        steam_id (str): Steam ID.

        Returns:
        list: Lijst van vrienden met details.
    """
    # Stel de URL en parameters in voor de API-aanroep
    url = "https://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
    params = {"key": API_KEY, "steamid": steam_id, "relationship": "friend" }

    # Voer de API-aanroep uit en controleer de status code van de response
    response = requests.get(url, params=params)
    if response.status_code != 200 or 'friendslist' not in response.json():
        raise Exception(f"Mislukt om vriendenlijst op te halen: {response.status_code}")

    # Haal de vriendenlijst op uit de response
    friends = response.json()['friendslist']['friends']
    friend_ids = [friend['steamid'] for friend in friends]

    # Haal de weergavenamen van de vrienden op
    display_names = get_player_displayname(friend_ids)

    # Return een lijst van vrienden met details
    return [
        {
            'steamid': friend['steamid'],
            'display_name': display_names.get(friend['steamid'], "Unknown"),
            'relationship': friend['relationship'],
            'friend_since': friend['friend_since']
        }
        for friend in friends
    ]
"""
 Voorbeeld van de return:
 [
   {'steamid': '76561198033737398', 'display_name': 'AlbertoVE', 'relationship': 'friend', 'friend_since': 1509471831},
   {'steamid': '76561198033737398', 'display_name': 'AlbertoVE', 'relationship': 'friend', 'friend_since': 1509471831}
 ]
"""


def get_owned_games(steam_id: str):
    """
        Haal bezeten spellen op van de Steam API.

        Argumenten:
        steam_id (str): Steam ID.

        Returns:
        list: Lijst van bezeten spellen met details.
    """
    # Stel de URL en parameters in voor de API-aanroep
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "include_appinfo": 1,
        "include_played_free_games": 1
    }

    # Voer de API-aanroep uit en controleer de status code van de response
    response = requests.get(url, params=params)
    if response.status_code != 200 or 'response' not in response.json():
        raise Exception(f"Failed to fetch game list: {response.status_code}")

    # Haal de spellenlijst op uit de response
    games = response.json().get('response', {}).get('games', [])

    # Return spellenlijst met details van de spellen gesorteerd op speeltijd
    return sorted(
        [
            {
                'appid': game['appid'],
                'name': game['name'],
                'url_avatar': game['img_icon_url'],
                'playtime_forever': round(game['playtime_forever'] / 60, 2)
            }
            for game in games
        ],
        key=lambda game: game['playtime_forever'], reverse=True
    )

def get_user_profile(steam_id: str, incl_games: bool = True):
    """
        Maakt een userprofile aan.

        Argumenten:
        steam_id (str): Steam ID.

        Returns:
        dict: Gebruikersprofiel.
    """
    # Haal de spelersgegevens op van de Steam API
    player_data = get_player_summary(steam_id)

    # Haal de vriendenlijst op van de Steam API
    try:
        friend_list = get_friend_list(steam_id)
    except Exception as e:
        friend_list = []
        print(f'Fout: {e}, vriendenlijst mogelijk op prive. Vriendenlijst is leeg: {friend_list}')

    # Haal de bezeten spellen op van de Steam API
    try:
        owned_games = get_owned_games(steam_id)
    except Exception as e:
        owned_games = []
        print(f'Fout: {e}, gamelijst mogelijk op prive. Gamelijst is leeg: {friend_list}')

    # Maak een dict van het gebruikersprofiel
    return {
        'steamid': player_data['steamid'],
        'display_name': player_data['personaname'],
        'profile_url': player_data['profileurl'],
        'avatar_url': player_data['avatarfull'],
        'friend_count': player_data['friend_count'],
        'friends': friend_list,
        'game_count': len(owned_games),
        'games': owned_games
    }