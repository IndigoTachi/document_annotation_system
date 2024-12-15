from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QRect, QPoint


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.rect_coords = None
        self.proportional_rect_coords = None
        self.can_draw = False

    def mousePressEvent(self, event):
        if self.can_draw and event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if self.can_draw and event.buttons() == Qt.MouseButton.LeftButton:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.can_draw and event.button() == Qt.MouseButton.LeftButton:
            rect = QRect(self.start_point, self.end_point).normalized()
            self.rect_coords = [rect.x(), rect.y(), rect.width(), rect.height()]
            self.update()

    def set_rect_coords(self, rect_coords):
        self.rect_coords = rect_coords
        self.update()

    def clear_rectangle(self):
        self.rect_coords = None
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.rect_coords:
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.red, 2)
            painter.setPen(pen)
            x, y, width, height = self.rect_coords
            painter.drawRect(QRect(x, y, width, height))
