"""SQLite-backed, hash-chained audit storage."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from pathlib import Path
from typing import Any

from .models import RunReport, utc_now


GENESIS_HASH = "0" * 64


class AuditStore:
    def __init__(self, database_path: str | Path = "runtime/al_mehdi.db") -> None:
        self.database_path = str(database_path)
        self._lock = threading.Lock()
        if self.database_path != ":memory:":
            Path(self.database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        self._initialise()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=15)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialise(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_records (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_type TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    previous_hash TEXT NOT NULL,
                    record_hash TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_audit_record_id ON audit_records(record_id)"
            )

    @staticmethod
    def _hash(record_type: str, record_id: str, payload_json: str, previous_hash: str, created_at: str) -> str:
        canonical = "|".join((record_type, record_id, payload_json, previous_hash, created_at))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def append(self, record_type: str, record_id: str, payload: dict[str, Any]) -> str:
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        created_at = utc_now()
        with self._lock, self._connect() as connection:
            previous_row = connection.execute(
                "SELECT record_hash FROM audit_records ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            previous_hash = previous_row["record_hash"] if previous_row else GENESIS_HASH
            record_hash = self._hash(record_type, record_id, payload_json, previous_hash, created_at)
            connection.execute(
                """
                INSERT INTO audit_records
                    (record_type, record_id, payload_json, previous_hash, record_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (record_type, record_id, payload_json, previous_hash, record_hash, created_at),
            )
        return record_hash

    def save_report(self, report: RunReport) -> str:
        return self.append("run_report", report.decision.run_id, report.to_dict(include_findings=True))

    def recent(self, limit: int = 20) -> list[dict[str, Any]]:
        safe_limit = max(1, min(int(limit), 200))
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM audit_records ORDER BY sequence DESC LIMIT ?", (safe_limit,)
            ).fetchall()
        return [
            {
                "sequence": row["sequence"],
                "record_type": row["record_type"],
                "record_id": row["record_id"],
                "payload": json.loads(row["payload_json"]),
                "previous_hash": row["previous_hash"],
                "record_hash": row["record_hash"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def verify_chain(self) -> dict[str, Any]:
        expected_previous = GENESIS_HASH
        checked = 0
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM audit_records ORDER BY sequence ASC").fetchall()
        for row in rows:
            expected_hash = self._hash(
                row["record_type"],
                row["record_id"],
                row["payload_json"],
                expected_previous,
                row["created_at"],
            )
            if row["previous_hash"] != expected_previous or row["record_hash"] != expected_hash:
                return {"valid": False, "checked": checked, "failed_sequence": row["sequence"]}
            expected_previous = row["record_hash"]
            checked += 1
        return {"valid": True, "checked": checked, "head_hash": expected_previous}

