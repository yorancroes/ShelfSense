import os
from PyQt6 import QtCore, uic
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QTimer
from PyQt6.QtWidgets import QMainWindow, QWidget
from app.backend.helpers import WindowHelpers
from app.backend.user import User
from app.frontend.windows.MenuWIndow import  MenuWindow
from app.backend.items import *

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
        self.loginButton.clicked.connect(self.clickedLogin)
        self.widgetMove = self.findChild(QWidget, 'widget2')
        self.gebruiker = None

        self.animation = QPropertyAnimation(self.widgetMove, b"geometry")

        start = self.widgetMove.geometry()
        end = QRect(290, start.top(), start.width(), start.height())

        self.animation.setStartValue(start)
        self.animation.setEndValue(end)

        self.animation.setDuration(600)
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)

        self.animation.start()

    def clicked(self):
        start = self.widgetMove.geometry()
        end = QRect(-20, start.top(), start.width(), start.height())

        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.setDuration(600)
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.animation.start()

        QTimer.singleShot(600, self.close_window)

    def clickedLogin(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.gebruiker = User(username, password)
        if self.gebruiker.verify_password(password):
            start = self.widgetMove.geometry()
            end = QRect(-20, start.top(), start.width(), start.height())

            self.animation.setStartValue(start)
            self.animation.setEndValue(end)
            self.animation.setDuration(600)
            self.animation.setEasingCurve(QEasingCurve.Type.Linear)
            self.animation.start()

        QTimer.singleShot(600, self.login)

    def login(self):
        password = self.lineEdit_2.text()
        if self.gebruiker.verify_password(password):
            id = self.gebruiker.GetUserId()
            user_vinyls = load_vinyls(id)
            self.gebruiker.SetVinyls(user_vinyls)
            self.win = MenuWindow(self.gebruiker)
            self.win.show()
            self.close()

    def close_window(self):
        from app.frontend.windows.RegisterWindow import RegisterWindow
        self.win = RegisterWindow()
        self.win.show()
        self.close()