import irsdk
from PySide6.QtCore import Signal, QObject

class IRacingDataWorker(QObject):
    updatedTelemetry = Signal(dict)
    connectionChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self.ir = irsdk.IRSDK()
        self.connected = False

    def update_connection(self):
        # If marked as connected, check if the connection is still alive
        if self.connected:
            if not self.ir.is_connected and self.ir.is_initialized:
                self.ir.shutdown()
                self.connected = False
                self.connectionChanged.emit(False)
            return
        
        # If not connected, try to connect
        if not self.ir.startup(test_file='src/data/data.bin'):
            return
        
        # Startup successful, record connection
        if self.ir.is_connected and self.ir.is_initialized:
            self.connected = True
            self.connectionChanged.emit(True)

    def process_data(self):
        self.update_connection()

        if self.connected:
            telemetry = {
                'throttle': self.ir['Throttle'],
                'brake': self.ir['Brake'],
            }

            self.updatedTelemetry.emit(telemetry)
