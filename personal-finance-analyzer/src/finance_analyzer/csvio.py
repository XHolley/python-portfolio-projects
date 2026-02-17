from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from .models import Transaction

DATE_ALIASES = {"date", "transaction date", "posted date"}
DESCRIPTION_ALIASES = {"description", "merchant", "name", "details"}
AMOUNT_ALIASES = {"amount", "transaction amount"}
DEBIT_ALIASES = {"debit", "withdrawal"}
CREDIT_ALIASES = {"credit", "deposit"}


def _clean_header(value: str) -> str:
    return value.strip().lower()


def _pick_column(headers: list[str], aliases: set[str]) -> str | None:
    for header in headers:
        if _clean_header(header) in aliases:
            return header
    return None


def _parse_float(value: str | None) -> float:
    if not value:
        return 0.0
    cleaned = value.replace(",", "").replace("$", "").strip()
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = f"-{cleaned[1:-1]}"
    return float(cleaned)


def _parse_date(value: str) -> datetime.date:
    patterns = ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
    for pattern in patterns:
        try:
            return datetime.strptime(value.strip(), pattern).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value}")


def load_transactions(csv_path: str | Path) -> list[Transaction]:
    path = Path(csv_path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return []

        headers = list(reader.fieldnames)
        date_col = _pick_column(headers, DATE_ALIASES)
        description_col = _pick_column(headers, DESCRIPTION_ALIASES)
        amount_col = _pick_column(headers, AMOUNT_ALIASES)
        debit_col = _pick_column(headers, DEBIT_ALIASES)
        credit_col = _pick_column(headers, CREDIT_ALIASES)

        if not date_col or not description_col:
            raise ValueError("CSV must include date and description columns")

        if not amount_col and not (debit_col and credit_col):
            raise ValueError("CSV must include either amount column or debit+credit columns")

        transactions: list[Transaction] = []
        for row in reader:
            tx_date = _parse_date(row[date_col])
            description = row[description_col].strip()

            if amount_col:
                amount = _parse_float(row.get(amount_col))
            else:
                debit = _parse_float(row.get(debit_col))
                credit = _parse_float(row.get(credit_col))
                amount = credit - debit

            transactions.append(Transaction(date=tx_date, description=description, amount=round(amount, 2)))

    return transactions


def save_transactions_csv(csv_path: str | Path, transactions: list[Transaction]) -> None:
    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "description", "amount", "category"])
        writer.writeheader()
        for tx in transactions:
            writer.writerow(
                {
                    "date": tx.date.isoformat(),
                    "description": tx.description,
                    "amount": f"{tx.amount:.2f}",
                    "category": tx.category,
                }
            )
