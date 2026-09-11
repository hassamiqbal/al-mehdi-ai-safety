import tempfile
import unittest
from pathlib import Path

from al_mehdi.models import DecisionStatus, SafetyEvent, Severity
from al_mehdi.orchestrator import SafetyOrchestrator
from al_mehdi.simulator import build_scenario


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.database = Path(self.tempdir.name) / "audit.db"
        self.orchestrator = SafetyOrchestrator(self.database, max_workers=8)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_normal_operation_is_monitored(self) -> None:
        report = self.orchestrator.analyze(build_scenario("normal_operation"))
        self.assertEqual(report.decision.status, DecisionStatus.MONITOR)
        self.assertFalse(report.decision.execution_authorized)
        self.assertEqual(report.decision.findings_count, 100)
        self.assertEqual(report.decision.teams_reporting, 10)

    def test_critical_goal_drift_recommends_emergency_stop(self) -> None:
        report = self.orchestrator.analyze(build_scenario("goal_drift"))
        self.assertEqual(report.decision.status, DecisionStatus.EMERGENCY_STOP_RECOMMENDED)
        self.assertEqual(report.decision.severity, Severity.CRITICAL)
        self.assertTrue(report.decision.human_approval_required)
        self.assertFalse(report.decision.execution_authorized)

    def test_manual_external_action_requires_human_review(self) -> None:
        event = SafetyEvent(
            summary="Routine configuration proposal",
            severity_hint=Severity.INFO,
            requested_action="deploy change",
        )
        report = self.orchestrator.analyze(event)
        self.assertTrue(report.decision.human_approval_required)
        self.assertFalse(report.decision.execution_authorized)


if __name__ == "__main__":
    unittest.main()

