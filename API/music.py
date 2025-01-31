import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
MY_API_KEY = os.getenv("API_KEY")
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'
PARAMS = {
    'method': 'album.search',
    'album': 'believe',
    'api_key': MY_API_KEY,
    'format': 'json',
    'limit': 30
}

response = requests.get(BASE_URL, params=PARAMS)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f'Error: {response.status_code}')



albums = data['results']['albummatches']['album']
album_name = next((album['name'] for album in albums if album['name'] == "Believe"), None)
artist_name = next((album['artist'] for album in albums if album['artist'] == "Justin Bieber"), None)
image_url = next(
    (img['#text'] for album in albums if album['artist'] == "Justin Bieber" for img in album['image'] if img['size'] == "large"),
    None
)

print(f"{album_name} - {artist_name} - {image_url}")


#response structuur
#name: "AlBUM_Name" | artist: "ARTIST_Name" | image: [...{'text': "URL_IMAGE", 'size' : "medium"}...]