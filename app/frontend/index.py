import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.uic import loadUi #is voor QT Designer als mag gebruiken
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import os
from app.backend.user import User
from app.backend.helpers import WindowHelpers
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



class MainWindow(QMainWindow, WindowHelpers):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/main.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.loginButton.clicked.connect(self.clicked)
        self.registerButton.clicked.connect(self.clickedRegi)
        self.closeButton.clicked.connect(super().closing)
        self.miniButton.clicked.connect(super().mini)

    def clicked(self):
        self.win = LoginWindow()
        self.win.show()
        self.close()


    def clickedRegi(self):
        self.win = RegisterWindow()
        self.win.show()
        self.close()

class LoginWindow(QMainWindow, WindowHelpers):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/login.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.terugButton.clicked.connect(self.clicked)
        self.closeButton.clicked.connect(super().closing)
        self.miniButton.clicked.connect(super().mini)
        self.loginButton.clicked.connect(self.login)


    def clicked(self):
        self.win = RegisterWindow()
        self.win.show()
        self.close()

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        gebruiker = User(username, password)


        if gebruiker.verify_password(password):
            self.win = MenuWindow(gebruiker)
            self.win.show()
            self.close()


class RegisterWindow(QMainWindow, WindowHelpers):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/register.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.loginButton.clicked.connect(self.clicked)
        self.terugButton.clicked.connect(self.login)
        self.closeButton.clicked.connect(super().closing)
        self.miniButton.clicked.connect(super().mini)

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

class MenuWindow(QMainWindow, WindowHelpers):
    def __init__(self, gebruiker):
        super(MenuWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/menu.ui"), self)
        self.gebruiker = gebruiker
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.closeButton.clicked.connect(super().closing)
        self.miniButton.clicked.connect(super().mini)
        self.label_8.setText(gebruiker.get_username())
        self.load_image_from_url()
        #TODO: label_7 moet totale aantal items weergeven!!!
        self.addButton.clicked.connect(self.add)

    def load_image_from_url(self, url):
        # URL of the image
        self.url = url

        # Fetch the image from the URL
        response = requests.get(self.url)
        if response.status_code == 200:
            # Save the image to a temporary file
            with open("temp_image.jpg", "wb") as file:
                file.write(response.content)

            # Load the image and set it to the QLabel
            pixmap = QPixmap("temp_image.jpg")
            self.coverLabel.setPixmap(pixmap)
            self.coverLabel.setScaledContents(True)

    def add(self):
        self.win = AddWindow()
        self.win.show()

class AddWindow(QMainWindow):
    def __init__(self):
        super(AddWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/toevoegen.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.deleteButton.clicked.connect(self.delete)
        self.addButton.clicked.connect(self.add)

    def delete(self):
        self.close()


    def add(self):
        if self.nameEdit.toPlainText().strip() == "":
            self.nameEdit.setPlaceholderText("Voer een naam in!")
        else:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #main_window.showMaximized();
    main_window.show()  # Toon het hoofdvenster
    sys.exit(app.exec())