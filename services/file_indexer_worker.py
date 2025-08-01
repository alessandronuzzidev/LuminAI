from time import sleep
from PySide6.QtCore import QObject, Signal, QThread
import json
import os


class FileIndexWorker(QObject):
    progress = Signal(int, int) 
    finished = Signal()

    def __init__(self, json_path="data/config.json", index_function=None):
        super().__init__()
        self.json_path = json_path
        self.index_function = index_function

    def run(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.path = self.config["path"]
        
        all_files = []
        for dirpath, _, filenames in os.walk(self.path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                all_files.append(full_path)

        total = len(all_files)

        for i, file_path in enumerate(all_files, 1):
            self.index_function(file_path)
            self.progress.emit(i, total)
        
        self.finished.emit()
