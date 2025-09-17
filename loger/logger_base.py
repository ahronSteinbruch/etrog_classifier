from abc import ABC, abstractmethod
import datetime

class Logger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def warning(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str, exception: Exception = None):
        pass

    def _format_message(self, level: str, message: str, exception: Exception = None):
        return f"[{level}] {datetime.datetime.now()}: {message} {exception or ''}"
