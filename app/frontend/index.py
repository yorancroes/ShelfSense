import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.uic import loadUi #is voor QT Designer als mag gebruiken
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import os
from app.backend.user import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/main.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.loginButton.clicked.connect(self.clicked)
        self.registerButton.clicked.connect(self.clickedRegi)
        self.closeButton.clicked.connect(self.closing)
        self.miniButton.clicked.connect(self.mini)

    def clicked(self):
        self.win = LoginWindow()
        self.win.show()
        self.close()


    def clickedRegi(self):
        self.win = RegisterWindow()
        self.win.show()
        self.close()

    def closing(self):
        self.close()

    def mini(self):
        self.showMinimized()

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/login.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.terugButton.clicked.connect(self.clicked)
        self.closeButton.clicked.connect(self.closing)
        self.miniButton.clicked.connect(self.mini)
        self.loginButton.clicked.connect(self.login)


    def clicked(self):
        self.win = RegisterWindow()
        self.win.show()
        self.close()

    def closing(self):
        self.close()

    def mini(self):
        self.showMinimized()

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        gebruiker = User(username, password)


        if gebruiker.verify_password(password):
            self.win = MenuWindow(gebruiker)
            self.win.show()
            self.close()


class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/register.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.loginButton.clicked.connect(self.clicked)
        self.terugButton.clicked.connect(self.login)
        self.closeButton.clicked.connect(self.closing)
        self.miniButton.clicked.connect(self.mini)

    def clicked(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        gebruiker = User(username, password)
        gebruiker.insert_user()

        self.win = LoginWindow()
        self.win.show()
        self.close()

    def login(self):
        self.win = LoginWindow()
        self.win.show()
        self.close()

    def closing(self):
        self.close()

    def mini(self):
        self.showMinimized()

class MenuWindow(QMainWindow):
    def __init__(self, gebruiker):
        super(MenuWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/menu.ui"), self)
        self.gebruiker = gebruiker
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label_8.setText(gebruiker.get_username())
        #TODO: label_7 moet totale aantal items weergeven!!!
        self.addButton.clicked.connect(self.add)

    def add(self):
        self.win = AddWindow()
        self.win.show()

class AddWindow(QMainWindow):
    def __init__(self):
        super(AddWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/toevoegen.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #main_window.showMaximized();
    main_window.show()  # Toon het hoofdvenster
    sys.exit(app.exec())