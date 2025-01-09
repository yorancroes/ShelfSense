from PyQt6.QtWidgets import QApplication
import sys
from frontend.index import MainWindow
from Database.database_scripts.init_db import init_db

import os 
def main():

    # init_db()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #main_window.showMaximized();
    main_window.show()  # Toon het hoofdvenster
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
