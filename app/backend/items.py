class Item:
    def __init__(self, name, price, description, category):
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.date_created = None


class Vinyl(Item):
    def __init__(self, name, price, description, category, artist, album, cover_art, release_date):
        super().__init__(name,price, description, category)
        self.artist = artist
        self.album = album
        self.cover_art = cover_art
        self.release_date = release_date
        self.date_created = None

