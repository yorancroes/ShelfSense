from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QPushButton
from app.backend.helpers import WindowHelpers
from app.frontend.windows.AddWindow import AddWindow
from app.backend.items import load_items, Vinyl, Game, Book
import os
from app.Database.database_scripts.connect import connect_db
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

            items = (
                    load_items(self.gebruiker.GetUserId(), item_type='vinyl') +
                    load_items(self.gebruiker.GetUserId(), item_type='game') +
                    load_items(self.gebruiker.GetUserId(), item_type='book')
            )

            # Update total items label
            if hasattr(self, 'label_7'):
                self.label_7.setText(str(len(items)))

            self.selected_items = []

            # Add item cards to grid
            columns = 3
            for i, item in enumerate(items):
                row = i // columns
                col = i % columns
                item_widget = item.load(self.grid_layout, row, col)

                # Ensure widget is linked to its item object
                item_widget.mousePressEvent = lambda event, w=item_widget, obj=item: self.select_item(w, obj)

                self.grid_layout.addWidget(item_widget, row, col)

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

    def select_item(self, item_widget, item_object):
        if item_object not in self.selected_items:
            self.selected_items.append(item_object)
            item_widget.setStyleSheet("border-radius: 5px; background-color: rgba(51, 153, 204,50);")
        else:
            self.selected_items.remove(item_object)
            item_widget.setStyleSheet("border-radius: 5px;")
        print(f"Selected items: {[item.id for item in self.selected_items]}")

    def create_item_deletion_function(self, item):
        return lambda checked: self.select_item(item)

    def delete(self):
        try:
            if not self.selected_items:
                print("No items selected for deletion.")
                return

            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    for item in self.selected_items:
                        if hasattr(item, "id") and item.id:  # Ensure item has an ID
                            if isinstance(item, Vinyl):
                                table = "vinyls"
                            elif isinstance(item, Game):
                                table = "games"
                            elif isinstance(item, Book):
                                table = "books"
                            else:
                                continue  # Skip if item type is unknown

                            query = f"DELETE FROM {table} WHERE id = %s;"
                            cursor.execute(query, (item.id,))
                            conn.commit()
                            print(f"Deleted {table} item with ID: {item.id}")
                            self.load_items()

            except Exception as e:
                print(f"Database error while deleting items: {e}")
                conn.rollback()
            finally:
                conn.close()

            # Remove items from the UI
            for item in self.selected_items:
                for i in range(self.grid_layout.count()):
                    widget = self.grid_layout.itemAt(i).widget()
                    if widget and hasattr(widget, "item_id") and widget.item_id == item.id:
                        self.grid_layout.removeWidget(widget)
                        widget.deleteLater()

            self.selected_items.clear()

        except Exception as e:
            print(f"Error deleting items: {e}")
            import traceback
            traceback.print_exc()


