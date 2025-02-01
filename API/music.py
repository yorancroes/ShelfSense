import json
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
        print(data)
    else:
        print(f'Error: {response.status_code}')
    albums = data['results']['albummatches']['album']
    album_name = next((album['name'] for album in albums if album['name'] == album_name), None)
    artist_name = next((album['artist'] for album in albums if album['name'] == album_name), None)
    image_url = next(
        (img['#text'] for album in albums if album['name'] == album_name for img in album['image'] if
         img['size'] == "large"),
        None
    )
    print(f"{album_name} - {artist_name} - {image_url}")

searchMusic('Thriller')


#response structuur voor referentie
#name: "AlBUM_Name" | artist: "ARTIST_Name" | image: [...{'text': "URL_IMAGE", 'size' : "medium"}...]