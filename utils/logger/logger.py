from datetime import datetime
from pymongo import MongoClient
import json
import os


class Logger:
    """
    Universal Logger:
    - Log to console, file, or MongoDB
    - Default file path: 'logs.txt'
    - MongoDB defaults: mongodb://localhost:27017/, DB: logging_db, Collection: logs
    """

    # Class variables to hold single MongoDB client and collection
    _mongo_client = None
    _mongo_collection = None

    def __init__(self, destination="console", **kwargs):
        self.destination = destination.lower()  # case-insensitive
        self.kwargs = kwargs

        if self.destination == "file":
            # default file path
            self.filepath = kwargs.get("filepath", os.path.join(os.getcwd(), "logs.txt"))

        elif self.destination == "mongo":
            # Initialize singleton MongoDB client/collection if not done yet
            if Logger._mongo_client is None:
                uri = kwargs.get("connection_string", "mongodb://localhost:27017/")
                db_name = kwargs.get("db_name", "logging_db")
                collection_name = kwargs.get("collection_name", "logs")
                Logger._mongo_client = MongoClient(uri)
                Logger._mongo_collection = Logger._mongo_client[db_name][collection_name]

            self.collection = Logger._mongo_collection

    def _format_message(self, level, message, exception=None):
        """Create a standardized log entry"""
        log_entry = {
            "level": level,
            "timestamp": datetime.now(),
            "message": message
        }
        if exception:
            log_entry["exception"] = str(exception)
        return log_entry

    def _log(self, level, message, exception=None):
        """Send log to the correct destination"""
        entry = self._format_message(level, message, exception)

        if self.destination == "console":
            print(f"[{level}] {entry['timestamp']}: {message} {exception or ''}")
        elif self.destination == "file":
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        elif self.destination == "mongo":
            self.collection.insert_one(entry)

    # Public logging methods
    def info(self, message):
        self._log("INFO", message)

    def warning(self, message):
        self._log("WARNING", message)

    def error(self, message, exception=None):
        self._log("ERROR", message, exception)