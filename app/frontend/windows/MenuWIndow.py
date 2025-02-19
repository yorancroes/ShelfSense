from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QPushButton
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
        self.deleteButton.clicked.connect(self.delete)
        self.lpButton.clicked.connect(self.filter_vinyls)
        self.bookButton.clicked.connect(self.filter_books)
        self.gameButton.clicked.connect(self.filter_games)
        self.allButton.clicked.connect(self.load_items)

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
            item_type='game') + load_items(self.gebruiker.GetUserId(),item_type='book')

            # Update total items label
            if hasattr(self, 'label_7'):
                self.label_7.setText(str(len(items)))

                # vò às ge miër às iën wilt dún, perchance
                self.selected_items = []

            # Add item cards to grid
            columns = 3
            for i, item in enumerate(items):
                row = i // columns
                col = i % columns
                item_widget = QWidget(item.load(self.grid_layout, row, col))
                #item.load(self.grid_layout, row, col)

                item_widget.setStyleSheet("border-radius: 5px;")

                # Voeg mousePressEvent toe aan deze widget
                item_widget.mousePressEvent = lambda event, widget=item_widget: self.select_item(widget)

                # Voeg de widget toe aan de layout
                self.grid_layout.addWidget(item_widget, row, col)

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

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def filter_vinyls(self):
        items = load_items(self.gebruiker.GetUserId(), item_type='vinyl')
        self.label_7.setText(str(len(items)))
        self.clear_layout(self.grid_layout)

        columns = 3
        for i, item in enumerate(items):
            row = i // columns
            col = i % columns
            item.load(self.grid_layout, row, col)

    def filter_books(self):
        items = load_items(self.gebruiker.GetUserId(), item_type='book')
        self.label_7.setText(str(len(items)))
        self.clear_layout(self.grid_layout)

        columns = 3
        for i, item in enumerate(items):
            row = i // columns
            col = i % columns
            item.load(self.grid_layout, row, col)

    def filter_games(self):
        items = load_items(self.gebruiker.GetUserId(), item_type='game')
        self.label_7.setText(str(len(items)))
        self.clear_layout(self.grid_layout)

        columns = 3
        for i, item in enumerate(items):
            row = i // columns
            col = i % columns
            item.load(self.grid_layout, row, col)

    def select_item(self, item):
        if item not in self.selected_items:
            self.selected_items.append(item)
            item.setStyleSheet("border-radius: 5px; background-color: rgba(51, 153, 204,50);")
        else:
            self.selected_items.remove(item)
            item.setStyleSheet("border-radius: 5px;")
        print(f"Selected items: {self.selected_items}")

    def create_item_deletion_function(self, item):
        return lambda checked: self.select_item(item)

    def delete(self):
        try:
            for item in self.selected_items:
                widget = item
                if widget:
                    self.grid_layout.removeWidget(widget)
                    widget.deleteLater()
                print(f"Deleted item: {item}")
            self.selected_items.clear()

        except Exception as e:
            print(f"Error deleting items: {e}")
            import traceback
            traceback.print_exc()
