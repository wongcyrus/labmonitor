import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib

file_hash = {}


class Watcher:
    DIRECTORY_TO_WATCH = "/home/osboxes/PycharmProjects/ite3101_introduction_to_programming/lab"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def sha256_checksum(filename, block_size=65536):
        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    @staticmethod
    def on_any_event(event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return None
        elif event.event_type == 'modified':
            print("Received modified event - %s." % event.src_path)
            new_hash = Handler.sha256_checksum(event.src_path)
            print('\t' + new_hash)
            if event.src_path in file_hash:
                old_hash = file_hash.get(event.src_path)
                if old_hash != new_hash:
                    print("Code changed " + event.src_path)
                    file_hash[event.src_path] = new_hash
            else:
                print("First update")
                file_hash[event.src_path] = new_hash
        print(file_hash)
