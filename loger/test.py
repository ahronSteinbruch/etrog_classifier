from console_logger import ConsoleLogger
from file_logger import FileLogger
from mongo_logger import MongoLogger

def test_console_logger():
    print("\n--- Testing ConsoleLogger ---")
    logger = ConsoleLogger()
    logger.info("Info test message")
    logger.warning("Warning test message")
    logger.error("Error test message", Exception("Console Test Exception"))

def test_file_logger():
    print("\n--- Testing FileLogger ---")
    logger = FileLogger("test_logs.txt")
    logger.info("Info test message")
    logger.warning("Warning test message")
    logger.error("Error test message", Exception("File Test Exception"))
    print("Logs were written to test_logs.txt")

def test_mongo_logger():
    print("\n--- Testing MongoLogger ---")
    logger = MongoLogger("mongodb://localhost:27017/", "logging_db", "logs")
    logger.info("Info test message")
    logger.warning("Warning test message")
    logger.error("Error test message", Exception("Mongo Test Exception"))
    print("Logs were written to MongoDB → DB: logging_db, Collection: logs")

if __name__ == "__main__":
    test_console_logger()
    test_file_logger()
    test_mongo_logger()
