import requests
from dotenv import load_dotenv


load_dotenv()

def searchBooks(book_name):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{book_name}",
        "maxResults": 30
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        volume_info = [book.get("volumeInfo", {}) for book in data.get("items", [])]
        books = [
            {
                "title": book.get("title"),
                "authors": book.get("authors"),
                "description": book.get("description"),
                "imageLinks": {"thumbnail": book.get("imageLinks", {}).get("thumbnail")}
            }
            for book in volume_info
        ]
        return books


books = searchBooks("Harry Potter")
for book in books:
    print(book)