from pathlib import Path
from queue import Queue


class ImageQueue:
    def __init__(self):
        self.queue = Queue()

    def add_image(self, image_path):
        path = Path(image_path)
        if path.exists() and path.is_file():
            self.queue.put(path)
            print(f"Image added to queue: {path}")

    def get_image(self):
        if not self.queue.empty():
            return self.queue.get()
        return None

    def is_empty(self):
        return self.queue.empty()