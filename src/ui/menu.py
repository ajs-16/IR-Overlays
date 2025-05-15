from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QCheckBox, QVBoxLayout, QWidget, QLabel, QFrame, QSizePolicy
from overlays.overlays import OverlayType

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlay Menu")
        self.setFixedSize(QSize(250, 400))

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)
        
        # Title
        title = QLabel("Select Overlays")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(title)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)
        
        # Checkboxes
        for overlay in OverlayType:
            checkbox = QCheckBox(overlay.label, self)
            if overlay.widget_cls: checkbox.overlay = overlay.widget_cls()
            checkbox.stateChanged.connect(self.toggle_overlay)
            layout.addWidget(checkbox)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def toggle_overlay(self):
        sender = self.sender()

        if sender.isChecked(): sender.overlay.show()
        else: sender.overlay.hide()
