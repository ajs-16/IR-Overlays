from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

class BaseOverlay(QWidget):
    def __init__(self, settings, base_width, base_height):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.baseWidth = base_width
        self.baseHeight = base_height

        self._drag_pos = None
        
        settings['Scale'].scaleChanged.connect(self.apply_scaling)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def apply_scaling(self, scale):
        self.sf = scale / 100
        self.newWidth = int(self.baseWidth * self.sf)
        self.newHeight = int(self.baseHeight * self.sf)

        self.setFixedSize(self.newWidth, self.newHeight)
