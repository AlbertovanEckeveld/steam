import requests

from app.connector import get_steam_API

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


def get_player_displayname(steam_id):
    return get_player_summary(steam_id)['response']['players'][0]['personaname']


def get_friend_list(steam_id):
    url = "https://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "relationship": "friend"
    }

    response = requests.get(url, params=params)
    friends_list = [
        {
            'steamid': friend['steamid'],
            'display_name': get_player_displayname(friend['steamid']),
            'relationship': friend['relationship'],
            'friend_since': friend['friend_since']
        }
        for friend in response.json()['friendslist']['friends']
    ]

    # Voorbeeld over de output:
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

"""
def get_play_time(steam_id):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "include_appinfo": 1,
        "include_played_free_games": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    totaalAantalGespeeldeMinuten = 0


    games = data.get('response', {}).get('games', [])

    #Check of de lijst niet leeg is
    if not games:
        print("Geen games gevonden of een fout is opgetreden.")
        return

    for game in games:
        gameNaam = game.get('name', 'Onbekende game')
        speeltijdMinuten = game.get('playtime_forever', 0)
        speeltijdUren = speeltijdMinuten / 60
        totaalAantalGespeeldeMinuten += speeltijdMinuten
        print(f"Game: {gameNaam}, Speeltijd: {speeltijdUren:.2f} uur")


    totaalAantalGespeeldeUren = totaalAantalGespeeldeMinuten / 60
    print(f"Totaal aantal uren gespeeld: {totaalAantalGespeeldeUren:.2f} uur")


get_play_time('76561198273359778')

"""