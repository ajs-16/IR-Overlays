from .base_overlay import BaseOverlay
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient
from PySide6.QtCore import Qt, QRect

class RadarOverlay(BaseOverlay):
    def __init__(self, worker, settings):
        super().__init__(settings, base_width=150, base_height=150)
        self.apply_scaling(settings['Scale'].slider.value())
        self.range = 15 # Meters
        self.telemetry = {}

        worker.updatedTelemetry.connect(self._update_radar)

    def paintEvent(self, event):
        w = self.width()
        h = self.height()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(0, 0, w, h, QColor(0, 0, 0, 1))
        painter.end()

        self.draw_grid()
        self.draw_car()

        if not self.telemetry:
            return
        
        # Ahead/Behind warning lines
        if self.telemetry['CarDistAhead'] <= self.range / 2:
            self.DrawABWarning(
                self.telemetry['CarDistAhead']
            )
        
        if self.telemetry['CarDistBehind'] <= self.range / 2:
            self.DrawABWarning(
                -self.telemetry['CarDistBehind']
            )

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
    
    def DrawABWarning(self, distance):
        w = self.width()
        h = self.height()
        PxPerM = h / self.range
    
        yPos = int(h / 2 - distance * PxPerM)
        ahead = distance > 0
    
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
    
        gradient = QLinearGradient()
        gradient.setStart(0, yPos)

        if ahead:
            gradient.setFinalStop(0, 0)
            rect = QRect(0, 0, w, yPos)
        else:
            gradient.setFinalStop(0, h)
            rect = QRect(0, yPos, w, h - yPos)
        
        gradient.setColorAt(0, QColor(255, 255, 0, 100))
        gradient.setColorAt(1, QColor(255, 255, 0, 0))
    
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)
    
        painter.end()

    def _update_radar(self, telemetry):
        self.telemetry = telemetry
        self.update()
