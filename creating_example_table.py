import sqlite3
import random

DB_PATH = "etrog_grades.db"

VARIETIES = [
    "Yemeni Etrog",
    "Moroccan Etrog",
    "Calabrian Etrog",
    "Jerusalem Etrog",
    "Chabad Etrog",
    "Etrog Burstein",
]

random.seed(42)

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS grades")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            variety    TEXT PRIMARY KEY,
            A          INTEGER NOT NULL DEFAULT 0,
            B          INTEGER NOT NULL DEFAULT 0,
            C          INTEGER NOT NULL DEFAULT 0,
            D          INTEGER NOT NULL DEFAULT 0,
            E          INTEGER NOT NULL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    rows = []
    for v in VARIETIES:
        A = random.randint(0, 10)
        B = random.randint(0, 10)
        C = random.randint(0, 10)
        D = random.randint(0, 10)
        E = random.randint(0, 10)
        rows.append((v, A, B, C, D, E))

    cur.executemany(
        "INSERT OR REPLACE INTO grades (variety, A, B, C, D, E) VALUES (?, ?, ?, ?, ?, ?)",
        rows
    )
    conn.commit()


