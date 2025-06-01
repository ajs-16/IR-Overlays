from PySide6.QtCore import QPoint
from PySide6.QtWidgets import (
    QWidget, QCheckBox, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFrame
)
from PySide6.QtGui import QFont
import qtawesome as qta
from state import state

class MenuItem(QWidget):
    def __init__(self, overlay, IRWorker):
        super().__init__()
        self.overlayLabel = overlay.label
        self.setObjectName(f"menu_item_{overlay.label}")
        self.expanded = False

        self.chevDown = qta.icon('fa5s.chevron-down', color='white', scale_factor=0.75)
        self.chevUp = qta.icon('fa5s.chevron-up', color='white', scale_factor=0.75)
        self.setStyleSheet("""
            background-color: #1f2a3c;
            border: 1px solid #404958;
            border-radius: 2px;
        """)
        self._init_ui()

        self.overlaySettings = {}
        self._load_settings(overlay.settings)

        self.overlayWidget = overlay.widget_cls(
            IRWorker,
            self.overlaySettings
        )

        self.checkbox.setChecked(state.value(f"{self.overlayLabel}/enabled", False, type=bool))

    def _init_ui(self):
        self.MainVLayout = QVBoxLayout(self)
        self.MainVLayout.setContentsMargins(0, 0, 0, 0)
        self.MainVLayout.setSpacing(0)

        self._create_top_row()
        self._create_dropdown()
        
        self.MainVLayout.addWidget(self.topRow)
        self.MainVLayout.addWidget(self.dropdownContent)

    def _create_top_row(self):
        self.topRow = QWidget()
        self.topLayout = QHBoxLayout(self.topRow)
        self.topLayout.setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self._toggle_overlay)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                border: none;
                padding-left: 8px;
                background: transparent;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #404958;
                border-radius: 3px;
                background-color: #2a3441;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #babdc3;
                background-color: #3a4551;
            }
            QCheckBox::indicator:checked {
                background-color: #4a90e2;
                border: 2px solid #4a90e2;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #5aa0f2;
                border: 2px solid #5aa0f2;
            }
        """)
        
        self.label = QLabel(self.overlayLabel)
        self.label.setFont(QFont("Roboto", 10))
        self.label.setStyleSheet("""
            color: #babdc3;
            border: none;
            padding: 8px;
            padding-left: 0px;
            background: transparent;
        """)

        self.dropdownBtn = QPushButton()
        self.dropdownBtn.setIcon(self.chevDown)
        self.dropdownBtn.setStyleSheet("""
            background:transparent;
            border:none;
            border-left: 1px solid #404958;
            border-radius: 0px;
            padding: 5px;
        """)
        self.dropdownBtn.clicked.connect(self.toggle_dropdown)

        self.topLayout.addWidget(self.checkbox)
        self.topLayout.addWidget(self.label)
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.dropdownBtn)

    def _create_dropdown(self):
        self.dropdownContent = QFrame()
        self.dropdownContent.setFrameStyle(QFrame.StyledPanel)
        self.dropdownLayout = QVBoxLayout(self.dropdownContent)
        self.dropdownContent.setStyleSheet("border: none;")
        self.dropdownContent.hide()

    def _load_settings(self, settings):
        for setting in settings:
            widget = setting(self.overlayLabel)
            self.overlaySettings[widget.settingName] = widget
            self.add_dropdown_item(widget)

    def add_dropdown_item(self, widget):
        self.dropdownLayout.addWidget(widget)

    def toggle_dropdown(self):
        self.expanded = not self.expanded
        self.dropdownContent.setVisible(self.expanded)
        self.dropdownBtn.setIcon(self.chevDown if not self.expanded else self.chevUp)

    def _toggle_overlay(self):
        sender = self.sender()

        if sender.isChecked():
            self.overlayWidget.move(state.value(f"{self.overlayLabel}/pos", defaultValue=QPoint(0, 0)))
            self.overlayWidget.show()
            state.setValue(f"{self.overlayLabel}/enabled", True)
        else:
            self.overlayWidget.hide()
            state.setValue(f"{self.overlayLabel}/enabled", False)
