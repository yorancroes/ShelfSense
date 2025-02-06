from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget
from app.backend.helpers import WindowHelpers
from app.frontend.windows.AddWindow import AddWindow
from app.backend.items import load_items
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MenuWindow(QMainWindow, WindowHelpers):
    def __init__(self, gebruiker):
        super(MenuWindow, self).__init__()

        # Load UI first
        uic.loadUi(os.path.join(BASE_DIR, "../UI/menu.ui"), self)
        self.gebruiker = gebruiker

        # Window setup
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Connect buttons
        self.closeButton.clicked.connect(super().closing)
        self.miniButton.clicked.connect(super().mini)
        self.addButton.clicked.connect(self.add)

        # Set user info
        self.label_8.setText(gebruiker.get_username())

        try:
            # Setup grid layout in the existing scroll area content widget
            self.grid_layout = QGridLayout(self.scrollAreaWidgetContents)
            self.grid_layout.setSpacing(20)
            self.grid_layout.setContentsMargins(20, 20, 20, 20)

            # Clear default widgets from UI file
            for child in self.scrollAreaWidgetContents.findChildren((QWidget)):
                child.deleteLater()

            # Initial load of vinyls
            self.load_items()

        except Exception as e:
            print(f"Error initializing MenuWindow: {e}")
            import traceback
            traceback.print_exc()

    def load_items(self):
        try:
            while self.grid_layout.count():
                item = self.grid_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            items = load_items(self.gebruiker.GetUserId(), item_type='vinyl') + load_items(self.gebruiker.GetUserId(),
                                                                                           item_type='game')

            # Update total items label
            if hasattr(self, 'label_7'):
                self.label_7.setText(str(len(items)))

            # Add item cards to grid
            columns = 3
            for i, item in enumerate(items):
                row = i // columns
                col = i % columns
                item.load(self.grid_layout, row, col)

            # Add stretch to fill empty space
            self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)
            self.grid_layout.setColumnStretch(self.grid_layout.columnCount(), 1)

        except Exception as e:
            print(f"Error loading items: {e}")
            import traceback
            traceback.print_exc()

    def add(self):
        try:
            self.win = AddWindow(self, self.gebruiker)
            self.win.show()
        except Exception as e:
            print(f"Error opening AddWindow: {e}")
            import traceback
            traceback.print_exc()