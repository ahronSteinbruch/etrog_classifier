import os


class Config:
    """
    Holds runtime configuration loaded from environment variables.

    Attributes:
        BASE_URL (str): Base URL for the Etrog-B service (default: "http://localhost:8000").
        PATH_TEMPLATE (str): Status path template; expected to include "{id}" (default: "/etrog/status/{id}").
        POLL_INTERVAL_MS (int): Poll interval in milliseconds (default: 200).
        TIMEOUT_S (int): Max seconds to wait for a job to finish (default: 1200).
        DB_PATH (str): SQLite database file path (default: "etrog_grades.db").
        VALID_GRADES (set[str]): Allowed grades: {"A","B","C","D","E"}.
    """
    def __init__(self):
        self.BASE_URL = os.getenv("ETROG_B_BASE_URL", "http://localhost:8000")
        self.PATH_TEMPLATE = os.getenv("ETROG_B_STATUS_PATH", "/etrog/status/{id}")
        self.POLL_INTERVAL_MS = int(os.getenv("ETROG_POLL_INTERVAL_MS", "200"))
        self.TIMEOUT_S = int(os.getenv("ETROG_TIMEOUT_S", "1200"))
        self.DB_PATH = os.getenv("ETROG_SQLITE_PATH", "etrog_grades.db")
        self.VALID_GRADES = {"A", "B", "C", "D", "E"}
