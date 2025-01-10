import json
import matplotlib.pyplot as plt
import datetime

def gemiddelde(data):
    return sum(data) / len(data)

with open('steam.json', 'r') as file:
    games = json.load(file)

filtered_games = [game for game in games if 'Adventure' in game['genres'] and 150 <= (game['positive_ratings'] + game['negative_ratings']) <= 100000]

filtered_games = [game for game in filtered_games if datetime.datetime.strptime(game['release_date'], '%Y-%m-%d').year >= 2007]

release_dates = [datetime.datetime.strptime(game['release_date'], '%Y-%m-%d') for game in filtered_games]
review_counts = [game['positive_ratings'] + game['negative_ratings'] for game in filtered_games]

gem_reviews = gemiddelde(review_counts)

gmean_release_date = datetime.datetime.fromtimestamp(gemiddelde([date.timestamp() for date in release_dates]))

plt.figure(figsize=(10, 6))
plt.scatter(release_dates, review_counts, color='blue', label='Games')
plt.axhline(gem_reviews, color='red', linestyle='dashed', linewidth=2.5, label=f"Gemiddelde reviews: {gem_reviews:.2f}")
plt.axvline(gmean_release_date, color='green', linestyle='dashed', linewidth=2.5, label=f"Gemiddelde release datum: {gmean_release_date.strftime('%Y-%m-%d')}")
plt.xlabel('Release Datum (Adventure games)')
plt.ylabel('Aantal Reviews')
plt.title('release datum vs aantal reviews voor Adventure games')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.yticks(range(0, max(review_counts) + 10000, 10000))
plt.savefig(f'../../static/images/gemiddelde.png', dpi=300, bbox_inches='tight')
