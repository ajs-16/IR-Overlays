from PySide6.QtCore import Qt, QRect, QRectF
from PySide6.QtGui import QPaintEvent, QColor, QPainterPath, QPainter, QPen
from PySide6.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg

class TelemetryGraph(pg.PlotWidget):
    def __init__(self):
        pg.setConfigOption('background', (60, 60, 60, 170))

        super().__init__()
        self.setFixedSize(300, 100)

        self.setStyleSheet(
            """
            background: transparent;
            border: 1px solid black;
            """
        )

        self.hideAxis('bottom')
        self.hideAxis('left')
        
    def update_graph(self, data):
        pass

class TelemetryBar(QWidget):
    def __init__(self, colour):
        super().__init__()
        self.colour: QColor = colour
        self._value = 50
        self.barHeight = 84
        self.textZone = 16
        self.setFixedSize(20, self.textZone + self.barHeight)

    def update_value(self, value):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(Qt.white)
        f = painter.font()
        f.setBold(True)
        painter.setFont(f)
        text = str(self._value)
        text_rect = QRect(0, 0, self.width(), self.textZone)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, text)

        borderWidth = 1
        outer = QRect(
            0,
            self.textZone,
            self.width(),
            self.barHeight
        )
        inner = outer.adjusted(
            borderWidth,
            borderWidth,
            -borderWidth,
            -borderWidth
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(60, 60, 60, 170))
        painter.drawRect(inner)

        fillHeight = int(self._value / 100.0 * inner.height())
        fillRect = QRect(
            inner.left(),
            inner.bottom() - fillHeight + 1,
            inner.width(),
            fillHeight
        )
        painter.setBrush(self.colour)
        painter.drawRect(fillRect)

        # draw the red fill
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.black, borderWidth))
        painter.drawRect(inner)

        painter.end()

class InputTelemetryOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 110)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignLeft)

        layout.addWidget(TelemetryGraph())
        layout.addWidget(TelemetryBar(QColor(255, 0, 0)))
        layout.addWidget(TelemetryBar(QColor(0, 255, 0)))

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
