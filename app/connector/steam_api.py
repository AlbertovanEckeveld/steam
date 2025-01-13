import requests
from app.models import UserProfile
from app.connector import get_steam_API

API_KEY = get_steam_API()

def get_player_summary(steam_id: str):
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


def get_friend_info(steam_id: str):
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
    return {player['steamid']: {'personaname': player['personaname'], 'avatar': player['avatar']} for player in player_data}


def get_friend_list(steam_id: str):
    """
        Haal vriendenlijst op van de Steam API.

        Argumenten:
        steam_id (str): Steam ID.

        Returns:
        list: Lijst van vrienden met details.
    """
    # Stel de URL en parameters in voor de API-aanroep
    url = "https://api.steampowered.com/ISteamUser/GetFriendList/v0001"
    params = {"key": API_KEY, "steamid": steam_id, "relationship": "friend" }

    # Voer de API-aanroep uit en controleer de status code van de response
    response = requests.get(url, params=params)
    if response.status_code != 200 or 'friendslist' not in response.json():
        raise Exception(f"Mislukt om vriendenlijst op te halen: {response.status_code}")

    # Haal de vriendenlijst op uit de response
    friends = response.json()['friendslist']['friends']
    friend_ids = [friend['steamid'] for friend in friends]

    # Haal de weergavenamen van de vrienden op
    friend_info = get_friend_info(friend_ids)

    # Return een lijst van vrienden met details
    return [
        {
            'steamid': friend['steamid'],
            'display_name': friend_info.get(friend['steamid'], {}).get('personaname', "Unknown"),
            'avatar': friend_info.get(friend['steamid'], {}).get('avatar', ""),
            'relationship': friend['relationship'],
            'friend_since': friend['friend_since']
        }
        for friend in friends
    ]


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
        print(f"Mislukt om bezeten spellen op te halen: {response.status_code}")
        return []

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
            'url_avatar': own_game_dict[game_id]['url_avatar'],
            'name': own_game_dict[game_id]['name'],
            'own_playtime': own_game_dict[game_id].get('playtime_forever', 0),
            'friend_playtime': friend_game_dict[game_id].get('playtime_forever', 0)
        }
        for game_id in own_game_dict if game_id in friend_game_dict
    ]


def get_recent_playtime(steam_id: str):
    """
        Haal recent gespeelde spellen op van de Steam API.

        Argumenten:
        steam_id (str): Steam ID.

        Returns:
        list: Lijst van recent gespeelde spellen met speeltijden.
    """

    # Stel de URL en parameters in voor de API-aanroep
    url = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/"
    params = { "key": API_KEY, "steamid": steam_id, "format": "json"}

    # Voer de API-aanroep uit en controleer de status code van de response
    responses = requests.get(url, params=params)
    data = responses.json()
    if responses.status_code != 200 or 'response' not in responses.json():
        print(f"Mislukt om recent gespeelde spellen op te halen: {responses.status_code}")
        return []

    # Haal de spellenlijst op uit de response
    if "games" in data["response"]:
        games = data["response"]["games"]
        total_playtime_2weeks = round((sum(game['playtime_2weeks'] for game in games) / 60), 2)
        sorted_games = sorted([
            {
                'name': game['name'],
                'appid': game['appid'],
                'url_avatar': game['img_icon_url'],
                'playtime_2weeks': round((game['playtime_2weeks']) / 60, 2)
            }
            for game in games
        ], key=lambda game: game['playtime_2weeks'], reverse=True)
        return {
            'total_playtime_2weeks': total_playtime_2weeks,
            'games': sorted_games
        }
    else:
        return {
            'total_playtime_2weeks': 0,
            'games': [],
            'url_avatar': ""
        }


def get_user_profile(steam_id: str = None, incl_friends: bool = False, incl_games: bool = False):
    """
        Maakt een userprofile aan.

        Argumenten:
        steam_id (str): Steam ID.

        Returns:
        dict: Gebruikersprofiel.
    """
    # Haal de spelersgegevens op van de Steam API
    player_data = get_player_summary(steam_id)

    # Controleer of de vriendenlijst moet worden opgenomen
    if not incl_friends and not incl_games:
        # Maak een dict van het gebruikersprofiel
        profile =  UserProfile(
            steam_id=player_data['steamid'],
            display_name=player_data['personaname'],
            url_avatar_small=player_data['avatar'],
            url_avatar_medium=player_data['avatarmedium'],
            url_avatar_full=player_data['avatarfull'],
            url_profile=player_data['profileurl'],
        )
        return profile

    # Haal de vriendenlijst op van de Steam API
    try:
        friend_list = get_friend_list(steam_id)
    except Exception as e:
        friend_list = []
        print(f'Fout: {e}, vriendenlijst mogelijk op prive. Vriendenlijst is leeg: {friend_list}')

    # Controleer of de spellenlijst moet worden opgenomen
    if incl_games:
        # Haal de spellenlijst op van de Steam API
        try:
            game_list = get_owned_games(steam_id)
        except Exception as e:
            game_list = []
            print(f'Fout: {e}, vriendenlijst mogelijk op prive. Vriendenlijst is leeg: {friend_list}')

        # Maak een dict van het gebruikersprofiel
        profile = UserProfile(
            steam_id=player_data['steamid'],
            display_name=player_data['personaname'],
            url_avatar_small=player_data['avatar'],
            url_avatar_medium=player_data['avatarmedium'],
            url_avatar_full=player_data['avatarfull'],
            url_profile=player_data['profileurl'],
            friend_list=friend_list,
            game_list=game_list
        )
        return profile

    # Maak een dict van het gebruikersprofiel
    profile = UserProfile(
        steam_id=player_data['steamid'],
        display_name=player_data['personaname'],
        url_avatar_small=player_data['avatar'],
        url_avatar_medium=player_data['avatarmedium'],
        url_avatar_full=player_data['avatarfull'],
        url_profile=player_data['profileurl'],
        friend_list=friend_list,
    )
    return profile