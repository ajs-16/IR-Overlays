from enum import Enum
from overlays.input_telemetry import InputTelemetryOverlay
from overlays.radar import RadarOverlay
from settings.scale import Scale
from settings.range import Range

class OverlayType(Enum):
    INPUT_TELEMETRY  = ("Input Telemetry", InputTelemetryOverlay, [Scale])
    RADAR            = ("Radar", RadarOverlay, [Scale, Range])

    def __init__(self, label, widget_cls, settings):
        self.label = label
        self.widget_cls = widget_cls
        self.settings = settings
