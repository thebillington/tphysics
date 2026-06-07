from js import OffscreenCanvas

_measure_canvas = OffscreenCanvas.new(1, 1)
_measure_ctx = _measure_canvas.getContext("2d")


class Font:
    def __init__(self, font=("Arial", 12, "normal")):
        self.family = font[0] if len(font) > 0 else "Arial"
        self.size = font[1] if len(font) > 1 else 12
        self.style = font[2] if len(font) > 2 else "normal"

    def metrics(self, metric=None):
        _measure_ctx.font = f"{self.size}px {self.family}"
        if metric == "ascent":
            return self.size
        elif metric == "descent":
            return int(self.size * 0.2)
        elif metric == "linespace":
            return int(self.size * 1.2)
        return {
            "ascent": self.size,
            "descent": int(self.size * 0.2),
            "linespace": int(self.size * 1.2),
        }

    def measure(self, text):
        _measure_ctx.font = f"{self.size}px {self.family}"
        return _measure_ctx.measureText(text).width
