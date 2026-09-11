import sqlite3
import tempfile
import unittest
from pathlib import Path

from al_mehdi.audit import AuditStore


class AuditStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.database = Path(self.tempdir.name) / "audit.db"
        self.store = AuditStore(self.database)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_empty_and_populated_chain_are_valid(self) -> None:
        self.assertTrue(self.store.verify_chain()["valid"])
        self.store.append("test", "one", {"value": 1})
        self.store.append("test", "two", {"value": 2})
        result = self.store.verify_chain()
        self.assertTrue(result["valid"])
        self.assertEqual(result["checked"], 2)

    def test_tampering_is_detected(self) -> None:
        self.store.append("test", "one", {"value": 1})
        with sqlite3.connect(self.database) as connection:
            connection.execute("UPDATE audit_records SET payload_json = ? WHERE sequence = 1", ('{"value":9}',))
        result = self.store.verify_chain()
        self.assertFalse(result["valid"])
        self.assertEqual(result["failed_sequence"], 1)


if __name__ == "__main__":
    unittest.main()

