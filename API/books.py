import requests
from dotenv import load_dotenv

load_dotenv()

def searchBooks(book_name):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{book_name}",
        "maxResults": 25,
        "fields": "items(volumeInfo/title,volumeInfo/authors,volumeInfo/description,volumeInfo/imageLinks/thumbnail)"
        #fields gerbuiken om de api te versnellen zodat we alleen de data da we nodig hebben opvragen. verbetering van 2seconden
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        books = [
            {
                "title": book.get("volumeInfo", {}).get("title"),
                "authors": book.get("volumeInfo", {}).get("authors", []),
                "description": book.get("volumeInfo", {}).get("description"),
                "imageLinks": {"thumbnail": book.get("volumeInfo", {}).get("imageLinks", {}).get("thumbnail")}
            }
            for book in data.get("items", [])
        ]
        return books
