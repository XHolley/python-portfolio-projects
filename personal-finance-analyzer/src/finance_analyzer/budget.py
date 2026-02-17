from __future__ import annotations

from dataclasses import dataclass, field

from .models import MonthlySummary


@dataclass(slots=True)
class BudgetConfig:
    monthly_spending_limit: float | None = None
    category_limits: dict[str, float] = field(default_factory=dict)


def generate_budget_alerts(
    summaries: list[MonthlySummary],
    categories_by_month: dict[str, dict[str, float]],
    budget: BudgetConfig,
) -> list[str]:
    if not summaries:
        return ["No transactions found; no alerts generated."]

    latest = summaries[-1]
    latest_categories = categories_by_month.get(latest.month, {})
    alerts: list[str] = []

    if budget.monthly_spending_limit is not None and latest.expenses > budget.monthly_spending_limit:
        delta = latest.expenses - budget.monthly_spending_limit
        alerts.append(
            f"ALERT: Total spending for {latest.month} is ${latest.expenses:.2f}, "
            f"which is ${delta:.2f} above your ${budget.monthly_spending_limit:.2f} budget."
        )

    for category, limit in budget.category_limits.items():
        spent = latest_categories.get(category, 0.0)
        if spent > limit:
            alerts.append(
                f"ALERT: {category} spending for {latest.month} is ${spent:.2f}, "
                f"which is ${(spent - limit):.2f} above your ${limit:.2f} budget."
            )

    if latest.savings_rate < 0.2:
        alerts.append(
            f"NOTICE: Savings rate for {latest.month} is {latest.savings_rate:.1%}, below the 20% target."
        )

    if not alerts:
        alerts.append(f"OK: Spending for {latest.month} is within configured budget limits.")

    return alerts
