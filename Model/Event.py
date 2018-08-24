import datetime
from json import JSONEncoder
import pickle


def _default(self, obj):
    return {'_python_object': pickle.dumps(obj)}


JSONEncoder.default = _default  # Replace with the above.


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


class Event:
    def __init__(self):
        self.time = str(datetime.datetime.now())


@auto_str
class MoveEvent(Event):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y


@auto_str
class ClickEvent(Event):
    def __init__(self, x, y, button, pressed):
        super().__init__()
        self.x = x
        self.y = y
        self.button = button
        self.pressed = pressed


@auto_str
class ScrollEvent(Event):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


@auto_str
class KeyPressEvent(Event):
    def __init__(self, key):
        super().__init__()
        try:
            self.key = str(key.char)
        except AttributeError:
            self.key = str(key)


@auto_str
class KeyReleaseEvent(Event):
    def __init__(self, key):
        super().__init__()
        try:
            self.key = str(key.char)
        except AttributeError:
            self.key = str(key)
