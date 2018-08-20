# https://github.com/moses-palmer/pynput/issues/52
from queue import Queue

from pynput import keyboard
from pynput import mouse

from threading import Thread
import multiprocessing

from Model.EventListener import EventListener
from Model.Watcher import Watcher

q = Queue()


def worker():
    while True:
        queue_size = q.qsize()
        if queue_size > 10:
            print("Batch processing for " + str(queue_size) + " events")
            for i in range(queue_size):
                item = q.get()
                print("worker: " + str(item))
                q.task_done()


if __name__ == '__main__':
    def file_monitor():
        w = Watcher()
        w.run()


    def input_monitor():
        t = Thread(target=worker)
        t.start()

        event_listener = EventListener(q)

        with mouse.Listener(on_move=event_listener.on_move, on_click=event_listener.on_click,
                            on_scroll=event_listener.on_scroll) as listener:
            with keyboard.Listener(on_press=event_listener.on_press, on_release=event_listener.on_release) as listener:
                listener.join()


    jobs = [multiprocessing.Process(target=file_monitor), multiprocessing.Process(target=input_monitor)]

    # Start the processes (i.e. calculate the random number lists)
    for j in jobs:
        j.start()

    # Ensure all of the processes have finished
    for j in jobs:
        j.join()

    print("List processing complete.")
