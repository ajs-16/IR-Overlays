import pytest
from unittest.mock import MagicMock, patch
from src.overlays.radar import RadarOverlay

@pytest.fixture
def mock_worker():
    worker = MagicMock()
    worker.updatedTelemetry = MagicMock()
    return worker

@pytest.fixture
def mock_settings():
    scale = MagicMock()
    scale.slider = MagicMock()
    scale.slider.value.return_value = 100
    scale.settingName = "Scale"
    scale.scaleChanged = MagicMock()
    
    rangeSetting = MagicMock()
    rangeSetting.slider = MagicMock()
    rangeSetting.slider.value.return_value = 30
    rangeSetting.settingName = "Range"
    rangeSetting.rangeChanged = MagicMock()
    
    return {'Scale': scale, 'Range': rangeSetting}

def test_radar_overlay_initialisation(qtbot, mock_worker, mock_settings):
    radar = RadarOverlay(mock_worker, mock_settings)
    qtbot.addWidget(radar)
    
    assert radar.range == 30
    assert radar.telemetry == {}
    assert mock_worker.updatedTelemetry.connect.called
    assert mock_settings['Range'].rangeChanged.connect.called

def test_radar_overlay_update_telemetry(qtbot, mock_worker, mock_settings):
    radar = RadarOverlay(mock_worker, mock_settings)
    qtbot.addWidget(radar)
    
    testData = {
        'CarDistAhead': 10,
        'CarDistBehind': 5,
        'CarLeftRight': 3
    }
    
    with patch.object(radar, 'update') as mockUpdate:
        radar._update_radar(testData)
        assert radar.telemetry == testData
        mockUpdate.assert_called_once()
