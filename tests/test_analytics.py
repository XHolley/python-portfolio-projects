import unittest

from jobtracker.analytics import build_funnel_metrics
from jobtracker.models import JobApplication


class AnalyticsTests(unittest.TestCase):
    def test_metrics(self) -> None:
        # Mixed pipeline sample: applied, interview, offer, and rejected.
        apps = [
            JobApplication(1, "A", "Eng", "applied", "referral", "2026-01-01", "2026-01-01", ""),
            JobApplication(2, "B", "Eng", "interview", "linkedin", "2026-01-01", "2026-01-05", ""),
            JobApplication(3, "C", "Eng", "offer", "site", "2026-01-02", "2026-01-08", ""),
            JobApplication(4, "D", "Eng", "rejected", "site", "2026-01-02", "2026-01-06", ""),
        ]
        metrics = build_funnel_metrics(apps)
        # Expectations document how funnel KPIs should be interpreted.
        self.assertEqual(metrics.total, 4)
        self.assertEqual(metrics.interviews, 2)
        self.assertEqual(metrics.offers, 1)
        self.assertEqual(metrics.rejected, 1)
        self.assertAlmostEqual(metrics.response_rate, 1.0)
        self.assertAlmostEqual(metrics.offer_rate, 0.25)


if __name__ == "__main__":
    unittest.main()
