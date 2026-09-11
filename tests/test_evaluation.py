import tempfile
import unittest
from pathlib import Path

from al_mehdi.evaluation import run_benchmark
from al_mehdi.orchestrator import SafetyOrchestrator


class EvaluationTests(unittest.TestCase):
    def test_benchmark_passes_and_never_authorizes_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            orchestrator = SafetyOrchestrator(Path(tempdir) / "audit.db")
            result = run_benchmark(orchestrator)

        self.assertTrue(result["passed"])
        self.assertEqual(result["scenarios_passed"], 6)
        self.assertEqual(result["scenarios_total"], 6)
        self.assertTrue(result["execution_invariant_passed"])
        self.assertTrue(result["audit_chain_valid"])
        self.assertTrue(all(not item["execution_authorized"] for item in result["results"]))


if __name__ == "__main__":
    unittest.main()
