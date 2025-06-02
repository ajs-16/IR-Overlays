import os
import sys
from PySide6.QtCore import QSize, Qt, QThread, QTimer, QPoint
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout,
    QWidget, QLabel, QFrame,
    QScrollArea
)
from PySide6.QtGui import QIcon, QPalette, QColor, QFont
from overlays.overlays import OverlayType
from data.worker import IRacingDataWorker
from .menu_item import MenuItem
from state import state

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IRO")

        if getattr(sys, "frozen", False):
            baseDir = sys._MEIPASS
        else:
            baseDir = "src"
    
        iconPath = os.path.join(baseDir, "assets", "IRO_LOGO.png")
        icon = QIcon(iconPath)
        self.setWindowIcon(icon)

        self.setFixedSize(QSize(250, 300))
        self.move(state.value("MainWindow/pos", QPoint(100, 100)))

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#181f2a"))
        self.setPalette(palette)

        # Data Worker Setup
        self.irThread = QThread()
        self.irWorker = IRacingDataWorker()
        self.irWorker.moveToThread(self.irThread)
        self.irThread.start()

        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.irWorker.process_data)
        self.updateTimer.start(16)

        # UI Setup
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: #666;
                border-radius: 4px;
            }
        """)

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)
        
        # Title
        title = QLabel("IRacing Overlays")
        title.setFont(QFont("Roboto", 13))
        title.setStyleSheet("color: #e0e3e7;")
        layout.addWidget(title)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #404958;")
        layout.addWidget(divider)
        
        # Menu Items
        for overlay in OverlayType:
            layout.addSpacing(8)
            layout.addWidget(
                MenuItem(
                    overlay,
                    self.irWorker
                )
            )
        
        scroll.setWidget(container)
        self.setCentralWidget(scroll)

    def closeEvent(self, event):
        for overlay in OverlayType:
            menuItem = self.findChild(QWidget, f"menu_item_{overlay.label}")
            state.setValue(f"{overlay.label}/pos", menuItem.overlayWidget.pos())

        state.setValue("MainWindow/pos", self.pos())

        self.irThread.quit()
        self.irThread.wait()

        super().closeEvent(event)
