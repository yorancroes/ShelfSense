from PyQt6.QtCore import Qt, QPoint

class WindowHelpers():
    def __init__(self):
        self.dragging = False
        self.offset = QPoint()

    def closing(self):
        self.close()

    def mini(self):
        self.showMinimized()

    def mousePressEvent(self, event):
        """ Start dragging when left mouse button is pressed. """
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        """ Move the window while dragging. """
        if self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        """ Stop dragging when the left mouse button is released. """
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()
