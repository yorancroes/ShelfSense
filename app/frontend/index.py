import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.uic import loadUi #is voor QT Designer als mag gebruiken
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import os
from backend.user import User


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/main.ui"), self)
        self.loginButton.clicked.connect(self.clicked)


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


    def clicked(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        gebruiker = User(username, password)
        gebruiker.insert_user()

        if gebruiker.verify_password(password):
            print("password is correct!")
            #TODO: MAKE THE HOME SCREEN!
        else:
            print("password is incorrect!")


