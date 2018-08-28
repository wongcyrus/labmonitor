# https://github.com/moses-palmer/pynput/issues/52
import getopt
import json
import multiprocessing
import sys
from queue import Queue
from threading import Thread

import requests
from pynput import keyboard
from pynput import mouse

from Model.EventListener import EventListener
from Model.Watcher import Watcher

q = Queue()
batch_limit = 50


def worker(api, key):
    while True:
        queue_size = q.qsize()
        if queue_size > batch_limit:
            print("Batch processing for " + str(queue_size) + " events")
            events = []
            for i in range(queue_size):
                item = q.get()
                data = {}
                for attr, value in item.__dict__.items():
                    data[attr] = value
                data["event"] = item.__class__.__name__
                events.append(data)
                q.task_done()

            try:
                print("Json")
                data = json.dumps(events).encode('utf8')
                print(data)

                response = requests.post("https://" + api + "/event", data=data,
                                         headers={"x-api-key": key})
                if response.ok:
                    print(response.json())
                else:
                    print(response.status_code)
                    print(response.reason)
            except Exception as e:
                print(e)
                print(events)


def file_monitor(api, key):
    w = Watcher(api, key, "/home/osboxes/PycharmProjects/ite3101_introduction_to_programming/lab")
    w.run()


def input_monitor(api, key):
    t = Thread(target=worker, args=(api, key,))
    t.start()

    event_listener = EventListener(q)

    with mouse.Listener(on_move=event_listener.on_move, on_click=event_listener.on_click,
                        on_scroll=event_listener.on_scroll) as listener:
        with keyboard.Listener(on_press=event_listener.on_press, on_release=event_listener.on_release) as listener:
            listener.join()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "a:k:")
    except getopt.GetoptError:
        print('monitor.py -a <url> -k <apikey>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('monitor.py -a <url> -k <apikey>')
            sys.exit()
        elif opt == '-a':
            global api
            api = arg
        elif opt == '-k':
            global key
            key = arg

    api = api.replace("https://", "").replace("http://", "")
    print('api is ', api)
    print('key is ', key)

    if api is None or key is None:
        sys.exit()

    jobs = [multiprocessing.Process(target=file_monitor, args=(api, key,)),
            multiprocessing.Process(target=input_monitor, args=(api, key,))]

    # Start the processes (i.e. calculate the random number lists)
    for j in jobs:
        j.start()

    # Ensure all of the processes have finished
    for j in jobs:
        j.join()

    print("List processing complete.")


if __name__ == '__main__':
    main(sys.argv[1:])
