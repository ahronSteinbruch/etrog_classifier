import json
from logger_base import Logger
class FileLogger(Logger):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _write_to_file(self, data: dict):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, default=str) + "\n")

    def info(self, message: str):
        self._write_to_file(self._format_message("INFO", message))

    def warning(self, message: str):
        self._write_to_file(self._format_message("WARNING", message))

    def error(self, message: str, exception: Exception = None):
        self._write_to_file(self._format_message("ERROR", message, exception))


