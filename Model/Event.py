def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


@auto_str
class MoveEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


@auto_str
class ClickEvent:
    def __init__(self, x, y, button, pressed):
        self.x = x
        self.y = y
        self.button = button
        self.pressed = pressed


@auto_str
class ScrollEvent:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


@auto_str
class KeyPressEvent:
    def __init__(self, key):
        try:
            self.key = str(key.char)
        except AttributeError:
            self.key = str(key)

@auto_str
class KeyReleaseEvent:
    def __init__(self, key):
        try:
            self.key = str(key.char)
        except AttributeError:
            self.key = str(key)
