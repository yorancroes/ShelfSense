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
        self.setFixedSize(180, 240)  # Reduced size
        self.setStyleSheet("""
            #vinylCard {
                background-color: white;
                border-radius: 8px;
                padding: 8px;
                margin: 5px;
            }
            QLabel {
                color: #333333;
            }
        """)

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Image
        self.image_label = QLabel()
        self.image_label.setFixedSize(164, 164)  # Adjusted size
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.load_image(vinyl.image_url)
        layout.addWidget(self.image_label)

        # Album name
        name_label = QLabel(vinyl.name)
        name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)

        # Artist
        artist_label = QLabel(vinyl.artist)
        artist_label.setStyleSheet("color: #666666; font-size: 10px;")
        artist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(artist_label)

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