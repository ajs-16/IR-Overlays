from PySide6.QtCore import QPoint
from PySide6.QtWidgets import (
    QWidget, QCheckBox, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFrame
)
from state import appState

class MenuItem(QWidget):
    def __init__(self, overlay, IRWorker):
        super().__init__()
        self.overlayLabel = overlay.label
        self.overlayWidget = overlay.widget_cls(IRWorker)
        self.setObjectName(f"menu_item_{overlay.label}")
        self.expanded = False

        self.MainVLayout = QVBoxLayout(self)
        self.MainVLayout.setContentsMargins(0, 0, 0, 0)
        self.MainVLayout.setSpacing(0)

        self.topRow = QWidget()
        self.topLayout = QHBoxLayout(self.topRow)
        self.topLayout.setContentsMargins(5, 5, 5, 5)

        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self._checkbox_toggled)
        
        self.label = QLabel(self.overlayLabel)
        
        self.dropdownBtn = QPushButton("▼")
        self.dropdownBtn.setFixedWidth(20)
        self.dropdownBtn.clicked.connect(self.toggle_dropdown)

        self.topLayout.addWidget(self.checkbox)
        self.topLayout.addWidget(self.label)
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.dropdownBtn)

        self.dropdownContent = QFrame()
        self.dropdownContent.setFrameStyle(QFrame.StyledPanel)
        self.dropdownLayout = QVBoxLayout(self.dropdownContent)
        self.dropdownContent.hide()

        self.MainVLayout.addWidget(self.topRow)
        self.MainVLayout.addWidget(self.dropdownContent)

        if appState.state.get(self.overlayLabel, None):
            self.checkbox.setChecked(appState.state[self.overlayLabel]['enabled'])
        else:
            appState.state[self.overlayLabel] = {
                'enabled': False,
                'pos': QPoint(0, 0)
            }

    def add_dropdown_item(self, widget):
        self.dropdownLayout.addWidget(widget)

    def toggle_dropdown(self):
        self.expanded = not self.expanded
        self.dropdownContent.setVisible(self.expanded)
        self.dropdownBtn.setText("▼" if not self.expanded else "▲")

    def _checkbox_toggled(self):
        print("toggled")
