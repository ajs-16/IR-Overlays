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
        if not self.ir.startup():
            return
        
        # Startup successful, record connection
        if self.ir.is_connected and self.ir.is_initialized:
            self.connected = True
            self.connectionChanged.emit(True)

    @staticmethod
    def convert_gear(numericGear):
        if numericGear == -1:
            return "R"
        elif numericGear == 0:
            return "N"
        else:
            return str(numericGear)

    def process_data(self):
        self.update_connection()

        if self.connected:
            telemetry = {
                'throttle': round(self.ir['ThrottleRaw'] * 100),
                'brake': round(self.ir['BrakeRaw'] * 100),
                'gear': self.convert_gear(self.ir['Gear']),
                'speed': round(self.ir['Speed']),
                'wheelAngle': self.ir['SteeringWheelAngle']
            }

            self.updatedTelemetry.emit(telemetry)
