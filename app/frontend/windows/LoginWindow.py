import os
from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QMainWindow
from app.backend.helpers import WindowHelpers
from app.backend.user import User
from app.frontend.windows.MenuWIndow import  MenuWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class LoginWindow(QMainWindow, WindowHelpers):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "../ui/login.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.terugButton.clicked.connect(self.clicked)
        self.closeButton.clicked.connect(super().closing)
        self.miniButton.clicked.connect(super().mini)
        self.loginButton.clicked.connect(self.login)

    def clicked(self):
        from app.frontend.windows.RegisterWindow import RegisterWindow
        self.win = RegisterWindow()
        self.win.show()
        self.close()

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        gebruiker = User(username, password)
        print(f"logging in: {gebruiker.username}")

        if gebruiker.verify_password(password):
            print("login successful")
            self.win = MenuWindow(gebruiker)
            self.win.show()
            self.close()