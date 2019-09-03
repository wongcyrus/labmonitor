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
        self.data_saving = "true"

    def run(self):
        count = 0
        last_running_process = {}
        while True:
            submit_process = []
            running_process = {}
            killed = False
            for proc in psutil.process_iter(
                    attrs=['pid', 'name', 'cpu_times', 'memory_percent', 'memory_info', 'io_counters']):
                if proc.info['name'] in self.black_list_process:
                    print("killed ", proc.info)
                    proc.kill()
                    ps = ProcessEvent(proc, datetime.datetime.now(), True)
                    killed = True
                    print("Killed: ", ps)
                else:
                    ps = ProcessEvent(proc, datetime.datetime.now(), False)

                if self.data_saving == "true":
                    # Just record newly opened process.
                    if str(ps.event["pid"]) not in last_running_process:
                        submit_process.append(ps.event)
                    running_process[str(ps.event["pid"])] = ps.event
                else:
                    submit_process.append(ps.event)

            last_running_process = running_process
            if killed or len(submit_process) > 0:
                try:
                    data = json.dumps(submit_process).encode('utf8')
                    response = requests.post("https://" + self.api + "/process", data=data,
                                             headers={"x-api-key": self.key})
                    if response.ok:
                        self.data_saving, *self.black_list_process = list(
                            map(lambda x: x.strip(), response.json().split(",")))
                    else:
                        print(response.status_code)
                        print(response.reason)
                except Exception as e:
                    print(e)
            count = count + 1
            sleep(10)
