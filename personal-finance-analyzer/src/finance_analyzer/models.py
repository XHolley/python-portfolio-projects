from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Transaction:
    date: date
    description: str
    amount: float
    category: str = "Uncategorized"


@dataclass(slots=True)
class MonthlySummary:
    month: str
    income: float
    expenses: float
    net: float
    savings_rate: float
