import os
import signal
import time
import json
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
import json

def load_watch_path():
    with open("data/config.json", "r") as f:
        config = json.load(f)
    return config["path"]

def save_pid(file_path):
    pid_file = file_path
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

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


class WatcherHandler(FileSystemEventHandler):
    
    def handle_event(self, src_path, action):
        """Enqueue event instead of processing immediately."""
        if action in ("modified", "created"):
            try:
                mtime = os.path.getmtime(src_path)
            except FileNotFoundError:
                return

            if last_mtime.get(src_path) == mtime:
                return

            last_mtime[src_path] = mtime
        
        task = {"src_path": src_path, "action": action}

        s = socket.socket()
        s.connect(("127.0.0.1", 65432))
        s.send(json.dumps(task).encode())
        response = s.recv(1024)
        s.close()
    
    def on_modified(self, event):
        if not event.is_directory and not paused:
            self.handle_event(event.src_path, "modified")

    def on_created(self, event):
        if not event.is_directory and not paused:
            self.handle_event(event.src_path, "created")

    def on_deleted(self, event):
        if not event.is_directory and not paused:
            self.handle_event(event.src_path, "deleted")

def start_observer(path):
    global observer
    if observer:
        observer.stop()
        observer.join()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring path: {path}")
            
WATCH_PATH = None
paused = False
snapshot = {}
observer = None
last_mtime = {}

signal.signal(signal.SIGUSR1, pause)
signal.signal(signal.SIGUSR2, resume)

pid_file = "data/monitor.pid"
save_pid(pid_file)
            
event_handler = WatcherHandler()

WATCH_PATH = load_watch_path()
start_observer(WATCH_PATH)

try:
    while True:
        if not paused and observer is not None and observer.is_alive():
            current_path = load_watch_path()
            if current_path != WATCH_PATH:
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