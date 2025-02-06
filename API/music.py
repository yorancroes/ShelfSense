import os
import requests
from dotenv import load_dotenv

load_dotenv()
MY_API_KEY = os.getenv("API_KEY")


def searchMusic(album_name):
    base_url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'album.search',
        'album': album_name,
        'api_key': MY_API_KEY,
        'format': 'json',
        'limit': 8
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        albums = data.get("results", {}).get("albummatches", {}).get("album",
                                                                     [])  # We steken de ongefilterde data in een eerste lijst

        # Print the raw album data for debugging

        # We filteren de data zodat we enkel de nodige informatie eruithalen en in onze definitive lijst steken
        albums_filtered = [
            {
                "name": album.get("name"),  # Check if the title key exists
                "artist": album.get("artist"),
                "image": next((image.get("#text") for image in album.get("image", []) if image.get("size") == "large"),
                              None)
            }
            for album in albums
        ]

        # Print filtered album data for debuggin

        return albums_filtered
