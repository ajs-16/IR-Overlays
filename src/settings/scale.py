from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class Scale(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("scale_setting_widget")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.label = QLabel("Scale")
        self.label.setFont(QFont("Roboto", 10))
        self.label.setStyleSheet("color: #babdc3;")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(150)
        self.slider.setValue(100)
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

    def get_scale(self):
        return self.slider.value() / 100.0

    def set_scale(self, value):
        self.slider.setValue(int(value * 100))
