import unittest

from finance_analyzer.categorization import build_default_categorizer


class CategorizationTests(unittest.TestCase):
    def test_income_always_income_for_positive_amounts(self) -> None:
        c = build_default_categorizer()
        self.assertEqual(c.categorize("Payroll ACME", 2300.0), "Income")

    def test_keyword_category_match(self) -> None:
        c = build_default_categorizer()
        self.assertEqual(c.categorize("Trader Joe weekly run", -85.10), "Groceries")

    def test_other_fallback(self) -> None:
        c = build_default_categorizer()
        self.assertEqual(c.categorize("Random merchant", -12.0), "Other")


if __name__ == "__main__":
    unittest.main()
