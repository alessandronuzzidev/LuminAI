import queue
import threading
import socket
import json
import time
import services.embeddings_lib as embedding
from services.text_extractor_service import TextExtractorService


class TaskManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host="127.0.0.1", port=65432):
        if hasattr(self, "_initialized"):
            return

        
        self.event_queue = queue.Queue()
        self.total_tasks = 0
        self.completed_tasks = 0

        threading.Thread(target=self._worker, daemon=True).start()

        self.host = host
        self.port = port
        threading.Thread(target=self._start_socket_server, daemon=True).start()

        self._initialized = True

    def add_task(self, task):
        self.total_tasks += 1
        self.event_queue.put(task)

    def clear_queue(self):
        self.event_queue.queue.clear()
        self.total_tasks = 0
        self.completed_tasks = 0

    def get_progress(self):
        return self.completed_tasks, self.total_tasks

    def _worker(self):
        while True:
            task = self.event_queue.get()
            
            if task["action"] == "modified":
                embedding.delete_by_file_path(task["src_path"])
                TextExtractorService().extract_and_save_text(task["src_path"])
            elif task["action"] == "created":
                TextExtractorService().extract_and_save_text(task["src_path"])
            elif task["action"] == "deleted":
                embedding.delete_by_file_path(task["src_path"])

            self.completed_tasks += 1
            self.event_queue.task_done()

    def _start_socket_server(self):
        """Servidor TCP que recibe tareas en JSON y las encola"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f"[TaskManager] Listening for tasks on {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()

    def _handle_client(self, conn, addr):
        """Recibe datos de un cliente y los añade como tarea"""
        try:
            data = conn.recv(4096)
            if not data:
                return

            try:
                task = json.loads(data.decode())
                if "action" in task and "src_path" in task:
                    self.add_task(task)
                    conn.sendall(b"Task received\n")
                elif "progress" in task:
                    completed, total = self.get_progress()
                    response = {"completed": completed, "total": total}
                    conn.sendall(json.dumps(response).encode())
                elif "cancel" in task:
                    self.clear_queue()
                    conn.sendall(b"Queue cleared\n")
                elif "search" in task:
                    message = task["message"]
                    similarity_threshold = task["similarity_threshold"]
                    top_k = task["top_k"]
                    results = embedding.query_embedding(message, similarity_threshold, top_k)
                    response = {"results": results}
                    conn.sendall(json.dumps(response).encode())
                else:
                    conn.sendall(b"Invalid task format\n")
            except json.JSONDecodeError:
                conn.sendall(b"Invalid JSON\n")
        finally:
            conn.close()
            

if __name__ == "__main__":
    embedding.create_database()
    tm = TaskManager()
    print("TaskManager is running...")

    try:
        while True:
            completed, total = tm.get_progress()
            print(f"Progress: {completed}/{total} tasks completed", end="\r")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down TaskManager...")
