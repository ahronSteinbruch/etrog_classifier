from datetime import datetime
from pymongo import MongoClient

class MongoLogger:
    def __init__(self, connection_string, db_name, collection_name):
        client = MongoClient(connection_string)
        db = client[db_name]
        self.collection = db[collection_name]

    def _format_message(self, level, message, exception=None):
        log_entry = {
            "level": level,
            "timestamp": datetime.now(),
            "message": message
        }
        if exception:
            log_entry["exception"] = str(exception)
        return log_entry

    def info(self, message):
        self.collection.insert_one(self._format_message("INFO", message))

    def warning(self, message):
        self.collection.insert_one(self._format_message("WARNING", message))

    def error(self, message, exception=None):
        self.collection.insert_one(self._format_message("ERROR", message, exception))
