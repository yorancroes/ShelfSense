import os
from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QMainWindow
from app.backend.helpers import WindowHelpers
from app.backend.user import User
from app.frontend.windows.LoginWindow import LoginWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class RegisterWindow(QMainWindow, WindowHelpers):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "../ui/register.ui"), self)
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