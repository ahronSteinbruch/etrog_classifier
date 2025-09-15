from __future__ import annotations
import time
import sqlite3
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
        timeout_s (int): Maximum total wait time in seconds before giving up.
        db_path (str): SQLite database file path.
        valid_grades (set[str]): Allowed grades.
    """
    def __init__(self):
        self.cfg = Config()
        self.base_url = self.cfg.BASE_URL
        self.path_template = self.cfg.PATH_TEMPLATE
        self.timeout_s = self.cfg.TIMEOUT_S
        self.db_path = self.cfg.DB_PATH
        self.valid_grades = self.cfg.VALID_GRADES

    def poll_until_status_done(self, job_id) -> str:
        """
        Poll the status endpoint until it reports 'done', then return the final grade.

        Behavior:
            - Builds URL as: base_url.rstrip('/') + path_template.
            - Sends repeated GET requests with the job_id in the request body.
            - Expects JSON like: {"status": "done", "response": "A"}.
            - Sleeps 100 seconds between attempts; no timeout is enforced here.

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

    def ensure_schema(self) -> None:
        """
        Create the SQLite schema and trigger if they do not already exist.

        Creates:
            - Table 'grades' with columns: variety (PK), A..E counters, updated_at.
            - Trigger 'trg_grades_updated' to refresh updated_at on row updates.

        Idempotent:
            Safe to call multiple times; uses IF NOT EXISTS.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS grades (
                    variety     TEXT PRIMARY KEY,
                    A           INTEGER NOT NULL DEFAULT 0,
                    B           INTEGER NOT NULL DEFAULT 0,
                    C           INTEGER NOT NULL DEFAULT 0,
                    D           INTEGER NOT NULL DEFAULT 0,
                    E           INTEGER NOT NULL DEFAULT 0,
                    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS trg_grades_updated
                AFTER UPDATE ON grades
                FOR EACH ROW BEGIN
                    UPDATE grades SET updated_at = CURRENT_TIMESTAMP WHERE variety = NEW.variety;
                END;
            """)
            conn.commit()

    def increment_grade(self, variety: str, grade: str) -> None:
        """
        Increment the counter for a specific grade for the given variety.

        Args:
            variety (str): The etrog variety key to update.
            grade (str): One of VALID_GRADES ('A'..'E').

        Raises:
            ValueError: If 'grade' is not in VALID_GRADES.

        Side Effects:
            - Ensures the schema exists.
            - UPSERTs the row for 'variety' and increments only the submitted grade using
              ON CONFLICT(variety) DO UPDATE.
        """
        if grade not in self.valid_grades:
            raise ValueError(f"Invalid grade '{grade}'")
        self.ensure_schema()

        sql = """
            INSERT INTO grades (variety, A, B, C, D, E)
            VALUES (
                ?,
                CASE WHEN ?='A' THEN 1 ELSE 0 END,
                CASE WHEN ?='B' THEN 1 ELSE 0 END,
                CASE WHEN ?='C' THEN 1 ELSE 0 END,
                CASE WHEN ?='D' THEN 1 ELSE 0 END,
                CASE WHEN ?='E' THEN 1 ELSE 0 END
            )
            ON CONFLICT(variety) DO UPDATE SET
                A = A + excluded.A,
                B = B + excluded.B,
                C = C + excluded.C,
                D = D + excluded.D,
                E = E + excluded.E
        """
        params = (variety, grade, grade, grade, grade, grade)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(sql, params)
            conn.commit()

    def run_client_g(self, job_id: str, etrog_type: str) -> dict:
        """
        Orchestrate polling and persistence: wait for the final grade, store it, and return a summary.

        Args:
            job_id (str): The job ID to poll for completion.
            etrog_type (str): Variety name to increment in the database.

        Returns:
            dict: {'id': job_id, 'variety': etrog_type, 'grade': <grade>, 'saved': True}
        """
        grade = self.poll_until_status_done(job_id)
        self.increment_grade(etrog_type, grade)
        return {"variety": etrog_type, "grade": grade, "saved": True}
