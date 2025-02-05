import os
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.uic import loadUi #is voor QT Designer als mag gebruiken
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from app.backend.helpers import WindowHelpers
from API.music import searchMusic
from app.backend.items import Vinyl
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class AddWindow(QMainWindow,WindowHelpers):
    def __init__(self, menu_window, gebruiker):
        super(AddWindow, self).__init__()
        self.gebruiker = gebruiker
        self.menu_window = menu_window
        uic.loadUi(os.path.join(BASE_DIR, "../UI/toevoegen.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.deleteButton.clicked.connect(self.delete)
        self.addButton.clicked.connect(self.add)
        self.searchButton.clicked.connect(self.search)

    def search(self):
        user_id = self.gebruiker.GetUserId()

        if self.LPButton.isChecked():
            album_text = self.searchBar.toPlainText().strip()
            albums = searchMusic(album_text)
            vinyls = []

            for album in albums:
                vinyl = Vinyl(album)
                vinyl.load(self.menu_window.coverLabel)
                self.gebruiker.AddVinyl(vinyl)
                vinyl.upload(user_id)
            print(vinyls)
        else:
            print("no button selecetd")

    def delete(self):
        self.close()


    def add(self):
        if self.nameEdit.toPlainText().strip() == "":
            self.nameEdit.setPlaceholderText("Voer een naam in!")
        else:
            self.close()

    def set_cover_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.coverLabel.setPixmap(pixmap.scaled(self.coverLabel.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
