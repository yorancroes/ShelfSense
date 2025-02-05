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
        super(AddWindow).__init__()
        super(AddWindow, self).__init__()
        self.gebruiker = gebruiker
        self.menu_window = menu_window
        uic.loadUi(os.path.join(BASE_DIR, "../UI/toevoegen.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.deleteButton.clicked.connect(self.delete)
        self.addButton.clicked.connect(self.add)
        self.searchButton.clicked.connect(self.search)
        self.vinyl = None
        self.image = None

    def search(self):

        if self.LPButton.isChecked():
            album_text = self.searchBar.toPlainText().strip()
            albums = searchMusic(album_text)
            
            album = albums[0]
            print(album)
            self.nameEdit.setText(album['name'])
            self.iets1.setText(album['artist'])
            self.image = album['image']



        else:
            print("no button selected")

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
            print(vinyl)
            self.vinyl = Vinyl(vinyl)
            print(self.vinyl)
            self.vinyl.upload(self.gebruiker.GetUserId())
            #TODO: self.vinyl.load() label aanmaken voor de vinyl om te loaden
