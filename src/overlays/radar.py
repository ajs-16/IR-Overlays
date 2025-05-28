from .base_overlay import BaseOverlay

class RadarOverlay(BaseOverlay):
    def __init__(self, worker, settings):
        super().__init__(settings, base_width=500, base_height=500)
        self.apply_scaling(settings['Scale'].slider.value())
