from _pyrepl import console
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from app.Database.database_scripts.connect import connect_db
from abc import ABC, abstractmethod
import requests


class Item(ABC):
    def __init__(self, user_id, name, price, description, category):
        self.user_id = user_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.date_created = None

        @abstractmethod
        def load(self):
            pass



class Vinyl(Item):
    def __init__(self, Api_Dict, id=None):
        self.Api_Dict = Api_Dict
        self.title = self.Api_Dict['name']
        self.artist = self.Api_Dict['artist']
        self.image_url = self.Api_Dict['image']
        self.id = id

    def upload(self, user_id):
        query = """
        INSERT INTO vinyls (user_id, album, artist, image_path)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, self.title, self.artist, self.image_url))
                self.id = cursor.fetchone()[0]
                conn.commit()
                print(f"Vinyl inserted with ID: {self.id}")
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.close()

    def load(self, label: QLabel):

        response = requests.get(self.image_url)

        if response.status_code == 200:
            # Save the image to a temporary file
            with open("temp_image.jpg", "wb") as file:
                file.write(response.content)

        if label is not None:
            pixmap = QPixmap("temp_image.jpg")
            if pixmap.isNull():
                print("Failed to load pixmap")
            else:
                label.setPixmap(pixmap)
                label.setScaledContents(True)
                print("Pixmap set successfully")




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


def load_vinyls(user_id):
    vinyls = []
    query = "SELECT id, album, artist, image_path FROM vinyls WHERE user_id = %s;"
    conn = connect_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()  # Get all records

            for row in results:
                vinyl_id, album, artist, image_path = row
                api_dict = {'name': album, 'artist': artist, 'image': image_path}
                vinyl = Vinyl(api_dict, id=vinyl_id)
                vinyls.append(vinyl)

    except Exception as e:
        print(f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()

    return vinyls
