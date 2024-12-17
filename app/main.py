from PyQt6.QtWidgets import QApplication

import sys
from frontend.index import MainWindow

import os 
def main():

    app = QApplication(sys.argv)
    main_window = MainWindow()
    #main_window.showMaximized();
    main_window.show()  # Toon het hoofdvenster
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
