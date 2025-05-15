from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPaintEvent, QColor, QPainterPath, QPainter
from PySide6.QtWidgets import QWidget, QLabel

class InputTelemetryOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 100)

        self._drag_pos = None

    def paintEvent(self, event: QPaintEvent):
        w = self.width()
        h = self.height()
        radius = h / 2

        # Draw the base shape path
        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(w - radius, 0)
        path.quadTo(w, 0, w, radius)
        path.lineTo(w, h - radius)
        path.quadTo(w, h, w - radius, h)
        path.lineTo(0, h)
        path.closeSubpath()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fill base rectangle
        painter.fillPath(path, QColor(0, 0, 0, 180))

        painter.setClipPath(path)

        # Add Stripe
        stripeWidth = 5
        stripeRect = QRectF(0, 0, stripeWidth, h)
        painter.fillRect(stripeRect, QColor(0, 0, 255, 200))

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
