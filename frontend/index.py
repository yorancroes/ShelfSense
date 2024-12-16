import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.uic import loadUi #is voor QT Designer als mag gebruiken
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(BASE_DIR, "UI/main.ui"), self)
        """self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Shelfsense')

        self.label = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.label3 = QtWidgets.QLabel(self)

        self.label.setText("Welcome to Shelfsense!")
        self.label.adjustSize()
        self.label.move(50, 100)

        self.label2.setText("The place where collectors gather!")
        self.label2.adjustSize()
        self.label2.move(50, 120)

        self.label3.setText("Scored a new item? Add it here!")
        self.label3.adjustSize()
        self.label3.move(50, 160)

        self.label2 = QtWidgets.QLabel(self)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Start Collecting!")
        self.b1.move(50, 120)
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label2.setText("you pressed Login")
        self.label2.move(50, 200)

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setGeometry(100, 100, 800, 800)
        self.setStyleSheet("QWidget{background-color: qlineargradient(y1: 0, y1: 0, x2: 1, y2: 1,stop: 0 blue, stop: 0.8 purple);}")
        self.setWindowTitle('Shelfsense - Login')

        self.label = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.label3 = QtWidgets.QLabel(self)
        self.label4 = QtWidgets.QLabel(self)

        self.label5 = QtWidgets.QLabel(self)
        pixmap = QPixmap('test.png')
        self.label5.setPixmap(pixmap)
        self.label5.setScaledContents(True)


        self.label.setText("Login")
        self.label.setStyleSheet("color: cyan;"
                                 "background-color: none;"
                                 "font-weight: bold;"
                                 "font-size: 20px;")
        self.label.move(50, 30)

        self.label2.hide()

        self.label3.setText("Username")
        self.label3.setStyleSheet("color: cyan;"
                                  "background-color: none;"
                                  "font-size: 15px;")
        self.label3.move(50, 60)

        self.label4.setText("Password")
        self.label4.setStyleSheet("color: cyan;"
                                  "background-color: none;"
                                  "font-size: 15px;")
        self.label4.move(50, 80)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Login")
        self.b1.move(50, 120)
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label2.setText("you pressed Login")
        self.label2.setStyleSheet(f"qproperty-alignment: {int(QtCore.Qt.AlignmentFlag.AlignCenter)};"
                                  "background-color: rgb(150, 0, 255);"
                                  "color: cyan;"
                                  "font-weight: bold;"
                                  "min-width: 200px;"
                                  "min-height: 200px;"
                                  "font-size: 20px;")
        self.label2.move(50, 200)
        self.win = MainWindow()
        self.win.show()
        self.close()"""

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #main_window.showMaximized();
    main_window.show()  # Toon het hoofdvenster
    sys.exit(app.exec())
