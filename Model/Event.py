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
        self.time: str = str(datetime.datetime.now())


@auto_str
class MoveEvent(Event):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x: int = x
        self.y: int = y


@auto_str
class ClickEvent(Event):
    def __init__(self, x: int, y: int, button, pressed):
        super().__init__()
        self.x: int = x
        self.y: int = y
        self.button: str = button
        self.pressed: str = pressed


@auto_str
class ScrollEvent(Event):
    def __init__(self, x: int, y: int, dx: int, dy: int):
        super().__init__()
        self.x: int = x
        self.y: int = y
        self.dx: int = dx
        self.dy: int = dy


@auto_str
class KeyPressEvent(Event):
    def __init__(self, key):
        super().__init__()
        try:
            self.key: str = str(key.char)
        except AttributeError:
            self.key: str = str(key)


@auto_str
class KeyReleaseEvent(Event):
    def __init__(self, key):
        super().__init__()
        try:
            self.key: str = str(key.char)
        except AttributeError:
            self.key: str = str(key)
