from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
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

class VinylCard(QFrame):
    def __init__(self, vinyl, parent=None):
        super().__init__(parent)
        self.setObjectName("vinylCard")
        self.setFixedSize(160, 220)  # Made overall card smaller
        self.setStyleSheet("""
            #vinylCard {
                background-color: transparent;  # Removed white background
                border-radius: 8px;
                padding: 8px;
                margin: 5px;
            }
            QLabel {
                color: #333333;
                background-color: transparent;  # Ensure labels are also transparent
            }
        """)

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)  # Reduced margins
        layout.setSpacing(2)  # Reduced spacing between elements

        # Image
        self.image_label = QLabel()
        self.image_label.setFixedSize(140, 140)  # Made image smaller
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.load_image(vinyl.image_url)
        layout.addWidget(self.image_label)

        # Album name
        name_label = QLabel(vinyl.name)
        name_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 13px;
        """)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)

        # Artist
        artist_label = QLabel(vinyl.artist)
        artist_label.setStyleSheet("""
            color: #666666; 
            font-size: 11px;
        """)
        artist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(artist_label)

        # Add stretch to push everything to the top
        layout.addStretch()

    def load_image(self, image_url):
        try:
            if image_url:
                # Try to download the image if it's a URL
                if image_url.startswith(('http://', 'https://')):
                    response = requests.get(image_url, timeout=5)
                    if response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(response.content)
                        self.image_label.setPixmap(pixmap)
                else:
                    # Try to load as local file
                    pixmap = QPixmap(image_url)
                    if not pixmap.isNull():
                        self.image_label.setPixmap(pixmap)
                    else:
                        self.set_placeholder_image()
            else:
                self.set_placeholder_image()
        except Exception as e:
            print(f"Error loading image: {e}")
            self.set_placeholder_image()

    def set_placeholder_image(self):
        # Create a basic placeholder with album icon
        self.image_label.setText("🎵")
        self.image_label.setStyleSheet("QLabel { background-color: #f0f0f0; font-size: 48px; }")


class Vinyl(Item):
    def __init__(self, Api_Dict, id=None):
        self.Api_Dict = Api_Dict
        self.name = self.Api_Dict['name']
        self.artist = self.Api_Dict['artist']
        self.image_url = self.Api_Dict['image']
        self.description = self.Api_Dict['description']
        self.id = id

    def upload(self, user_id):
        query = """
        INSERT INTO vinyls (user_id, album, artist, image_path, description)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, self.name, self.artist, self.image_url, self.description))
                self.id = cursor.fetchone()[0]
                conn.commit()
                print(f"Vinyl inserted with ID: {self.id}")
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.close()

    def load(self, grid_layout, row, col):
        """Loads vinyl into the provided grid layout at specified position."""
        try:
            vinyl_card = VinylCard(self)
            grid_layout.addWidget(vinyl_card, row, col, Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            print(f"Error while loading vinyl: {e}")


def load_vinyls(user_id):
    vinyls = []
    query = "SELECT id, album, artist, image_path, description FROM vinyls WHERE user_id = %s;"
    conn = connect_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            for row in results:
                vinyl_id, album, artist, image_path, description = row
                api_dict = {
                    'name': album,
                    'artist': artist,
                    'image': image_path,
                    'description': description
                }
                vinyl = Vinyl(api_dict, id=vinyl_id)
                vinyls.append(vinyl)

    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

    return vinyls

class Game(Item):
    def __init__(self, Api_Dict, id=None):
        super().__init__(
            user_id=None,  # You'll need to pass the correct user_id if available
            name=Api_Dict['name'],
            price=None,  # Games might not have a price, adjust as needed
            description=Api_Dict['description'],
            category="game"
        )
        self.Api_Dict = Api_Dict
        self.publisher = Api_Dict['publisher']
        self.image_url = Api_Dict['image']
        self.id = id

    def upload(self, user_id):
        query = """
        INSERT INTO games (user_id, name, publisher, image_path, description)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, self.name, self.publisher, self.image_url, self.description))
                self.id = cursor.fetchone()[0]
                conn.commit()
                print(f"Vinyl inserted with ID: {self.id}")
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.close()

    def load(self, grid_layout, row, col):
        try:
            game_card = GameCard(self)
            grid_layout.addWidget(game_card, row, col, Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            print(f"Error while loading vinyl: {e}")



class GameCard(QFrame):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.setObjectName("GameCard")
        self.setFixedSize(160, 220)  # Made overall card smaller
        self.setStyleSheet("""
            #vinylCard {
                background-color: transparent;  # Removed white background
                border-radius: 8px;
                padding: 8px;
                margin: 5px;
            }
            QLabel {
                color: #333333;
                background-color: transparent;  # Ensure labels are also transparent
            }
        """)

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)  # Reduced margins
        layout.setSpacing(2)  # Reduced spacing between elements

        # Image
        self.image_label = QLabel()
        self.image_label.setFixedSize(140, 140)  # Made image smaller
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.load_image(game.image_url)
        layout.addWidget(self.image_label)

        # Album name
        name_label = QLabel(game.name)
        name_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 13px;
        """)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)

        # Artist
        artist_label = QLabel(game.publisher)
        artist_label.setStyleSheet("""
            color: #666666; 
            font-size: 11px;
        """)
        artist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(artist_label)

        # Add stretch to push everything to the top
        layout.addStretch()

    def load_image(self, image_url):
        try:
            if image_url:
                # Try to download the image if it's a URL
                if image_url.startswith(('http://', 'https://')):
                    response = requests.get(image_url, timeout=5)
                    if response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(response.content)
                        self.image_label.setPixmap(pixmap)
                else:
                    # Try to load as local file
                    pixmap = QPixmap(image_url)
                    if not pixmap.isNull():
                        self.image_label.setPixmap(pixmap)
                    else:
                        self.set_placeholder_image()
            else:
                self.set_placeholder_image()
        except Exception as e:
            print(f"Error loading image: {e}")
            self.set_placeholder_image()


    def set_placeholder_image(self):
        # Create a basic placeholder with album icon
        self.image_label.setText("🎵")
        self.image_label.setStyleSheet("QLabel { background-color: #f0f0f0; font-size: 48px; }")

class Book(Item):
    def __init__(self, Api_Dict, id=None):
        self.Api_Dict = Api_Dict
        print(Api_Dict)
        self.name = Api_Dict['title']
        self.authors = Api_Dict['author']


        self.image_url = Api_Dict['imageLinks']
        self.description = Api_Dict['description']
        self.id = id

    def upload(self, user_id):

        print("uplaod called")
        query = """
        INSERT INTO books (user_id, name, author, description, image_path)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, self.name, self.authors, self.description, self.image_url))
                self.id = cursor.fetchone()[0]
                conn.commit()
                print(f"Book inserted with ID: {self.id}")
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.close()

    def load(self, grid_layout, row, col):
        try:
            book_card = BookCard(self)
            grid_layout.addWidget(book_card, row, col, Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            print(f"Error while loading book: {e}")


class BookCard(QFrame):
    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.setObjectName("BookCard")
        self.setFixedSize(160, 220)  # Made overall card smaller
        self.setStyleSheet("""
            #vinylCard {
                background-color: transparent;  # Verwijderd witte achtergond
                border-radius: 8px;
                padding: 8px;
                margin: 5px;
            }
            QLabel {
                color: #333333;
                background-color: transparent;  # Maakt label ook transparant
            }
        """)

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)  # Reduced margins
        layout.setSpacing(2)  # Reduced spacing between elements

        # Image
        self.image_label = QLabel()
        self.image_label.setFixedSize(140, 140)  # Made image smaller
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.load_image(book.image_url)
        layout.addWidget(self.image_label)

        # Album name
        name_label = QLabel(book.name)
        name_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 13px;
        """)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)

        # Artist
        artist_label = QLabel(book.authors)
        artist_label.setStyleSheet("""
            color: #666666; 
            font-size: 11px;
        """)
        artist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(artist_label)

        # Add stretch to push everything to the top
        layout.addStretch()

    def load_image(self, image_url):
        try:
            if image_url:
                # Try to download the image if it's a URL
                if image_url.startswith(('http://', 'https://')):
                    response = requests.get(image_url, timeout=5)
                    if response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(response.content)
                        self.image_label.setPixmap(pixmap)
                else:
                    # Try to load as local file
                    pixmap = QPixmap(image_url)
                    if not pixmap.isNull():
                        self.image_label.setPixmap(pixmap)
                    else:
                        self.set_placeholder_image()
            else:
                self.set_placeholder_image()
        except Exception as e:
            print(f"Error loading image: {e}")
            self.set_placeholder_image()


    def set_placeholder_image(self):
        # Create a basic placeholder with album icon
        self.image_label.setText("🎵")
        self.image_label.setStyleSheet("QLabel { background-color: #f0f0f0; font-size: 48px; }")


def load_items(user_id, item_type='vinyl'):
    items = []
    if item_type == 'vinyl':
        query = "SELECT id, album, artist, image_path, description FROM vinyls WHERE user_id = %s;"
    elif item_type == 'game':
        query = "SELECT id, name, publisher, image_path, description FROM games WHERE user_id = %s;"
    elif item_type == 'book':
        query = "SELECT id, name, author, image_path, description FROM books WHERE user_id = %s;"
    else:
        raise ValueError("Invalid item type")

    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            print(f"Fetched {len(results)} {item_type}(s) from the database")  # Debugging print

            for row in results:

                if item_type == 'vinyl':
                    id_, name, artist, image, description = row
                    api_dict = {'name': name, 'artist': artist, 'image': image, 'description': description}
                    items.append(Vinyl(api_dict, id=id_))
                elif item_type == 'game':
                    id_, name, publisher, image, description = row
                    api_dict = {'name': name, 'publisher': publisher, 'image': image, 'description': description}
                    items.append(Game(api_dict, id=id_))
                elif item_type == 'book':
                    id_, name, authors, image, description = row
                    api_dict = {'title': name, 'author': authors, 'imageLinks': image, 'description': description}
                    items.append(Book(api_dict, id=id_))

    except Exception as e:
        print(f"Database error in load items: {e}")
    finally:
        conn.close()

    return items
