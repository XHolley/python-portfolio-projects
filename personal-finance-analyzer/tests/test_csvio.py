import tempfile
import unittest
from pathlib import Path

from finance_analyzer.csvio import load_transactions


class CsvIoTests(unittest.TestCase):
    def test_amount_column_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "transactions.csv"
            path.write_text(
                "Date,Description,Amount\n"
                "2026-01-03,Payroll,2500\n"
                "2026-01-04,Whole Foods,-91.22\n",
                encoding="utf-8",
            )
            txs = load_transactions(path)
            self.assertEqual(len(txs), 2)
            self.assertEqual(txs[0].amount, 2500.0)
            self.assertEqual(txs[1].amount, -91.22)

    def test_debit_credit_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "transactions.csv"
            path.write_text(
                "Date,Description,Debit,Credit\n"
                "01/03/2026,Payroll,0,2500\n"
                "01/04/2026,Coffee,5.50,0\n",
                encoding="utf-8",
            )
            txs = load_transactions(path)
            self.assertEqual(txs[0].amount, 2500.0)
            self.assertEqual(txs[1].amount, -5.5)


if __name__ == "__main__":
    unittest.main()
