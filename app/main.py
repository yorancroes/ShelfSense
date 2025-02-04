from PyQt6.QtWidgets import QApplication
import sys
from app.frontend.windows.MainWindow import MainWindow
from app.Database.database_scripts.init_db import init_db

def main():

    init_db()
    app = QApplication(sys.argv)
    main_window = MainWindow()

    #main_window.showMaximized();
    main_window.show()  # Toon het hoofdvenster
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
