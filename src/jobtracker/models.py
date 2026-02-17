from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ApplicationStatus(StrEnum):
    # Centralized lifecycle states used by CLI choices and DB validation.
    APPLIED = "applied"
    PHONE_SCREEN = "phone_screen"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


@dataclass(slots=True)
class JobApplication:
    """In-memory representation of one DB row from the applications table."""
    id: int | None
    company: str
    role: str
    status: str
    source: str
    applied_date: str
    last_updated: str
    notes: str
