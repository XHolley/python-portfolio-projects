from __future__ import annotations

import sqlite3

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    source TEXT NOT NULL,
    applied_date TEXT NOT NULL,
    last_updated TEXT NOT NULL,
    notes TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_company ON applications(company);
"""


def connect(db_path: str) -> sqlite3.Connection:
    # Use Row objects so callers can access columns by name (row["status"]).
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    # Safe to call on every startup; IF NOT EXISTS keeps this idempotent.
    conn.executescript(SCHEMA_SQL)
    conn.commit()
