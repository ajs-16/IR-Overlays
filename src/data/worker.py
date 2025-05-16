import irsdk

class IRacingDataWorker:
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.connected = False

    def connect(self):
        # If marked as connected, check if the connection is still alive
        if self.connected:
            if not self.ir.is_connected and self.ir.is_initialized:
                self.ir.shutdown()
                self.connected = False
            return
        
        # If not connected, try to connect
        if not self.ir.startup():
            return
        
        # Startup successful, record connection
        if self.ir.is_connected and self.ir.is_initialized:
            self.connected = True

