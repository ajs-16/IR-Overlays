from PySide6.QtCore import QSize, Qt, QThread, QTimer
from PySide6.QtWidgets import (
    QMainWindow, QCheckBox, QVBoxLayout,
    QWidget, QLabel, QFrame, QSizePolicy,
    QScrollArea
)
from PySide6.QtGui import QIcon
from overlays.overlays import OverlayType
from data.worker import IRacingDataWorker
import pickle
from state import appState
from .menu_item import MenuItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IR Overlays")
        self.icon = QIcon()
        self.icon.addFile("src/assets/IR_LOGO.png")
        self.setWindowIcon(self.icon)
        self.setFixedSize(QSize(250, 300))

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
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
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
        layout = QVBoxLayout(container)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)
        
        # Title
        title = QLabel("Overlays")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(title)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)
        
        # Menu Items
        for overlay in OverlayType:
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
            appState.state[overlay.label]['pos'] = menuItem.overlayWidget.pos()

        self.irThread.quit()
        self.irThread.wait()

        with open('src/tmp/state.pickle', 'wb') as f:
            pickle.dump(appState.state, f)

        super().closeEvent(event)
