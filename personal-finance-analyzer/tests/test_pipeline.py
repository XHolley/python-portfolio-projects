import tempfile
import unittest
from pathlib import Path

from finance_analyzer.cli import cmd_analyze
from finance_analyzer.config import write_default_config


class PipelineTests(unittest.TestCase):
    def test_full_pipeline_generates_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            csv_path = tmp / "input.csv"
            config_path = tmp / "config.json"
            out_dir = tmp / "reports"

            csv_path.write_text(
                "Date,Description,Amount\n"
                "2026-01-01,Payroll ACME,4000\n"
                "2026-01-02,Rent January,-1500\n"
                "2026-01-03,Trader Joe,-130\n"
                "2026-01-04,Netflix,-16.99\n",
                encoding="utf-8",
            )
            write_default_config(config_path)

            rc = cmd_analyze(str(csv_path), str(out_dir), str(config_path))
            self.assertEqual(rc, 0)

            expected = [
                "normalized_transactions.csv",
                "monthly_summary.csv",
                "category_summary.csv",
                "budget_alerts.txt",
                "monthly_spending_trend.svg",
                "latest_month_category_spending.svg",
                "report.md",
            ]
            for name in expected:
                self.assertTrue((out_dir / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
