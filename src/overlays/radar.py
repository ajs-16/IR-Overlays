from .base_overlay import BaseOverlay
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QPainterPath
from PySide6.QtCore import Qt, QRect

class RadarOverlay(BaseOverlay):
    def __init__(self, worker, settings):
        super().__init__(settings, base_width=150, base_height=150)
        self.apply_scaling(settings['Scale'].slider.value())
        self.range = settings['Range'].slider.value()
        self.telemetry = {}

        worker.updatedTelemetry.connect(self._update_radar)
        settings['Range'].rangeChanged.connect(self._update_range)        

    def paintEvent(self, event):
        w = self.width()
        h = self.height()
        carH = 4

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(0, 0, w, h, QColor(0, 0, 0, 1))
        painter.end()

        self.draw_grid()
        self.draw_car()

        if not self.telemetry:
            return
        
        adjustedDistAhead = self.telemetry['CarDistAhead'] - (carH / 2)
        adjustedDistBehind = self.telemetry['CarDistBehind'] - (carH / 2)

        # Ahead/Behind warning lines
        if adjustedDistAhead <= self.range / 2 and adjustedDistAhead > carH / 2:
            self.draw_ab_warning(
                adjustedDistAhead
            )
        
        if adjustedDistBehind <= self.range / 2 and adjustedDistBehind > carH / 2:
            self.draw_ab_warning(
                -adjustedDistBehind
            )

        # Draw Right/Left warnings
        if self.telemetry['CarLeftRight'] in [3, 6, 4]: # Car Right
            self.draw_lr_warning('right')
        
        if self.telemetry['CarLeftRight'] in [2, 5, 4]: # Car Left
            self.draw_lr_warning('left')

    def draw_grid(self):
        w = self.width()
        h = self.height()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
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
        h = self.height()
        PxPerM = h / self.range
        carW = 2 * PxPerM
        carH = 4 * PxPerM

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
    
    def draw_ab_warning(self, distance):
        w = self.width()
        h = self.height()
        PxPerM = h / self.range

        yPos = int(h / 2 - distance * PxPerM)
        ahead = distance > 0

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient()
        gradient.setStart(0, yPos)

        path = QPainterPath()
        path.moveTo(0, yPos)
        path.lineTo(w, yPos)

        if ahead:
            gradient.setFinalStop(0, 0)
            path.arcTo(0, 0, w, yPos*2, 0, 180)
        else:
            gradient.setFinalStop(0, h)
            path.arcTo(0, 2*yPos-h, w, (h-yPos)*2, 0, -180)

        path.closeSubpath()

        gradient.setColorAt(0, QColor(255, 255, 0, 100))
        gradient.setColorAt(1, QColor(255, 255, 0, 0))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)

        painter.drawPath(path)  
        painter.end()
    
    def draw_lr_warning(self, side):
        w, h = self.width(), self.height()
        PxPerM = h / self.range
        carW, carH = 2 * PxPerM, 4 * PxPerM
        centerX, centerY = w / 2, h / 2

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if side == 'right':
            xPos = centerX + carW/2
            rect = QRect(
                int(xPos),
                int(centerY - carH/2),
                int(w - xPos),
                int(carH)
            )
            
            gradient = QLinearGradient(xPos, 0, w, 0)
            gradient.setColorAt(0, QColor(255, 0, 0, 100))
            gradient.setColorAt(1, QColor(255, 0, 0, 0))

        if side == 'left':
            xPos = centerX - carW/2
            rect = QRect(
                0,
                int(centerY - carH/2),
                int(xPos),
                int(carH)
            )

            gradient = QLinearGradient(0, 0, xPos, 0)
            gradient.setColorAt(0, QColor(255, 0, 0, 0))
            gradient.setColorAt(1, QColor(255, 0, 0, 100))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        painter.end()

    def _update_range(self, value):
        self.range = value
        self.update()

    def _update_radar(self, telemetry):
        self.telemetry = telemetry
        self.update()
