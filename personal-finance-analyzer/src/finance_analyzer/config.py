from __future__ import annotations

import json
from pathlib import Path

from .budget import BudgetConfig
from .categorization import DEFAULT_RULES


DEFAULT_CONFIG = {
    "monthly_spending_limit": 2500.0,
    "category_limits": {
        "Dining": 250.0,
        "Groceries": 450.0,
        "Transport": 200.0,
        "Entertainment": 120.0,
    },
    "category_rules": DEFAULT_RULES,
}


def write_default_config(path: str | Path) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")


def load_config(path: str | Path | None) -> tuple[BudgetConfig, dict[str, list[str]]]:
    if path is None:
        return BudgetConfig(monthly_spending_limit=None, category_limits={}), DEFAULT_RULES

    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    budget = BudgetConfig(
        monthly_spending_limit=raw.get("monthly_spending_limit"),
        category_limits=raw.get("category_limits", {}),
    )
    rules = raw.get("category_rules", DEFAULT_RULES)
    return budget, rules
