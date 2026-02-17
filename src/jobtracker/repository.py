from __future__ import annotations

import csv
from datetime import date
import sqlite3
from typing import Iterable

from .models import ApplicationStatus, JobApplication


VALID_STATUSES = {status.value for status in ApplicationStatus}


class ApplicationRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_application(
        self,
        company: str,
        role: str,
        source: str = "unknown",
        applied_date: str | None = None,
        notes: str = "",
    ) -> int:
        applied = applied_date or date.today().isoformat()
        now = date.today().isoformat()
        cursor = self.conn.execute(
            """
            INSERT INTO applications (company, role, status, source, applied_date, last_updated, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (company.strip(), role.strip(), ApplicationStatus.APPLIED.value, source.strip(), applied, now, notes),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def list_applications(self, status: str | None = None) -> list[JobApplication]:
        query = "SELECT * FROM applications"
        params: tuple[str, ...] = ()
        if status:
            query += " WHERE status = ?"
            params = (status,)
        query += " ORDER BY applied_date DESC, id DESC"

        rows = self.conn.execute(query, params).fetchall()
        return [
            JobApplication(
                id=row["id"],
                company=row["company"],
                role=row["role"],
                status=row["status"],
                source=row["source"],
                applied_date=row["applied_date"],
                last_updated=row["last_updated"],
                notes=row["notes"],
            )
            for row in rows
        ]

    def update_status(self, application_id: int, new_status: str) -> bool:
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Unsupported status: {new_status}")

        cursor = self.conn.execute(
            "UPDATE applications SET status = ?, last_updated = ? WHERE id = ?",
            (new_status, date.today().isoformat(), application_id),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def export_csv(self, output_path: str) -> int:
        rows = self.conn.execute("SELECT * FROM applications ORDER BY id").fetchall()
        with open(output_path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "id",
                    "company",
                    "role",
                    "status",
                    "source",
                    "applied_date",
                    "last_updated",
                    "notes",
                ],
            )
            writer.writeheader()
            writer.writerows([dict(row) for row in rows])
        return len(rows)

    def import_csv(self, input_path: str) -> int:
        imported = 0
        with open(input_path, "r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                status = row.get("status", ApplicationStatus.APPLIED.value)
                if status not in VALID_STATUSES:
                    status = ApplicationStatus.APPLIED.value

                self.conn.execute(
                    """
                    INSERT INTO applications (company, role, status, source, applied_date, last_updated, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        (row.get("company") or "Unknown").strip(),
                        (row.get("role") or "Unknown").strip(),
                        status,
                        (row.get("source") or "unknown").strip(),
                        row.get("applied_date") or date.today().isoformat(),
                        row.get("last_updated") or date.today().isoformat(),
                        row.get("notes") or "",
                    ),
                )
                imported += 1
        self.conn.commit()
        return imported

    def iter_all(self) -> Iterable[JobApplication]:
        return self.list_applications(status=None)
