import requests

from app.connector import get_steam_API

# "B6B4AC430AB9229F3E35F0DD9FF510CE"

API_KEY = get_steam_API()

def get_player_summary(steam_id):
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        "key": API_KEY,
        "steamids": steam_id
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")


def get_friend_list(steam_id):
    url = "https://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "relationship": "friend"
    }

    response = requests.get(url, params=params)
    return response.json()



