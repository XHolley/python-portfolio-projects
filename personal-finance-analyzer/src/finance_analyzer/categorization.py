from __future__ import annotations

from dataclasses import dataclass


DEFAULT_RULES: dict[str, list[str]] = {
    "Housing": ["rent", "mortgage", "apartment"],
    "Groceries": ["grocery", "market", "whole foods", "trader joe", "aldi", "kroger"],
    "Dining": ["restaurant", "coffee", "cafe", "uber eats", "doordash", "grubhub"],
    "Transport": ["uber", "lyft", "gas", "shell", "chevron", "transit", "metro"],
    "Utilities": ["electric", "water", "internet", "verizon", "att", "t-mobile"],
    "Entertainment": ["netflix", "spotify", "hulu", "movie", "steam"],
    "Healthcare": ["pharmacy", "clinic", "hospital", "medical", "dental"],
    "Income": ["payroll", "salary", "direct deposit", "bonus", "refund"],
}


@dataclass(slots=True)
class Categorizer:
    rules: dict[str, list[str]]

    def categorize(self, description: str, amount: float) -> str:
        text = description.lower()

        # Positive amounts are usually income/refunds.
        if amount > 0:
            if any(key in text for key in self.rules.get("Income", [])):
                return "Income"
            return "Income"

        for category, keywords in self.rules.items():
            if category == "Income":
                continue
            if any(word in text for word in keywords):
                return category
        return "Other"


def build_default_categorizer() -> Categorizer:
    return Categorizer(rules=DEFAULT_RULES)
