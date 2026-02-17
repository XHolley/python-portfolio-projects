# Personal Finance Analyzer

Portfolio-grade Python project that imports bank CSV data, auto-categorizes transactions, computes monthly trends, generates SVG charts, and emits budget alerts.

## Highlights
- Flexible CSV ingestion (`Amount` or `Debit/Credit` formats)
- Rule-based auto-categorization with customizable keyword rules
- Monthly analytics: income, expenses, net, savings rate
- Budget alerts for total monthly spend + category overspend
- Report artifacts: CSV outputs, SVG charts, Markdown summary
- Unit tests for parser, categorization, and end-to-end pipeline

## Quick Start
```bash
cd personal-finance-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

finance-analyzer init-config --output finance_config.json
finance-analyzer analyze --input examples/bank_sample.csv --config finance_config.json --output-dir reports
```

If you do not install editable package, run with:
```bash
PYTHONPATH=src python3 -m finance_analyzer.cli init-config --output finance_config.json
PYTHONPATH=src python3 -m finance_analyzer.cli analyze --input examples/bank_sample.csv --config finance_config.json --output-dir reports
```

## Output Files
- `reports/normalized_transactions.csv`
- `reports/monthly_summary.csv`
- `reports/category_summary.csv`
- `reports/monthly_spending_trend.svg`
- `reports/latest_month_category_spending.svg`
- `reports/budget_alerts.txt`
- `reports/report.md`

## Config Format (`finance_config.json`)
```json
{
  "monthly_spending_limit": 2500.0,
  "category_limits": {
    "Dining": 250.0,
    "Groceries": 450.0,
    "Transport": 200.0,
    "Entertainment": 120.0
  },
  "category_rules": {
    "Groceries": ["whole foods", "trader joe", "market"],
    "Dining": ["restaurant", "coffee", "doordash"],
    "Income": ["payroll", "salary"]
  }
}
```

## Tests
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py"
```

## Resume Bullets
- Built a Python finance analytics CLI that normalizes raw bank exports into categorized spending and monthly KPI reports.
- Designed a configurable rule engine for transaction categorization and budget-alert generation.
- Implemented automated report generation (CSV + SVG + Markdown) with test coverage across ingestion and pipeline stages.
