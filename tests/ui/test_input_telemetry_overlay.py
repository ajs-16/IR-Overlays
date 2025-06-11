import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtCore import Qt
from src.overlays.input_telemetry import (
    InputTelemetryOverlay, TelemetryBar,
    TelemetryWheel, TelemetryGraph )

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
    
    return {'Scale': scale}

def test_input_telemetry_overlay_initialisation(qtbot, mock_worker, mock_settings):
    overlay = InputTelemetryOverlay(mock_worker, mock_settings)
    qtbot.addWidget(overlay)
    
    assert overlay.layout is not None
    assert overlay.graph is not None
    assert overlay.brakeBar is not None
    assert overlay.throttleBar is not None
    assert overlay.wheel is not None
    
    assert overlay.baseWidth == 470
    assert overlay.baseHeight == 110
    assert mock_settings['Scale'].scaleChanged.connect.called

def test_telemetry_bar_initialisation(qtbot, mock_worker):
    brakeBar = TelemetryBar('brake', Qt.red, mock_worker)
    qtbot.addWidget(brakeBar)
    
    assert brakeBar.pedal == 'brake'
    assert brakeBar._value == 0
    assert mock_worker.updatedTelemetry.connect.called
    
    with patch.object(brakeBar, 'update') as mockUpdate:
        testData = {'brake': 75}
        brakeBar.update_value(testData)
        
        assert brakeBar._value == 75
        mockUpdate.assert_called_once()

def test_telemetry_wheel_initialisation(qtbot, mock_worker):
    wheel = TelemetryWheel(mock_worker)
    qtbot.addWidget(wheel)
    
    assert wheel.gear == "N"
    assert wheel.speed == 0
    assert wheel.wheelAngle == 0.0
    assert mock_worker.updatedTelemetry.connect.called
    
    with patch.object(wheel, 'update') as mockUpdate:
        testData = {'gear': "4", 'speed': 120, 'wheelAngle': 0.25}
        wheel.update_metrics(testData)
        
        assert wheel.gear == "4"
        assert wheel.speed == 120
        assert wheel.wheelAngle == 0.25
        mockUpdate.assert_called_once()

def test_telemetry_graph_initialisation(qtbot, mock_worker):
    graph = TelemetryGraph(mock_worker)
    qtbot.addWidget(graph)
    
    assert graph._brakeBuffer is not None
    assert graph._throttleBuffer is not None
    assert graph._brakeLine is not None
    assert graph._throttleLine is not None
    assert mock_worker.updatedTelemetry.connect.called
    
    testData = {'throttle': 80, 'brake': 20}
    graph.update_graph(testData)
    
    assert list(graph._throttleBuffer) == [80]
    assert list(graph._brakeBuffer) == [20]

def test_input_telemetry_overlay_scaling(qtbot, mock_worker, mock_settings):
    overlay = InputTelemetryOverlay(mock_worker, mock_settings)
    qtbot.addWidget(overlay)
    
    assert overlay.width() == 470
    assert overlay.height() == 110
    
    with patch.object(overlay, 'setFixedSize') as mockSetSize:
        overlay.apply_scaling(125)
        
        assert overlay.sf == 1.25
        assert overlay.newWidth == 587
        assert overlay.newHeight == 137
        
        mockSetSize.assert_called_with(587, 137)
