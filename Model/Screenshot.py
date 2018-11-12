import datetime
import json
import threading
from time import sleep

import psutil
import requests

from Model.Event import ProcessEvent


class ProcessMonitor(threading.Thread):

    def __init__(self, api: str, key: str):
        super().__init__()
        self.name = "ProcessMonitor"
        self.api = api
        self.key = key
        self.black_list_process = []

    def run(self):
        count = 0
        while True:
            running_process = []
            killed = False
            for proc in psutil.process_iter(
                    attrs=['pid', 'name', 'cpu_times', 'memory_percent', 'memory_info', 'io_counters']):
                if proc.info['name'] in self.black_list_process:
                    print("killed ", proc.info)
                    proc.kill()
                    ps = ProcessEvent(proc, datetime.datetime.now(), True)
                    killed = True
                else:
                    ps = ProcessEvent(proc, datetime.datetime.now(), False)
                running_process.append(ps.event)

            if killed or count <= 1 or count % 10 == 0:
                try:
                    data = json.dumps(running_process).encode('utf8')
                    response = requests.post("https://" + self.api + "/process", data=data,
                                             headers={"x-api-key": self.key})
                    if response.ok:
                        self.black_list_process = list(map(lambda x: x.strip(), response.json().split(",")))
                    else:
                        print(response.status_code)
                        print(response.reason)
                except Exception as e:
                    print(e)
            count = count + 1
            sleep(5)
