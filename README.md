# python-portfolio-projects

Portfolio-ready Python projects:
- Job Application Tracker CLI with SQLite analytics
- Personal Finance Analyzer with CSV import, auto-categorization, trend charts, and budget alerts

## Projects

### 1) Job Application Tracker (`/`)
A Python CLI app for tracking job applications and funnel metrics.

### 2) Personal Finance Analyzer (`personal-finance-analyzer/`)
A Python CLI app that imports bank CSVs, categorizes transactions, generates monthly spending charts, and creates budget alerts.

## Quick Start

### Job Tracker
```bash
PYTHONPATH=src python3 -m jobtracker.cli --db applications.db init-db
PYTHONPATH=src python3 -m jobtracker.cli --db applications.db add --company "OpenAI" --role "Software Engineer"
PYTHONPATH=src python3 -m jobtracker.cli --db applications.db stats
```

### Finance Analyzer
```bash
cd personal-finance-analyzer
PYTHONPATH=src python3 -m finance_analyzer.cli init-config --output finance_config.json
PYTHONPATH=src python3 -m finance_analyzer.cli analyze --input examples/bank_sample.csv --config finance_config.json --output-dir reports
```
