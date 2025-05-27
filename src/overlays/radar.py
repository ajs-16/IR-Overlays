from PySide6.QtWidgets import QWidget

class RadarOverlay(QWidget):
    def __init__(self, IRWorker, settings):
        super().__init__()
