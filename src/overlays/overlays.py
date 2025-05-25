from enum import Enum
from overlays.input_telemetry import InputTelemetryOverlay
from overlays.radar import RadarOverlay

class OverlayType(Enum):
    INPUT_TELEMETRY  = ("Input Telemetry",    InputTelemetryOverlay)
    RADAR            = ("Radar",              RadarOverlay)

    def __init__(self, label, widget_cls):
        self.label      = label
        self.widget_cls = widget_cls
