from PySide6.QtCore import Qt, QRect, QRectF, QPointF
from PySide6.QtGui import QPaintEvent, QColor, QPainterPath, QPainter, QPen, QFont, QFontMetricsF
from PySide6.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg
from collections import deque
import math

pg.setConfigOptions(antialias=True)

class TelemetryGraph(pg.PlotWidget):
    def __init__(self, worker):
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

        # Horizontal grid lines
        for yVal in [0, 25, 50, 75, 100]:
            gridLine = pg.InfiniteLine(
                pos=yVal, 
                angle=0,
                pen=pg.mkPen(color=(200, 200, 200, 75), width=1, style=Qt.DotLine)
            )
            self.addItem(gridLine)

        self.enableAutoRange(y=False, x=False)
        self.setXRange(0, 500, padding=0)
        self.setYRange(-3, 102, padding=0)

        plotItem = self.getPlotItem()
        plotItem.vb.setLimits(yMin=-3, yMax=102)
        plotItem.hideButtons()
        plotItem.setMouseEnabled(x=False, y=False)
        plotItem.setMenuEnabled(False)
        self.setToolTip('')

        # Buffers for throttle and brake data
        self._brakeBuffer = deque(maxlen=500)
        self._throttleBuffer = deque(maxlen=500)

        self._brakeLine = self.plot(pen=pg.mkPen('r', width=4))
        self._throttleLine = self.plot(pen=pg.mkPen('g', width=4))
        
        # Update the graph on updated telemetry signal
        worker.updatedTelemetry.connect(self.update_graph)

    def update_graph(self, data):
        self._brakeBuffer.append(data['brake'])
        self._throttleBuffer.append(data['throttle'])

        self._brakeLine.setData(self._brakeBuffer)
        self._throttleLine.setData(self._throttleBuffer)

class TelemetryBar(QWidget):
    def __init__(self, pedal, colour, worker):
        super().__init__()
        worker.updatedTelemetry.connect(self.update_value)

        self.pedal = pedal
        self.colour: QColor = colour
        self._value = 0
        self.barHeight = 84
        self.textZone = 16
        self.setFixedSize(20, self.textZone + self.barHeight)

    def update_value(self, data):
        if self.pedal == 'brake' and 'brake' in data:
            self._value = data['brake']
        elif self.pedal == 'throttle' and 'throttle' in data:
            self._value = data['throttle']

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(Qt.white)
        painter.setFont(QFont("Roboto", 10, QFont.Bold))
        text_rect = QRect(0, 0, self.width(), self.textZone)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, str(self._value))

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

class TelemetryWheel(QWidget):
    def __init__(self, worker):
        super().__init__()
        self.gear = "N"
        self.speed = 0
        self.wheelAngle = 0.0

        self._fonts = {
            'gear': QFont("Roboto", 20, QFont.Bold),
            'speed': QFont("Roboto", 18, QFont.Bold),
            'unit': QFont("Roboto", 11, QFont.Bold)
        }
        self._metrics = {k: QFontMetricsF(f) for k, f in self._fonts.items()}

        worker.updatedTelemetry.connect(self.update_metrics)

        self.setFixedSize(100, 100)

    def normalise_angle(self, angle):
        normalised = angle % (2 * math.pi)
        if normalised < 0: normalised += 2 * math.pi

        return abs(normalised)

    def update_metrics(self, data):
        self.gear = data['gear']
        self.speed = data['speed']
        self.wheelAngle = data['wheelAngle']
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Center the wheel in the widget
        diameter = 90
        radius = diameter / 2
        x = (self.width() - diameter) // 2
        y = (self.height() - diameter) // 2
        cx = x + radius
        cy = y + radius

        # Draw wheel
        painter.setBrush(QColor(40, 40, 40, 255))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x, y, diameter, diameter)

        # Add border
        borderWidth = 10
        painter.setPen(QPen(Qt.black, borderWidth))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(x, y, diameter, diameter)

        # Draw wheel angle marker
        painter.save()
        painter.translate(cx, cy)

        markerWidth = 12
        markerHeight = 6

        normalisedAngle = self.normalise_angle(self.wheelAngle)
        drawAngle = -(normalisedAngle)
        painter.rotate(math.degrees(drawAngle))

        y0 = -radius - (borderWidth/2) + (markerHeight/2)

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)

        painter.drawRect(-markerWidth/2, y0, markerWidth, markerHeight)
        painter.restore()

        # Draw gear and speed
        painter.save()
        painter.translate(cx, cy)
        painter.setPen(Qt.white)

        items = [
            ('gear', self.gear, QPointF(0,-radius * 0.25)),
            ('unit', 'kph', QPointF(0, +radius * 0.25)),
            ('speed', str(self.speed), QPointF(0, +radius * 0.75)),
        ]

        for key, text, pos in items:
            font = self._fonts[key]
            fm = self._metrics[key]
            width = fm.horizontalAdvance(text)
            painter.setFont(font)
            painter.drawText(pos - QPointF(width/2, 0), text)

        painter.restore()

class InputTelemetryOverlay(QWidget):
    def __init__(self, worker):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(470, 110)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignLeft)

        layout.addWidget(TelemetryGraph(worker))
        layout.addWidget(TelemetryBar('brake', QColor(255, 0, 0), worker))
        layout.addWidget(TelemetryBar('throttle', QColor(0, 255, 0), worker))
        layout.addWidget(TelemetryWheel(worker))

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
        painter.fillPath(path, QColor(0, 0, 0, 200))

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
