import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")

def fetch_games(ordering, output_file, metacritic_only=False):
    url = "https://api.rawg.io/api/games"
    all_games = []
    page = 1

    while page <= 25:
        print(f"Fetching {output_file} - page {page}...")

        params = {
            "key": API_KEY,
            "ordering": ordering,
            "page_size": 40,
            "page": page,
            "exclude_additions": True
        }

        if metacritic_only:
            params["metacritic"] = "1,100"

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code}")
            break

        data = response.json()

        for game in data["results"]:
            genres = ", ".join([g["name"] for g in game.get("genres", []) or []])
            platforms = ", ".join([p["platform"]["name"] for p in game.get("platforms", []) or []])
            tags = [t["name"].lower() for t in game.get("tags", []) or []]
            genres_list = [g["name"].lower() for g in game.get("genres", []) or []]

            is_multiplayer = (
                "multiplayer" in tags or
                "massively multiplayer" in genres_list or
                "co-op" in tags or
                "online co-op" in tags or
                "pvp" in tags
            )
            is_singleplayer = (
                "singleplayer" in tags or
                "single-player" in tags
            )

            if is_singleplayer and is_multiplayer:
                play_mode = "Both"
            elif is_multiplayer:
                play_mode = "Multiplayer"
            elif is_singleplayer:
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

    with open(f"data/{output_file}", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_games[0].keys())
        writer.writeheader()
        writer.writerows(all_games)

    print(f"Done! Saved {len(all_games)} games to data/{output_file}")

# Fetch top 1000 by RAWG community rating
fetch_games(
    ordering="-rating",
    output_file="games_rated.csv"
)

# Fetch top 1000 by Metacritic score (all have metacritic scores)
fetch_games(
    ordering="-metacritic",
    output_file="games_metacritic.csv",
    metacritic_only=True
)