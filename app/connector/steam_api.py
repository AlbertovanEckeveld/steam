import requests

from app.connector import get_steam_API

API_KEY = get_steam_API()


def get_player_summary(steam_id):
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"

    if isinstance(steam_id, list):
        steam_id = ",".join(steam_id)
    elif not isinstance(steam_id, str):
        raise ValueError("steam_id must be a string or a list of strings.")

    params = {
        "key": API_KEY,
        "steamids": steam_id
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")


def get_player_displayname(steam_id):
    player_data = get_player_summary(steam_id)
    players = player_data.get('response', {}).get('players', [])

    if isinstance(steam_id, str):
        return players[0]['personaname'] if players else None
    elif isinstance(steam_id, list):
        return [player['personaname'] for player in players]
    else:
        raise ValueError("steam_id must be a string or a list of strings.")


def get_friend_list(steam_id):
    url = "https://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "relationship": "friend"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200 or 'friendslist' not in response.json():
        raise Exception(f"Failed to fetch friends list: {response.status_code}")

    friends = response.json()['friendslist']['friends']

    friend_ids = [friend['steamid'] for friend in friends]

    player_data = get_player_summary(friend_ids)
    players = player_data.get('response', {}).get('players', [])

    steamid_to_displayname = {player['steamid']: player['personaname'] for player in players}

    friends_list = [
        {
            'steamid': friend['steamid'],
            'display_name': steamid_to_displayname.get(friend['steamid'], "Unknown"),
            'relationship': friend['relationship'],
            'friend_since': friend['friend_since']
        }
        for friend in friends
    ]

    # {'steamid': '76561198033737398', 'relationship': 'friend', 'friend_since': 1509471831}

    # Voorbeeld van de output:
    # [
    #   {'steamid': '76561198033737398', 'display_name': 'AlbertoVE', 'relationship': 'friend', 'friend_since': 1509471831},
    #   {'steamid': '76561198033737398', 'display_name': 'AlbertoVE', 'relationship': 'friend', 'friend_since': 1509471831}
    # ]

    return friends_list


def get_owned_games(steam_id):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "include_appinfo": 1,
        "include_played_free_games": 1
    }

    response = requests.get(url, params=params)
    game_list = [
        {
            'appid': game['appid'],
            'name': game['name'],
            'playtime_forever': round((game['playtime_forever'] / 60), 2)
        }
        for game in response.json()['response']['games']
    ]

    return sorted(game_list, key=lambda game: game['playtime_forever'], reverse=True)