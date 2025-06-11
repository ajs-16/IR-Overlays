import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtCore import Qt
from src.ui.menu_item import MenuItem

@pytest.fixture
def mock_overlay():
    overlay = MagicMock()
    overlay.label = "TestOverlay"
    overlay.settings = []
    overlay.widget_cls.return_value = MagicMock()
    return overlay

@pytest.fixture
def mock_worker():
    return MagicMock()

def test_initialisation(qtbot, mock_overlay, mock_worker):
    with patch("src.ui.menu_item.state") as mockState:
        mockState.value.return_value = False
        menuItem = MenuItem(mock_overlay, mock_worker)
        qtbot.addWidget(menuItem)
        
        assert menuItem.overlayLabel == "TestOverlay"
        assert menuItem.expanded is False
        assert menuItem.checkbox.isChecked() is False
