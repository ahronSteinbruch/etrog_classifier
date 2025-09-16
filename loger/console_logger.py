from logger_base import Logger

class ConsoleLogger(Logger):
    def info(self, message: str):
        print(self._format_message("INFO", message))

    def warning(self, message: str):
        print(self._format_message("WARNING", message))

    def error(self, message: str, exception: Exception = None):
        print(self._format_message("ERROR", message, exception))


