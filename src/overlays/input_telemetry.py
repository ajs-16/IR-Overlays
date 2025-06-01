from PySide6.QtCore import Qt, QRect, QRectF, QPointF
from PySide6.QtGui import QPaintEvent, QColor, QPainterPath, QPainter, QPen, QFont, QFontMetricsF
from PySide6.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg
from collections import deque
import math
from .base_overlay import BaseOverlay

pg.setConfigOptions(antialias=True)

class TelemetryGraph(pg.PlotWidget):
    def __init__(self, worker):
        pg.setConfigOption('background', (60, 60, 60, 170))
        super().__init__()

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

        self._brakeLine = self.plot(pen=pg.mkPen('r', width=3))
        self._throttleLine = self.plot(pen=pg.mkPen('g', width=3))
        
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

    def update_value(self, data):
        if self.pedal == 'brake' and 'brake' in data:
            self._value = data['brake']
        elif self.pedal == 'throttle' and 'throttle' in data:
            self._value = data['throttle']

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()

        textH = h * 0.16
        barH = h - textH

        painter.setPen(Qt.white)
        painter.setFont(QFont("Roboto", textH * 0.6, QFont.Bold))
        textRect = QRect(0, 0, w, textH)
        painter.drawText(textRect, Qt.AlignCenter | Qt.AlignVCenter, str(self._value))

        borderWidth = 1
        outer = QRect(
            0,
            textH,
            w,
            barH
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

        # draw the colour fill
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

        worker.updatedTelemetry.connect(self.update_metrics)

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
        w, h = self.width(), self.height()

        fonts = {
            'gear': QFont("Roboto", w * 0.2, QFont.Bold),
            'speed': QFont("Roboto", w * 0.18, QFont.Bold),
            'unit': QFont("Roboto", w * 0.11, QFont.Bold)
        }
        fontMetrics = {k: QFontMetricsF(f) for k, f in fonts.items()}

        # Center the wheel in the widget
        diameter = w * 0.9
        radius = diameter / 2
        x = (w - diameter) // 2
        y = (h - diameter) // 2
        cx = x + radius
        cy = y + radius

        # Draw wheel
        painter.setBrush(QColor(40, 40, 40, 255))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x, y, diameter, diameter)

        # Add border
        borderWidth = w * 0.1
        painter.setPen(QPen(Qt.black, borderWidth))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(x, y, diameter, diameter)

        # Draw wheel angle marker
        painter.save()
        painter.translate(cx, cy)

        markerWidth = w * 0.12
        markerHeight = w * 0.06

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
            font = fonts[key]
            fm = fontMetrics[key]
            width = fm.horizontalAdvance(text)
            painter.setFont(font)
            painter.drawText(pos - QPointF(width/2, 0), text)

        painter.restore()

class InputTelemetryOverlay(BaseOverlay):
    def __init__(self, worker, settings):
        super().__init__(settings, base_width=470, base_height=110)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)

        self.graph = TelemetryGraph(worker)
        self.brakeBar = TelemetryBar('brake', QColor(255, 0, 0), worker)
        self.throttleBar = TelemetryBar('throttle', QColor(0, 255, 0), worker)
        self.wheel = TelemetryWheel(worker)

        self.layout.addWidget(self.graph)
        self.layout.addWidget(self.brakeBar)
        self.layout.addWidget(self.throttleBar)
        self.layout.addWidget(self.wheel)

        self.apply_scaling(settings['Scale'].slider.value())

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
        stripeWidth = w * 0.01
        stripeRect = QRectF(0, 0, stripeWidth, h)
        painter.fillRect(stripeRect, QColor(0, 0, 255, 200))

        painter.end()
    
    def apply_scaling(self, scale):
        super().apply_scaling(scale)

        sf = scale / 100
        newWidth = int(self.baseWidth * sf)

        self.layout.setContentsMargins(newWidth * 0.02, 0, 0, 0)
        self.layout.setSpacing(newWidth * 0.012)

        self.graph.setFixedSize(300 * sf, 100 * sf)
        self.brakeBar.setFixedSize(20 * sf, 100 * sf)
        self.throttleBar.setFixedSize(20 * sf, 100 * sf)
        self.wheel.setFixedSize(100 * sf, 100 * sf)
