import datetime
import pickle
from json import JSONEncoder


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


@auto_str
class ProcessEvent:
    def __init__(self, proc, now, is_killed):
        self.event = {'name': str(proc.info['name']), 'pid': str(proc.info['pid']),
                      'cpu_times': str(proc.info['cpu_times']),
                      'memory_percent': str(proc.info['memory_percent']),
                      'memory_info': str(proc.info['memory_info']),
                      'io_counters': str(proc.info['io_counters']),
                      'time': (str(now)),
                      "is_killed": is_killed}

    def __hash__(self):
        return self.event["pid"]

    def __eq__(self, other):
        return self.event["pid"] == other.event["pid"]

    def __ge__(self, other):
        return self.event["pid"] > other.event["pid"]


class GenericEvent:
    def __init__(self):
        self.event = {
            'x': 0,
            'y': 0,
            'dx': 0,
            'dy': 0,
            'time': str(datetime.datetime.now()),
            'button': "",
            "pressed": "",
            "key": ""
        }

    def copy(self, event):
        for attr, value in event.__dict__.items():
            self.event[attr] = value if type(value) is int else str(value)
            self.event["name"] = event.__class__.__name__


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
