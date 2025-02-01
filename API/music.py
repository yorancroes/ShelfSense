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
        'limit': 30
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        albums = data.get("results", {}).get("albummatches", {}).get("album", []) #we steken de ongefilterde data in een eerste lijst
        #we filteren de data zodat we enkel de nodige informatie eruithalen en in onze definiteive lijst steken
        albums_filtered = [
            {
                "name": album.get("title"),
                "artist": album.get("artist"),
                "image": {
                    "large": next((image.get("#text") for image in album.get("image", []) if image.get("size") == "large"), None)
                }
            }
            for album in albums
        ]
        return albums_filtered #we geven de gefilterde definitieve lijst terug als output van de functie

albums = searchMusic("Thriller")
for album in albums:
    print(album)

#response structuur voor referentie
#name: "AlBUM_Name" | artist: "ARTIST_Name" | image: [...{'text': "URL_IMAGE", 'size' : "medium"}...]