from enum import Enum
from overlays.input_telemetry import InputTelemetryOverlay

class OverlayType(Enum):
    INPUT_TELEMETRY  = ("Input Telemetry",    InputTelemetryOverlay)
    LAPTIMES         = ("Laptimes",           None)
    LAPTIME_DELTA    = ("Laptime Delta",      None)
    STANDINGS        = ("Standings",          None)
    RELATIVES        = ("Relatives",          None)
    RADAR            = ("Radar",              None)

    def __init__(self, label, widget_cls):
        self.label      = label
        self.widget_cls = widget_cls
