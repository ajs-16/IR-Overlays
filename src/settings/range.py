from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from state import state

class Range(QWidget):
    rangeChanged = Signal(int)

    def __init__(self, overlayLabel):
        super().__init__()
        self.settingName = "Range"
        self.setObjectName(f"{overlayLabel}_range_setting")
        self.overlayLabel = overlayLabel

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.label = QLabel(self.settingName)
        self.label.setFont(QFont("Roboto", 10))
        self.label.setStyleSheet("color: #babdc3;")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(50)
        self.slider.setValue(state.value(f"{self.overlayLabel}/range", defaultValue=30, type=int))
        self.slider.valueChanged.connect(self._update_state)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #404958;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #5aa0f2;
            }
        """)
        layout.addWidget(self.slider)

    def _update_state(self):
        state.setValue(f"{self.overlayLabel}/range", self.slider.value())
        self.rangeChanged.emit(self.slider.value())
