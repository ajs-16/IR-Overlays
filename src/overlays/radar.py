from .base_overlay import BaseOverlay
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QRect

class RadarOverlay(BaseOverlay):
    def __init__(self, worker, settings):
        super().__init__(settings, base_width=200, base_height=200)
        self.apply_scaling(settings['Scale'].slider.value())

    def paintEvent(self, event):
        w = self.width()
        h = self.height()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(0, 0, w, h, QColor(0, 0, 0, 1))
        painter.end()

        self.draw_grid()
        self.draw_car()

    def draw_grid(self):
        w = self.width()
        h = self.height()

        painter = QPainter(self)
        painter.setPen(
            QPen(
                QColor(255, 255, 255, 100),
                1,
                Qt.DashLine
            )
        )
        painter.drawLine(0, h / 2, w, h / 2)
        painter.drawLine(w / 2, 0, w / 2, h)
        painter.end()

    def draw_car(self):
        carW = self.width() * 0.1
        carH = self.height() * 0.2

        painter = QPainter(self)
        car = QRect(
            (self.width() - carW) / 2,
            (self.height() - carH) / 2,
            carW,
            carH
        )
        painter.fillRect(
            car, 
            QColor(255, 255, 255, 200)
        )
        painter.end()
