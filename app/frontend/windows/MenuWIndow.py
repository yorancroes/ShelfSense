from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.uic import loadUi #is voor QT Designer als mag gebruiken
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from app.backend.helpers import WindowHelpers
from app.frontend.windows.AddWindow import AddWindow
from app.backend.user import User
from app.backend.items import *
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MenuWindow(QMainWindow, WindowHelpers):
    def __init__(self, gebruiker):
        super(MenuWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "../UI/menu.ui"), self)
        self.gebruiker = gebruiker
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.closeButton.clicked.connect(super().closing)
        self.miniButton.clicked.connect(super().mini)
        self.label_8.setText(gebruiker.get_username())
        # TODO: label_7 moet totale aantal items weergeven!!!
        self.addButton.clicked.connect(self.add)
        self.coverLabel = self.findChild(QLabel, "coverLabel")
        vinyls = load_vinyls(self.gebruiker.GetUserId())
        # for vinyl in vinyls:
        #     vinyl.load()
        print(vinyls)

    def add(self):
        self.win = AddWindow(self, self.gebruiker)
        self.win.show()