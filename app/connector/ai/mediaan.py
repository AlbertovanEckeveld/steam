import json
import matplotlib.pyplot as plt

def median(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2

    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]

with open('steam.json', 'r') as file:
    games = json.load(file)

action_games = [game for game in games if 'Action' in game['genres'] and float(game['price']) <= 70 and game['positive_ratings'] <= 50000 and 100 <= game['average_playtime'] <= 30000]

prices = [float(game['price']) for game in action_games]
average_playtime = [game['average_playtime'] for game in action_games]

median_price = median(prices)
median_playtime = median(average_playtime)

plt.figure(figsize=(10, 6))
plt.scatter(prices, average_playtime, color='blue', label='Games')
plt.axvline(median_price, color='green', linestyle='dashed', linewidth=1, label=f'Mediaan Prijs: {median_price:.2f}')
plt.axhline(median_playtime, color='red', linestyle='dashed', linewidth=1, label=f'Mediaan Speeltijd (minuten): {median_playtime:.2f}')
plt.xlabel('Prijs')
plt.ylabel('Gemiddelde Speeltijd (minuten)')
plt.title('prijs vs gemiddelde speeltijd voor genre "Action"')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f'../../static/images/mediaan.png', dpi=300, bbox_inches='tight')
