import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")

def fetch_games():
    url = "https://api.rawg.io/api/games"
    all_games = []
    page = 1

    while page <= 25:
        print(f"Fetching page {page}...")

        params = {
            "key": API_KEY,
            "ordering": "-rating",
            "page_size": 40,
            "page": page
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code}")
            break

        data = response.json()

        for game in data["results"]:
            genres = ", ".join([g["name"] for g in game.get("genres", [])])
            platforms = ", ".join([p["platform"]["name"] for p in game.get("platforms", [])])

            # Extract singleplayer/multiplayer from tags
            tags = [t["name"].lower() for t in game.get("tags", [])]
            if "singleplayer" in tags and "multiplayer" in tags:
                play_mode = "Both"
            elif "multiplayer" in tags:
                play_mode = "Multiplayer"
            elif "singleplayer" in tags:
                play_mode = "Singleplayer"
            else:
                play_mode = "Unknown"

            all_games.append({
                "name": game["name"],
                "rating": game["rating"],
                "released": game["released"],
                "genres": genres,
                "platforms": platforms,
                "metacritic": game.get("metacritic", "N/A"),
                "playtime": game.get("playtime", "N/A"),
                "play_mode": play_mode,
            })

        page += 1

    with open("data/games.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_games[0].keys())
        writer.writeheader()
        writer.writerows(all_games)

    print(f"Done! Saved {len(all_games)} games to data/games.csv")

fetch_games()