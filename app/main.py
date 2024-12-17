from PyQt6.QtWidgets import QApplication
from backend.username import get_username
import sys
from frontend.index import MainWindow

import os 
def main():

    app = QApplication(sys.argv)
    main_window = MainWindow()
    #main_window.showMaximized();
    main_window.show()  # Toon het hoofdvenster
    get_username() 
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
