import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.request import Request, urlopen

from al_mehdi.orchestrator import SafetyOrchestrator
from al_mehdi.service import SafetyHTTPServer


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        database = Path(self.tempdir.name) / "audit.db"
        self.server = SafetyHTTPServer(("127.0.0.1", 0), SafetyOrchestrator(database))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)
        self.tempdir.cleanup()

    def test_health(self) -> None:
        with urlopen(f"{self.base_url}/health", timeout=5) as response:
            payload = json.load(response)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["agents"], 100)
        self.assertFalse(payload["external_actuation"])

    def test_simulation_endpoint(self) -> None:
        request = Request(
            f"{self.base_url}/api/v1/simulate",
            data=json.dumps({"scenario": "prompt_injection"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=10) as response:
            payload = json.load(response)
        self.assertEqual(payload["decision"]["findings_count"], 100)
        self.assertFalse(payload["decision"]["execution_authorized"])


if __name__ == "__main__":
    unittest.main()

