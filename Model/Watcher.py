import hashlib
import json
import platform
import time

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

file_hash = {}


class Watcher:

    def __init__(self, api: str, key: str, directory_to_watch: str, using_pycharm: bool):
        self.observer = Observer()
        self.api = api
        self.key = key
        self.directory_to_watch = directory_to_watch
        self.using_pycharm = using_pycharm

    def run(self):
        event_handler = Handler(self.api, self.key, self.directory_to_watch, self.using_pycharm)
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, api: str, key: str, directory_to_watch: str, using_pycharm: bool):
        self.api = api
        self.key = key
        self.directory_to_watch = directory_to_watch
        self.using_pycharm = using_pycharm

    def upload(self, file_path):
        try:
            with open(file_path, 'r') as in_file:
                code = in_file.read()
            key = file_path.replace(self.directory_to_watch, "")
            data = {"key": key, "code": code}
            response = requests.post("https://" + self.api + "/code", data=json.dumps(data).encode('utf8'),
                                     headers={"x-api-key": self.key})
            if response.ok:
                print(response.json()['test_result'])
            else:
                print(response.status_code)
                print(response.reason)
        except Exception as e:
            print(e)

    @staticmethod
    def sha256_checksum(filename, block_size=65536):
        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    def on_any_event(self, event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return None
        elif (not platform.release() == '10' and event.event_type == 'modified') or \
                (self.using_pycharm and platform.release() == '10' and event.event_type == 'moved'):
            # PyCharm in Windows 10 renames a tmp file when save.
            path = event.dest_path if self.using_pycharm and platform.release() == '10' and event.dest_path.endswith(
                ".py") else event.src_path
            time.sleep(1)
            print("Received modified event - %s." % path)
            new_hash = self.sha256_checksum(path)
            print('\t' + new_hash)
            if path in file_hash:
                old_hash = file_hash.get(path)
                if old_hash != new_hash:
                    print("Code changed " + path)
                    file_hash[path] = new_hash
                    self.upload(path)
            else:
                print("First update")
                file_hash[path] = new_hash
                self.upload(path)
        print(file_hash)
