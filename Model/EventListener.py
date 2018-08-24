from Model.Event import *


class EventListener:
    def __init__(self, q):
        self.q = q

    def on_move(self, x, y):
        # print('Pointer moved to {0}'.format(
        #     (x, y)))
        self.q.put(MoveEvent(x, y))

    def on_click(self, x, y, button, pressed):
        print('{0} - {1} at {2}'.format(button,
                                        'Pressed' if pressed else 'Released',
                                        (x, y)))
        self.q.put(ClickEvent(x, y, button, pressed))

    def on_scroll(self, x, y, dx, dy):
        print('Scrolled {0}'.format(
            (x, y)) + 'and Moved {0}'.format(
            (dx, dy)))
        self.q.put(ScrollEvent(x, y, dx, dy))

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
        self.q.put(KeyPressEvent(key))

    def on_release(self, key):
        print('{0} released'.format(
            key))
        self.q.put(KeyReleaseEvent(key))
