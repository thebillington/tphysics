import math
from js import OffscreenCanvas
from pyodide.ffi import create_proxy


def _normalize_color(c):
    if isinstance(c, str):
        return c.replace(" ", "")
    return c

_canvas = None
_ctx = None
_canvas_width = 800
_canvas_height = 700
_bgcolor = "grey"
_screen_instance = None

_keydown_handlers = {}
_keyup_handlers = {}
_click_handlers = []


def _init(width, height):
    global _canvas, _ctx, _canvas_width, _canvas_height
    _canvas = OffscreenCanvas.new(width, height)
    _ctx = _canvas.getContext("2d")
    _canvas_width = width
    _canvas_height = height
    _clear_screen()
    _flush()


def _flush():
    global _canvas, _ctx
    if _ctx:
        from js import self as js_self
        width = int(_canvas_width)
        height = int(_canvas_height)
        image_data = _ctx.getImageData(0, 0, width, height)
        js_self.sendFrame(image_data)
        _ctx.clearRect(0, 0, width, height)


def _resize(width, height):
    global _canvas_width, _canvas_height
    _canvas_width = width
    _canvas_height = height


def _clear_screen():
    if _ctx:
        _ctx.fillStyle = _normalize_color(_bgcolor)
        _ctx.fillRect(0, 0, _canvas_width, _canvas_height)


def _tcx(x):
    return x + _canvas_width / 2


def _tcy(y):
    return _canvas_height / 2 - y


def _handle_keydown(key):
    if key in _keydown_handlers:
        for handler in _keydown_handlers[key]:
            handler()


def _handle_keyup(key):
    if key in _keyup_handlers:
        for handler in _keyup_handlers[key]:
            handler()


def _handle_click(canvas_x, canvas_y, button):
    turtle_x = canvas_x - _canvas_width / 2
    turtle_y = _canvas_height / 2 - canvas_y
    for handler in _click_handlers:
        handler(turtle_x, turtle_y)


class Turtle:
    def __init__(self):
        self._x = 0.0
        self._y = 0.0
        self._heading = 0.0
        self._pen_down = True
        self._pen_color = "black"
        self._fill_color = "black"
        self._filling = False
        self._fill_points = []
        self._visible = True

    def penup(self):
        self._pen_down = False

    def pendown(self):
        self._pen_down = True

    def isdown(self):
        return self._pen_down

    def goto(self, x, y=None):
        if y is None:
            x, y = x
        if _ctx and self._pen_down:
            _ctx.beginPath()
            _ctx.moveTo(_tcx(self._x), _tcy(self._y))
            _ctx.lineTo(_tcx(x), _tcy(y))
            _ctx.strokeStyle = _normalize_color(self._pen_color)
            _ctx.lineWidth = 1
            _ctx.stroke()
        self._x = float(x)
        self._y = float(y)
        if self._filling:
            self._fill_points.append((self._x, self._y))

    def setpos(self, x, y=None):
        self.goto(x, y)

    def setposition(self, x, y=None):
        self.goto(x, y)

    def forward(self, d):
        rad = math.radians(self._heading)
        x = self._x + d * math.cos(rad)
        y = self._y + d * math.sin(rad)
        self.goto(x, y)

    def fd(self, d):
        self.forward(d)

    def backward(self, d):
        self.forward(-d)

    def bk(self, d):
        self.forward(-d)

    def right(self, angle):
        self._heading = (self._heading - angle) % 360

    def rt(self, angle):
        self.right(angle)

    def left(self, angle):
        self._heading = (self._heading + angle) % 360

    def lt(self, angle):
        self.left(angle)

    def setheading(self, angle):
        self._heading = angle % 360

    def seth(self, angle):
        self.setheading(angle)

    def color(self, *args):
        if len(args) == 1:
            self._pen_color = args[0]
            self._fill_color = args[0]
        elif len(args) >= 2:
            self._pen_color = args[0]
            self._fill_color = args[1]
        return self._pen_color

    def pencolor(self, c=None):
        if c is not None:
            self._pen_color = c
        return self._pen_color

    def fillcolor(self, c=None):
        if c is not None:
            self._fill_color = c
        return self._fill_color

    def begin_fill(self):
        self._filling = True
        self._fill_points = [(self._x, self._y)]

    def end_fill(self):
        if self._filling and _ctx:
            if len(self._fill_points) >= 3:
                _ctx.beginPath()
                _ctx.moveTo(_tcx(self._fill_points[0][0]), _tcy(self._fill_points[0][1]))
                for px, py in self._fill_points[1:]:
                    _ctx.lineTo(_tcx(px), _tcy(py))
                _ctx.closePath()
            else:
                _ctx.closePath()
            _ctx.fillStyle = _normalize_color(self._fill_color)
            _ctx.fill()
        self._filling = False
        self._fill_points = []

    def circle(self, radius, extent=None, steps=None):
        if not _ctx:
            return
        cx = _tcx(self._x)
        cy = _tcy(self._y) - radius
        r = abs(radius)
        _ctx.beginPath()
        _ctx.arc(cx, cy, r, 0, 2 * math.pi)
        if self._pen_down:
            _ctx.strokeStyle = _normalize_color(self._pen_color)
            _ctx.stroke()
        if self._filling:
            _ctx.fillStyle = _normalize_color(self._fill_color)
            _ctx.fill()

    def dot(self, size=None, color=None):
        if not _ctx:
            return
        r = size / 2 if size else 2
        _ctx.beginPath()
        _ctx.arc(_tcx(self._x), _tcy(self._y), r, 0, 2 * math.pi)
        _ctx.fillStyle = _normalize_color(color if color else self._pen_color)
        _ctx.fill()

    def write(self, text, move=False, align="left", font=("Arial", 12, "normal")):
        if not _ctx:
            return
        family = font[0] if len(font) > 0 else "Arial"
        size = font[1] if len(font) > 1 else 12
        _ctx.font = f"{size}px {family}"
        _ctx.fillStyle = _normalize_color(self._pen_color)
        _ctx.textBaseline = "middle"
        _ctx.textAlign = align
        _ctx.fillText(str(text), _tcx(self._x), _tcy(self._y))

    def clear(self):
        _clear_screen()

    def hideturtle(self):
        self._visible = False

    def ht(self):
        self.hideturtle()

    def showturtle(self):
        self._visible = True

    def st(self):
        self.showturtle()

    def isvisible(self):
        return self._visible

    def shape(self, name=None):
        return "classic"

    def speed(self, s):
        pass

    @property
    def xcor(self):
        return self._x

    @property
    def ycor(self):
        return self._y

    def position(self):
        return (self._x, self._y)

    def pos(self):
        return (self._x, self._y)

    def heading(self):
        return self._heading

    def distance(self, x, y=None):
        if y is None:
            x, y = x
        return math.sqrt((self._x - x)**2 + (self._y - y)**2)

    def towards(self, x, y=None):
        if y is None:
            x, y = x
        return math.degrees(math.atan2(y - self._y, x - self._x)) % 360

    def clone(self):
        t = Turtle()
        t._x = self._x
        t._y = self._y
        t._heading = self._heading
        t._pen_down = self._pen_down
        t._pen_color = self._pen_color
        t._fill_color = self._fill_color
        t._visible = self._visible
        return t

    def getpen(self):
        return self

    def getscreen(self):
        return _screen_instance


class Screen:
    def __init__(self):
        global _screen_instance
        _screen_instance = self

    def title(self, name):
        pass

    def bgcolor(self, colour):
        global _bgcolor
        _bgcolor = colour
        _clear_screen()

    def setup(self, width, height):
        global _canvas_width, _canvas_height
        if width == 1.0 and height == 1.0:
            pass
        else:
            _canvas_width = int(width)
            _canvas_height = int(height)

    def tracer(self, arg1, arg2=None):
        pass

    def update(self):
        _flush()

    def delay(self, d):
        pass

    def onclick(self, f, btn=1):
        _click_handlers.append(f)

    def onkey(self, f, key):
        if key not in _keydown_handlers:
            _keydown_handlers[key] = []
        _keydown_handlers[key].append(f)

    def onkeypress(self, f, key):
        if key not in _keydown_handlers:
            _keydown_handlers[key] = []
        _keydown_handlers[key].append(f)

    def onkeyrelease(self, f, key):
        if key not in _keyup_handlers:
            _keyup_handlers[key] = []
        _keyup_handlers[key].append(f)

    def listen(self):
        pass

    def window_width(self):
        return _canvas_width

    def window_height(self):
        return _canvas_height

    def addshape(self, name, shape=None):
        pass

    def bye(self):
        pass

    def exitonclick(self):
        pass

    def resetscreen(self):
        pass

    def clearscreen(self):
        _clear_screen()


def done():
    pass


def mainloop():
    pass


def bye():
    pass


def exitonclick():
    pass


def clear():
    _clear_screen()


def bgcolor(color):
    global _bgcolor
    _bgcolor = color
