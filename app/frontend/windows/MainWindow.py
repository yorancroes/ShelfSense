import os
from PyQt6 import QtCore, uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon
from PyQt6.QtCore import Qt, QPoint
from app.backend.helpers import WindowHelpers
from app.frontend.windows.LoginWindow import LoginWindow
from app.frontend.windows.RegisterWindow import RegisterWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow, WindowHelpers):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "../ui/main.ui"), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("frontend/test.png"))


        self.loginButton.clicked.connect(self.clicked)
        self.registerButton.clicked.connect(self.clickedRegi)
        self.closeButton.clicked.connect(self.closing)
        self.miniButton.clicked.connect(self.mini)

        self.dragging = False  # Flag to track dragging state
        self.offset = QPoint()  # Stores the position offset for smooth dragging

    def clicked(self):
        self.win = LoginWindow()
        self.win.show()
        self.close()

    def clickedRegi(self):
        self.win = RegisterWindow()
        self.win.show()
        self.close()

