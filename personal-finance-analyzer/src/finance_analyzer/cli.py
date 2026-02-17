from __future__ import annotations

import argparse
from pathlib import Path

from .analytics import (
    assign_categories,
    category_spending_by_month,
    monthly_summaries,
    write_category_summary_csv,
    write_monthly_summary_csv,
)
from .budget import generate_budget_alerts
from .categorization import Categorizer
from .charts import write_category_bar_svg, write_spending_trend_svg
from .config import load_config, write_default_config
from .csvio import load_transactions, save_transactions_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="finance-analyzer",
        description="Analyze personal finance CSVs with auto-categorization, trends, and budget alerts.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init-config", help="Create starter JSON config file")
    init.add_argument("--output", default="finance_config.json")

    analyze = sub.add_parser("analyze", help="Run full analysis from input CSV")
    analyze.add_argument("--input", required=True, help="Path to bank CSV file")
    analyze.add_argument("--output-dir", default="reports", help="Directory for generated reports")
    analyze.add_argument("--config", default=None, help="JSON config with budget limits and category rules")

    return parser


def _build_markdown_report(
    out_path: Path,
    summaries,
    category_by_month,
    alerts,
    monthly_chart_name: str,
    category_chart_name: str,
) -> None:
    if summaries:
        latest = summaries[-1]
        headline = (
            f"Latest month: {latest.month} | Income: ${latest.income:.2f} | "
            f"Expenses: ${latest.expenses:.2f} | Net: ${latest.net:.2f} | "
            f"Savings Rate: {latest.savings_rate:.1%}"
        )
    else:
        headline = "No transactions available."

    lines = [
        "# Personal Finance Report",
        "",
        headline,
        "",
        "## Budget Alerts",
        "",
    ]
    lines.extend([f"- {alert}" for alert in alerts])
    lines.extend(
        [
            "",
            "## Charts",
            "",
            f"![Monthly Spending Trend]({monthly_chart_name})",
            "",
            f"![Latest Month Category Spending]({category_chart_name})",
            "",
            "## Output Files",
            "",
            "- normalized_transactions.csv",
            "- monthly_summary.csv",
            "- category_summary.csv",
            "- budget_alerts.txt",
            "",
        ]
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def cmd_analyze(input_path: str, output_dir: str, config_path: str | None) -> int:
    budget, rules = load_config(config_path)
    categorizer = Categorizer(rules=rules)

    transactions = load_transactions(input_path)
    assign_categories(transactions, categorizer.categorize)

    summaries = monthly_summaries(transactions)
    categories = category_spending_by_month(transactions)
    alerts = generate_budget_alerts(summaries, categories, budget)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    save_transactions_csv(out / "normalized_transactions.csv", transactions)
    write_monthly_summary_csv(out / "monthly_summary.csv", summaries)
    write_category_summary_csv(out / "category_summary.csv", categories)

    latest_month = summaries[-1].month if summaries else None
    latest_categories = categories.get(latest_month, {}) if latest_month else {}

    monthly_series = [(summary.month, summary.expenses) for summary in summaries]

    monthly_chart = "monthly_spending_trend.svg"
    category_chart = "latest_month_category_spending.svg"
    write_spending_trend_svg(out / monthly_chart, monthly_series)
    write_category_bar_svg(out / category_chart, latest_categories, "Latest Month Category Spending")

    (out / "budget_alerts.txt").write_text("\n".join(alerts) + "\n", encoding="utf-8")
    _build_markdown_report(out / "report.md", summaries, categories, alerts, monthly_chart, category_chart)

    print(f"Analyzed {len(transactions)} transactions")
    print(f"Generated reports in: {out.resolve()}")
    if summaries:
        latest = summaries[-1]
        print(
            f"Latest month {latest.month}: expenses=${latest.expenses:.2f}, "
            f"net=${latest.net:.2f}, savings_rate={latest.savings_rate:.1%}"
        )
    for alert in alerts:
        print(alert)

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init-config":
        write_default_config(args.output)
        print(f"Created config file: {args.output}")
        return 0

    if args.command == "analyze":
        return cmd_analyze(args.input, args.output_dir, args.config)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
