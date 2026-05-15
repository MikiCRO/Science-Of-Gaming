import requests
import os
from dotenv import load_dotenv
import json

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")

def fetch_top_games():
    url = "https://api.rawg.io/api/games"
    params = {
        "key": API_KEY,
        "ordering": "-rating",
        "page_size": 20
    }

    response = requests.get(url, params=params)
    data = response.json()

    for game in data["results"]:
        print(f"{game['name']} | Rating: {game['rating']} | Released: {game['released']}")

fetch_top_games()