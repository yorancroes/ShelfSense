import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.uic import loadUi #is voor QT Designer als mag gebruiken
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import os 
from backend.sharedate import SharedData, set_credentials 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/main.ui"), self)
        self.loginButton.clicked.connect(self.clicked)
        self.shared_data = SharedData()


    def clicked(self):
        self.win = LoginWindow()
        self.win.show()
        self.close()



class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/login.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.loginButton.clicked.connect(self.clicked)
        self.shared_data = SharedData()  # Correct initialization

    def clicked(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        set_credentials(self.shared_data, username, password)


