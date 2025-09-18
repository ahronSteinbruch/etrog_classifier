from client.beckend.config import Config
import sqlite3


class DalSqlite:
    def __init__(self):
        self.cfg = Config()
        self.db_path = self.cfg.DB_PATH


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


        Side Effects:
            - Ensures the schema exists.
            - UPSERTs the row for 'variety' and increments only the submitted grade using
              ON CONFLICT(variety) DO UPDATE.
        """
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