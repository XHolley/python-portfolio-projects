from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from .models import MonthlySummary, Transaction


def assign_categories(transactions: list[Transaction], categorize_fn) -> list[Transaction]:
    for tx in transactions:
        tx.category = categorize_fn(tx.description, tx.amount)
    return transactions


def monthly_summaries(transactions: list[Transaction]) -> list[MonthlySummary]:
    monthly_income: dict[str, float] = defaultdict(float)
    monthly_expenses: dict[str, float] = defaultdict(float)

    for tx in transactions:
        month = tx.date.strftime("%Y-%m")
        if tx.amount >= 0:
            monthly_income[month] += tx.amount
        else:
            monthly_expenses[month] += abs(tx.amount)

    months = sorted(set(monthly_income) | set(monthly_expenses))
    summaries: list[MonthlySummary] = []

    for month in months:
        income = round(monthly_income[month], 2)
        expenses = round(monthly_expenses[month], 2)
        net = round(income - expenses, 2)
        savings_rate = round((net / income) if income else 0.0, 4)
        summaries.append(MonthlySummary(month=month, income=income, expenses=expenses, net=net, savings_rate=savings_rate))

    return summaries


def category_spending_by_month(transactions: list[Transaction]) -> dict[str, dict[str, float]]:
    data: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))

    for tx in transactions:
        if tx.amount < 0:
            month = tx.date.strftime("%Y-%m")
            data[month][tx.category] += abs(tx.amount)

    return {
        month: {category: round(amount, 2) for category, amount in sorted(categories.items())}
        for month, categories in sorted(data.items())
    }


def write_monthly_summary_csv(path: str | Path, summaries: list[MonthlySummary]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["month", "income", "expenses", "net", "savings_rate"])
        writer.writeheader()
        for summary in summaries:
            writer.writerow(
                {
                    "month": summary.month,
                    "income": f"{summary.income:.2f}",
                    "expenses": f"{summary.expenses:.2f}",
                    "net": f"{summary.net:.2f}",
                    "savings_rate": f"{summary.savings_rate:.4f}",
                }
            )


def write_category_summary_csv(path: str | Path, categories_by_month: dict[str, dict[str, float]]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["month", "category", "spend"])
        writer.writeheader()
        for month, categories in categories_by_month.items():
            for category, spend in categories.items():
                writer.writerow({"month": month, "category": category, "spend": f"{spend:.2f}"})
