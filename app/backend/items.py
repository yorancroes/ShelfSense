from _pyrepl import console
from app.Database.database_scripts.connect import connect_db

class Item:
    def __init__(self, user_id, name, price, description, category):
        self.user_id = user_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.date_created = None


class Vinyl(Item):
    def __init__(self, user_id, name, price, description, category, artist, album, cover_art, release_date):
        super().__init__(user_id, name, price, description, category)
        self.artist = artist
        self.album = album
        self.cover_art = cover_art
        self.release_date = release_date
        self.date_created = None

class Game(Item):
    def __init__(self, user_id, name, price, description, category, publisher, cover_art, release_date, platform):
        super().__init__(user_id, name, price, description, category)
        self.publisher = publisher
        self.cover_art = cover_art
        self.release_date = release_date
        self.platform = platform
        self.date_created = None

class Book(Item):
    def __init__(self, user_id, name, price, description, category, author, publisher, cover_art, release_date):
        super().__init__(user_id, name, price, description, category)
        self.author = author
        self.publisher = publisher
        self.cover_art = cover_art
        self.release_date = release_date
        self.date_created = None

