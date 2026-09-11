"""Deterministic, explainable safety-agent implementation."""

from __future__ import annotations

from .models import AgentSpec, Finding, SafetyEvent, Severity


SEVERITY_BASE = {
    Severity.INFO: 4.0,
    Severity.LOW: 14.0,
    Severity.MEDIUM: 34.0,
    Severity.HIGH: 60.0,
    Severity.CRITICAL: 82.0,
}

HIGH_RISK_TERMS = (
    "autonomous execution",
    "bypass approval",
    "disable logging",
    "delete evidence",
    "exfiltrate",
    "gain control",
    "ignore shutdown",
    "self replication",
    "steal credential",
    "weapons",
)


class SafetyAgent:
    """A bounded evaluator that can recommend actions but cannot execute them."""

    def __init__(self, spec: AgentSpec) -> None:
        self.spec = spec

    def evaluate(self, event: SafetyEvent) -> Finding:
        text = event.text()
        matched = tuple(signal for signal in self.spec.signals if signal in text)
        dangerous = tuple(term for term in HIGH_RISK_TERMS if term in text)
        base = SEVERITY_BASE[event.severity_hint]

        score = base * (0.28 if not matched else 0.55)
        score += min(42.0, len(matched) * 13.0)
        score += min(24.0, len(dangerous) * 12.0)
        if event.requested_action.lower() not in {"observe", "report", "none"}:
            score += 9.0
        score = round(max(0.0, min(100.0, score * self.spec.weight)), 2)

        confidence = 0.34 + (0.12 * len(matched)) + (0.08 * len(dangerous))
        if event.severity_hint in {Severity.HIGH, Severity.CRITICAL}:
            confidence += 0.08
        confidence = round(max(0.2, min(0.98, confidence)), 2)

        if score >= 75:
            recommendation = "Recommend immediate human review and reversible emergency containment."
        elif score >= 50:
            recommendation = "Recommend human-authorised containment and evidence preservation."
        elif score >= 25:
            recommendation = "Escalate to a human operator for investigation."
        else:
            recommendation = "Continue monitoring and preserve telemetry."

        evidence = tuple(dict.fromkeys(matched + dangerous))
        rationale = (
            f"Detected {len(evidence)} relevant signal(s) within the {self.spec.team} mandate. "
            f"Severity hint was {event.severity_hint.value}; this agent is recommendation-only."
        )
        return Finding(
            agent_id=self.spec.agent_id,
            agent_name=self.spec.name,
            team=self.spec.team,
            risk_score=score,
            confidence=confidence,
            matched_signals=evidence,
            rationale=rationale,
            recommendation=recommendation,
        )

