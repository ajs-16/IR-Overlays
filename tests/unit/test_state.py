from PySide6.QtCore import QSettings
from src.state import state

def test_state_instance():
    assert isinstance(state, QSettings)
    assert state.organizationName() == "IRacingOverlays"
    assert state.applicationName() == "IRO"
