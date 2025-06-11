from unittest.mock import MagicMock, patch
from PySide6.QtCore import QObject
from src.data.worker import IRacingDataWorker

class TestIRacingDataWorker:
    def test_init(self):
        worker = IRacingDataWorker()
        assert isinstance(worker, QObject)
        assert worker.connected is False

    @patch('src.data.worker.irsdk.IRSDK')
    def test_update_connection_connects(self, mock_irsdk):
        mockIR = MagicMock()
        mockIR.startup.return_value = True
        mockIR.is_connected = True
        mockIR.is_initialized = True
        mock_irsdk.return_value = mockIR

        worker = IRacingDataWorker()
        connectionChanged = False
        
        def on_connection_changed(state):
            nonlocal connectionChanged
            connectionChanged = state
            
        worker.connectionChanged.connect(on_connection_changed)

        worker.update_connection()
        assert worker.connected is True
        assert connectionChanged is True
        mockIR.startup.assert_called_once()

    def test_convert_gear(self):
        assert IRacingDataWorker.convert_gear(-1) == "R"
        assert IRacingDataWorker.convert_gear(0) == "N"
        assert IRacingDataWorker.convert_gear(1) == "1"
        assert IRacingDataWorker.convert_gear(2) == "2"
