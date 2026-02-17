import tempfile
import unittest

from jobtracker.db import connect, init_db
from jobtracker.repository import ApplicationRepository


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        # Each test gets an isolated SQLite file to avoid cross-test coupling.
        self.db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_file.close()
        self.conn = connect(self.db_file.name)
        init_db(self.conn)
        self.repo = ApplicationRepository(self.conn)

    def tearDown(self) -> None:
        self.conn.close()

    def test_add_and_list_application(self) -> None:
        # Verifies insert defaults and read-back mapping from DB -> model.
        app_id = self.repo.add_application(company="OpenAI", role="Python Engineer", source="Referral")
        self.assertGreater(app_id, 0)

        rows = self.repo.list_applications()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].company, "OpenAI")
        self.assertEqual(rows[0].status, "applied")

    def test_update_status(self) -> None:
        # Confirms status update path and filtered list query behavior.
        app_id = self.repo.add_application(company="Stripe", role="Backend Engineer")
        updated = self.repo.update_status(app_id, "interview")
        self.assertTrue(updated)
        rows = self.repo.list_applications(status="interview")
        self.assertEqual(len(rows), 1)


if __name__ == "__main__":
    unittest.main()
