from __future__ import annotations
import time
import requests
from config import Config


class ClientToSql:
    """
    Client that polls the Etrog-B status API until a job is done, validates the
    returned grade, and persists per-variety grade counts into a local SQLite DB.

    Attributes:
        cfg (Config): Loaded configuration.
        base_url (str): Service base URL from config.
        path_template (str): URL path template appended as-is (no ID formatting here).
        db_path (str): SQLite database file path.
        valid_grades (set[str]): Allowed grades.
    """
    def __init__(self):
        self.cfg = Config()
        self.base_url = self.cfg.BASE_URL
        self.path_template = self.cfg.PATH_TEMPLATE

        self.valid_grades = self.cfg.VALID_GRADES

    def poll_until_status_done(self, job_id) -> str:
        """
        Poll the status endpoint until it reports 'done', then return the final grade.

        Behavior:
            - Builds URL as: base_url.rstrip('/') + path_template.
            - Sends repeated GET requests with the job_id in the request body.
            - Expects JSON like: {"status": "done", "response": "A"}.
            - Sleeps 0.1 seconds between attempts.

        Args:
            job_id (str): Server-issued job identifier.

        Returns:
            str: Uppercase grade ('A'..'E') from the 'response' field.

        Raises:
            ValueError: If status is 'done' but the grade is not in valid_grades.
        """
        url = self.base_url.rstrip("/") + self.path_template

        while True:
            res = requests.get(url, data=job_id)
            data = res.json()

            status = str(data.get("status", "")).strip().lower()
            if status == "done":
                grade = str(data.get("response", "")).strip().upper()
                if grade not in self.valid_grades:
                    raise ValueError(f"Invalid grade at DONE: {grade!r}, payload={data}")
                return grade

            time.sleep(0.1)
