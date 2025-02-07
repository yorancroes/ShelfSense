import os
from PyQt6 import QtCore, uic
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QTimer
from PyQt6.QtWidgets import QMainWindow, QWidget
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
        self.widgetMove = self.findChild(QWidget, 'widget2')

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

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        gebruiker = User(username, password)
        gebruiker.insert_user()

        QTimer.singleShot(600, self.close_window)

    def login(self):
        start = self.widgetMove.geometry()
        end = QRect(-20, start.top(), start.width(), start.height())

        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.setDuration(600)
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.animation.start()

        QTimer.singleShot(600, self.close_window)

    def close_window(self):
        from app.frontend.windows.LoginWindow import LoginWindow
        self.win = LoginWindow()
        self.win.show()
        self.close()