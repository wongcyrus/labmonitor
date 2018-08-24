import json
import time
from urllib import request

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib

file_hash = {}


class Watcher:

    def __init__(self, api, key, directory_to_watch):
        self.observer = Observer()
        self.api = api
        self.key = key
        self.directory_to_watch = directory_to_watch

    def run(self):
        event_handler = Handler(self.api, self.key, self.directory_to_watch)
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

    def __init__(self, api, key, directory_to_watch):
        self.api = api
        self.key = key
        self.directory_to_watch = directory_to_watch

    def upload(self, file_path):
        try:
            with open(file_path, 'r') as in_file:
                code = in_file.read()
            key = file_path.replace(self.directory_to_watch, "")
            data = {"key": key, "code": code}
            req = request.Request("https://" + self.api + "/code", data=json.dumps(data).encode('utf8'))
            req.add_header("x-api-key", self.key)
            resp = request.urlopen(req)
            print(str(resp.status) + " -" + resp.msg)

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
        elif event.event_type == 'modified':
            print("Received modified event - %s." % event.src_path)
            new_hash = self.sha256_checksum(event.src_path)
            print('\t' + new_hash)
            if event.src_path in file_hash:
                old_hash = file_hash.get(event.src_path)
                if old_hash != new_hash:
                    print("Code changed " + event.src_path)
                    file_hash[event.src_path] = new_hash
                    self.upload(event.src_path)
            else:
                print("First update")
                file_hash[event.src_path] = new_hash
                self.upload(event.src_path)
        print(file_hash)
