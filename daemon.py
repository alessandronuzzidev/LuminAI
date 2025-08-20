import os
import signal
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import services.embeddings_lib as embedding
from controller.controller import Controller
from services.file_indexer_worker import FileIndexWorker

paused = False
snapshot = {}
WATCH_PATH = None
observer = None

def take_snapshot(path):
    """Return a dict with file paths and modification times."""
    state = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f)
            try:
                mtime = os.path.getmtime(full_path)
                state[full_path] = mtime
            except FileNotFoundError:
                continue
    return state

def compare_snapshots(old, new):
    """Compare old and new snapshots and print changes."""
    old_files = set(old.keys())
    new_files = set(new.keys())

    created = new_files - old_files
    deleted = old_files - new_files
    common = old_files & new_files

    for f in created:
        print(f"File created: {f}")
    for f in deleted:
        print(f"File deleted: {f}")
    for f in common:
        if old[f] != new[f]:
            print(f"File modified: {f}")

def pause(sig, frame):
    global paused, snapshot
    paused = True
    snapshot = take_snapshot(WATCH_PATH)
    print("Monitor paused, snapshot saved")

def resume(sig, frame):
    global paused, snapshot
    paused = False
    new_snapshot = take_snapshot(WATCH_PATH)
    print("Monitor resumed")
    compare_snapshots(snapshot, new_snapshot)
    snapshot = {}

# Register signals
signal.signal(signal.SIGUSR1, pause)
signal.signal(signal.SIGUSR2, resume)

# Save PID to a file
pid_file = "data/monitor.pid"
with open(pid_file, "w") as f:
    f.write(str(os.getpid()))

class WatcherHandler(FileSystemEventHandler):
    controller = Controller()
    
    def on_modified(self, event):
        if not event.is_directory and not paused:
            print(f"File modified: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory and not paused:
            print(f"File created: {event.src_path}")
            worker = FileIndexWorker(self.controller)
            worker.run()
            print(f"File indexed: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory and not paused:
            print(f"File deleted: {event.src_path}")

def load_watch_path():
    with open("data/config.json", "r") as f:
        config = json.load(f)
    return config["path"]

event_handler = WatcherHandler()

def start_observer(path):
    global observer
    if observer:
        observer.stop()
        observer.join()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring path: {path}")

WATCH_PATH = load_watch_path()
start_observer(WATCH_PATH)

try:
    embedding.create_database()
    while True:
        if not paused and observer is not None and observer.is_alive():
            current_path = load_watch_path()
            if current_path != WATCH_PATH:
                print(f"Watch path changed: {WATCH_PATH} -> {current_path}")
                embedding.restart()
                WATCH_PATH = current_path
                start_observer(WATCH_PATH)
                print(f"Watch path updated: {WATCH_PATH}")
            time.sleep(1 if not paused else 0.5)
except KeyboardInterrupt:
    print("Monitor stopped")
finally:
    if observer:
        observer.stop()
        observer.join()
    if os.path.exists(pid_file):
        os.remove(pid_file)
