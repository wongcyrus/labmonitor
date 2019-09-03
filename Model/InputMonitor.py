import json
import threading
from queue import Queue
from time import sleep

import requests

from Model.Event import GenericEvent


class InputMonitor(threading.Thread):

    def __init__(self, api: str, key: str, queue: Queue):
        super().__init__()
        self.name = "InputMonitor"
        self.api = api
        self.key = key
        self.queue = queue
        self.batch_limit = 1000

    def run(self):
        while True:
            sleep(1)
            queue_size = self.queue.qsize()
            if queue_size >= self.batch_limit:
                print("Batch processing for " + str(queue_size) + " events")
                events = []
                for i in range(queue_size):
                    item = self.queue.get()
                    generic_event = GenericEvent()
                    generic_event.copy(item)
                    events.append(generic_event.event)
                    self.queue.task_done()

                try:
                    data = json.dumps(events).encode('utf8')
                    response = requests.post("https://" + self.api + "/event", data=data,
                                             headers={"x-api-key": self.key})
                    if response.ok:
                        print(response.json())
                    else:
                        print(response.status_code)
                        print(response.reason)
                except Exception as e:
                    print(e)
                    print(len(events))
                    print(events)
