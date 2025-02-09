import os
import requests
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()
MY_API_KEY = os.getenv("GAMES_API_KEY")

BASE_URL = "https://www.giantbomb.com/api"
HEADERS = {"User-Agent": "YourAppName"}


def get_game_details(game_id):
    params = {
        "api_key": MY_API_KEY,
        "format": "json"
    }
    response = requests.get(f"{BASE_URL}/game/{game_id}/", params=params, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("results", {})
    return {}


def search_games(game_name):
    params = {
        "api_key": MY_API_KEY,
        "format": "json",
        "query": game_name,
        "resources": "game"
    }
    response = requests.get(f"{BASE_URL}/search/", params=params, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        games = []
        game_ids = {item["id"]: item for item in data.get("results", []) if "id" in item}

        # Parallel details ophalen
        with concurrent.futures.ThreadPoolExecutor() as executor:
            game_details_map = {game_id: executor.submit(get_game_details, game_id) for game_id in game_ids}

        for game_id, item in game_ids.items():
            game_details = game_details_map[game_id].result()  # Resultaat ophalen van toekomstige taak
            games.append({
                "name": item.get("name"),
                "platforms": [platform["name"] for platform in item.get("platforms", [])] if item.get(
                    "platforms") else [],
                "release_date": item.get("original_release_date"),
                "developer": [dev["name"] for dev in game_details.get("developers", [])] if game_details.get(
                    "developers") else ["Unknown"],
                "publisher": [pub["name"] for pub in game_details.get("publishers", [])] if game_details.get(
                    "publishers") else ["Unknown"],
                "cover_image": item.get("image", {}).get("original_url")
            })

        return games
