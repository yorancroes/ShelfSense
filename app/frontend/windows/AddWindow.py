import os
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.uic import loadUi #is voor QT Designer als mag gebruiken
from PyQt6.QtGui import QPixmap, QImage, QStandardItemModel, QIcon, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QListView
from app.backend.helpers import WindowHelpers
from API.music import searchMusic
from app.backend.items import Vinyl
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class AddWindow(QMainWindow,WindowHelpers):
    def __init__(self, menu_window, gebruiker):
        super().__init__()

        uic.loadUi(os.path.join(BASE_DIR, "../UI/toevoegen.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.deleteButton.clicked.connect(self.delete)
        self.addButton.clicked.connect(self.add)
        self.searchButton.clicked.connect(self.search)
        self.search_items.clicked.connect(self.album_selected)

        self.gebruiker = gebruiker
        self.menu_window = menu_window
        self.vinyl = None
        self.image = None

        self.model = QStandardItemModel()
        self.search_items.setModel(self.model)

        self.search_items.setViewMode(QListView.ViewMode.ListMode)
        self.search_items.setSpacing(5)
        self.search_items.setIconSize(QtCore.QSize(100, 100))
        self.search_items.setResizeMode(QListView.ResizeMode.Adjust)

        self.search_items.setItemDelegate(AlbumDelegate(self.search_items))

    def search(self):
        if self.LPButton.isChecked():
            album_text = self.searchBar.toPlainText().strip()
            albums = searchMusic(album_text)

            if not albums:
                print("No albums found")
                return

            self.model.clear()
            for album in albums:
                pixmap = QPixmap()
                image_url = album.get('image', '')

                if image_url:
                    try:
                        response = requests.get(image_url, timeout=5)
                        if response.status_code == 200:
                            pixmap.loadFromData(response.content)
                    except requests.RequestException:
                        print(f"Could not load image: {image_url}")

                icon = QIcon(pixmap)
                item = QStandardItem()
                item.setText(f"{album['name']} - {album['artist']}")  # Album + Artist
                item.setIcon(icon)
                item.setEditable(False)

                # Store album details in the item's data
                item.setData(album, QtCore.Qt.ItemDataRole.UserRole)

                self.model.appendRow(item)

    def delete(self):
        self.close()


    def add(self):
        if self.nameEdit.toPlainText().strip() == "":
            self.nameEdit.setPlaceholderText("Voer een naam in!")
        else:
            self.close()
            vinyl = {}
            vinyl['name'] = self.nameEdit.toPlainText().strip()
            vinyl['artist'] = self.iets1.toPlainText().strip()
            vinyl['image'] = self.image
            vinyl['description'] = self.iets2.toPlainText().strip()
            self.vinyl = Vinyl(vinyl)
            self.vinyl.upload(self.gebruiker.GetUserId())
            self.vinyl.load(self.menu_window.scroll_area)

    def album_selected(self, index):
        item = self.model.itemFromIndex(index)
        album = item.data(QtCore.Qt.ItemDataRole.UserRole)  # Retrieve stored album data

        if album:
            self.nameEdit.setText(album.get('name', ''))
            self.iets1.setText(album.get('artist', ''))
            self.image = album.get('image', '')  # Store image URL for later use


class AlbumDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        # Get album data
        model = index.model()
        item = model.itemFromIndex(index)

        icon = item.icon()
        text = item.text()

        # Draw background selection
        if option.state & QtWidgets.QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Draw album cover
        icon_rect = QtCore.QRect(option.rect.left() + 5, option.rect.top() + 5, 60, 60)
        icon.paint(painter, icon_rect, QtCore.Qt.AlignmentFlag.AlignLeft)

        # Draw text
        text_rect = QtCore.QRect(icon_rect.right() + 10, option.rect.top(),
                                 option.rect.width() - 80, option.rect.height())
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignVCenter, text)

        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(200, 70)  # Each item should be 70px tall
