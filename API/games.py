import os
import requests
from dotenv import load_dotenv

load_dotenv()
MY_API_KEY = os.getenv("GAMES_API_KEY")


BASE_URL = "https://www.giantbomb.com/api"
HEADERS = {"User-Agent": "YourAppName"}


def get_game_details(game_id):
    #we moeten bij deze api een aparte game details call aanmaken om de developer en publisher te krijgen.
    #dit is een vereiste omdat tijdens mijn testen de api geen developer en publisher teruggeeft als we geen call doen op een id voor de details.
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
        for item in data.get("results", []): #voor elke entry doen we een dubbele call voor de developer en publisher info te krijgen
            game_id = item.get("id")
            game_details = get_game_details(game_id) if game_id else {}
            game_info = {
                "name": item.get("name"),
                "platforms": [platform["name"] for platform in item.get("platforms", [])] if item.get(
                    "platforms") else [],
                "release_date": item.get("original_release_date"),
                "developer": [dev["name"] for dev in game_details.get("developers", [])] if game_details.get(
                    "developers") else ["Unknown"],
                "publisher": [pub["name"] for pub in game_details.get("publishers", [])] if game_details.get(
                    "publishers") else ["Unknown"],
                "cover_image": item.get("image", {}).get("original_url")
            }
            games.append(game_info)
        return games #we combineren beide info van beide calls en steken ze in de games list

