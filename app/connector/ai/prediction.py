import requests
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = "B6B4AC430AB9229F3E35F0DD9FF510CE"
BASE_URL = "https://api.steampowered.com"

def get_friends(steam_id):
    url = f"{BASE_URL}/ISteamUser/GetFriendList/v1/"
    params = {"key": API_KEY, "steamid": steam_id, "relationship": "friend"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [friend["steamid"] for friend in data.get("friendslist", {}).get("friends", [])]
    else:
        return []

def get_user_summary(steam_ids):
    url = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {"key": API_KEY, "steamids": ",".join(steam_ids)}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("response", {}).get("players", [])
    else:
        return []

def calculate_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(x[i] ** 2 for i in range(n))

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n

    return slope, intercept

def visualize_creation_dates_with_regression(root_id, file_name):
    print("Vrienden ophalen...")
    friends = get_friends(root_id)
    print(f"{len(friends)} vrienden gevonden voor gebruiker {root_id}.")

    creation_dates = []

    print('vrienden van vrienden ophalen...')

    friends_data = get_user_summary(friends[:20])
    for friend in friends_data:
        if "timecreated" in friend:
            creation_dates.append(friend["timecreated"])


    for friend_id in friends[:20]:
        second_level_friends = get_friends(friend_id)
        second_level_data = get_user_summary(second_level_friends[:40])
        for friend in second_level_data:
            if "timecreated" in friend:
                creation_dates.append(friend["timecreated"])

    for second_level_id in friends[:20]:
        third_level_friends = get_friends(second_level_id)
        third_level_data = get_user_summary(third_level_friends[:20])
        for friend in third_level_data:
            if "timecreated" in friend:
                creation_dates.append(friend["timecreated"])

    creation_dates.sort()

    creation_dates_dt = [datetime.utcfromtimestamp(ts) for ts in creation_dates]
    creation_dates_numeric = [(dt.timestamp() - creation_dates[0]) / (365 * 24 * 60 * 60) for dt in creation_dates_dt]

    x = creation_dates_numeric
    y = list(range(1, len(creation_dates) + 1))

    slope, intercept = calculate_regression(x, y)
    regression_line = [slope * xi + intercept for xi in x]

    print(f"Voorspelling: {round(slope, 2)} accounts worden aangemaakt in een jaar.")

    plt.figure(figsize=(14, 8))
    plt.scatter(creation_dates_dt, y, color="blue", label="Accounts", alpha=0.7)
    plt.plot(creation_dates_dt, regression_line, color="red", linestyle="--", label=f"Lineaire regressie (voorspelling: {round(slope, 2)} accounts/jaar)")
    plt.xlabel("Account aanmaakdatum")
    plt.ylabel("Aantal accounts")
    plt.title("Lineaire Regressie: Steam Account Aanmaakdata")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f'static/images/{file_name}.png', dpi=300, bbox_inches='tight')
    return round(slope, 2)

