# https://github.com/moses-palmer/pynput/issues/52
import getopt
import multiprocessing
import sys
from queue import Queue

from pynput import keyboard
from pynput import mouse

from Model.EventListener import EventListener
from Model.InputMonitor import InputMonitor
from Model.ProcessMonitor import ProcessMonitor
from Model.Screenshots import Screenshots
from Model.Watcher import Watcher

q = Queue()


def file_monitor(api, key, monitor_dir, using_pycharm):
    w = Watcher(api, key, monitor_dir, using_pycharm)
    w.run()


def input_monitor(api, key):
    q = Queue()
    im = InputMonitor(api, key, q)
    im.start()

    event_listener = EventListener(q)

    with mouse.Listener(on_move=event_listener.on_move, on_click=event_listener.on_click,
                        on_scroll=event_listener.on_scroll) as listener:
        with keyboard.Listener(on_press=event_listener.on_press, on_release=event_listener.on_release) as listener:
            listener.join()
    im.join()


def screenshots(api, key):
    s = Screenshots(api, key)
    s.start()
    s.join()


def process_monitor(api, key):
    pm = ProcessMonitor(api, key)
    pm.start()
    pm.join()


def main(argv):
    instruction = 'monitor.py -m <absolute path directory> -a <url> -k <apikey>'

    api = None
    key = None
    monitor_dir = None
    using_pycharm = True

    try:
        opts, args = getopt.getopt(argv, "m:a:k:t:")

    except getopt.GetoptError:
        print(instruction)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(instruction)
            sys.exit()
        elif opt == '-m':
            monitor_dir = arg
        elif opt == '-a':
            api = arg
            api = api.replace("https://", "").replace("http://", "")
        elif opt == '-k':
            key = arg
        elif opt == '-t':
            using_pycharm = False

    print('api: ', api)
    print('key: ', key)
    print('monitoring directory: ', monitor_dir)
    print('Using PyCharm: ', using_pycharm)

    if api is None or key is None:
        sys.exit()

    jobs = [multiprocessing.Process(target=file_monitor, args=(api, key, monitor_dir, using_pycharm,)),
            multiprocessing.Process(target=input_monitor, args=(api, key,)),
            multiprocessing.Process(target=screenshots, args=(api, key,)),
            multiprocessing.Process(target=process_monitor, args=(api, key,))
            ]

    # Start the processes (i.e. calculate the random number lists)
    for j in jobs:
        j.start()

    # Ensure all of the processes have finished
    for j in jobs:
        j.join()


if __name__ == '__main__':
    main(sys.argv[1:])
