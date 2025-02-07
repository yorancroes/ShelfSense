import sys

import requests
from dotenv import load_dotenv


load_dotenv()

def searchBooks(book_name):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = { #voegt de nodige filters toe aan de url
        "q": f"intitle:{book_name}",
        "maxResults": 30
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200: #status 200 betekent dat de api-call succesvol was.
        data = response.json()
        volume_info = [book.get("volumeInfo", {}) for book in data.get("items", [])] #we steken eerst de rauwe data in een lijst
        #We filteren nu onze rauwe lijst en steken enkel data dat we effectief nodig hebben in onze definiteive lijst van boeken
        books = [
            {
                "title": book.get("title"),
                "authors": book.get("authors", []),
                "description": book.get("description"),
                "imageLinks": {"thumbnail": book.get("imageLinks", {}).get("thumbnail")}
            }
            for book in volume_info
        ]
        return books

books = searchBooks("harry potter")
for book in books:
    print(book["imageLinks"])