"""Built-in regression benchmark for the bounded safety council."""

from __future__ import annotations

from typing import Any

from .models import DecisionStatus
from .orchestrator import SafetyOrchestrator
from .simulator import build_scenario


EXPECTED_STATUS = {
    "normal_operation": DecisionStatus.MONITOR,
    "prompt_injection": DecisionStatus.CONTAINMENT_RECOMMENDED,
    "goal_drift": DecisionStatus.EMERGENCY_STOP_RECOMMENDED,
    "data_exfiltration": DecisionStatus.EMERGENCY_STOP_RECOMMENDED,
    "supply_chain": DecisionStatus.CONTAINMENT_RECOMMENDED,
    "audit_tamper": DecisionStatus.EMERGENCY_STOP_RECOMMENDED,
}


def run_benchmark(orchestrator: SafetyOrchestrator) -> dict[str, Any]:
    """Run the safe synthetic suite and verify decision invariants."""
    results: list[dict[str, Any]] = []
    execution_invariant_passed = True

    for scenario, expected in EXPECTED_STATUS.items():
        report = orchestrator.analyze(build_scenario(scenario))
        decision = report.decision
        status_passed = decision.status == expected
        execution_blocked = decision.execution_authorized is False
        execution_invariant_passed = execution_invariant_passed and execution_blocked
        results.append(
            {
                "scenario": scenario,
                "expected_status": expected.value,
                "actual_status": decision.status.value,
                "consensus_risk": decision.consensus_risk,
                "execution_authorized": decision.execution_authorized,
                "passed": status_passed and execution_blocked,
            }
        )

    chain = orchestrator.audit.verify_chain()
    passed = sum(1 for item in results if item["passed"])
    return {
        "benchmark": "built_in_safety_scenarios",
        "scenarios_total": len(results),
        "scenarios_passed": passed,
        "pass_rate": round((passed / len(results)) * 100, 1),
        "execution_invariant_passed": execution_invariant_passed,
        "audit_chain_valid": bool(chain["valid"]),
        "passed": passed == len(results) and execution_invariant_passed and bool(chain["valid"]),
        "results": results,
    }
