import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class ReloadOnChange(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.run_script()

    def run_script(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen(["python", self.script_name])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print("Change detected. Restarting...", time.ctime())
            self.run_script()

if __name__ == "__main__":
    script = "main.py"
    event_handler = ReloadOnChange(script)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    print("Press Ctrl+C for exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.kill()
    observer.join()
