import os


class Config:
    """
    Holds runtime configuration loaded from environment variables.

    Attributes:
        BASE_URL (str): Base URL for the Etrog-B service (default: "http://localhost:8000").
        PATH_TEMPLATE (str): Status path template; expected to include "{id}" (default: "/answer/{id}").
        DB_PATH (str): SQLite database file path (default: "etrog_grades.db").
        VALID_GRADES (set[str]): Allowed grades: {"A","B","C","D","E"}.
    """
    def __init__(self):
        self.BASE_URL = os.getenv("ETROG_B_BASE_URL", "http://localhost:8000")
        self.PATH_TEMPLATE = os.getenv("ETROG_B_STATUS_PATH", "/answer/{id}")
        self.DB_PATH = os.getenv("ETROG_SQLITE_PATH", "etrog_grades.db")
        self.VALID_GRADES = {"A", "B", "C", "D", "E"}
