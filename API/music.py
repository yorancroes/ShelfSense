import requests

BASE_URL = 'https://ws.audioscrobbler.com/2.0/'
PARAMS = {
    'method': 'album.search',
    'album': 'believe',
    'api_key': "API_KEY"
}