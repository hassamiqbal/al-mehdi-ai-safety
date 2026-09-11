"""Typed domain models used throughout Al-Mehdi."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DecisionStatus(str, Enum):
    MONITOR = "monitor"
    HUMAN_REVIEW = "human_review"
    CONTAINMENT_RECOMMENDED = "containment_recommended"
    EMERGENCY_STOP_RECOMMENDED = "emergency_stop_recommended"


@dataclass(frozen=True)
class AgentSpec:
    agent_id: str
    name: str
    team: str
    mission: str
    signals: tuple[str, ...]
    weight: float = 1.0
    action_scope: str = "recommend_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SafetyEvent:
    summary: str
    source: str = "manual"
    category: str = "unspecified"
    details: dict[str, Any] = field(default_factory=dict)
    severity_hint: Severity = Severity.INFO
    requested_action: str = "observe"
    event_id: str = field(default_factory=lambda: f"evt_{uuid4().hex[:16]}")
    created_at: str = field(default_factory=utc_now)

    def text(self) -> str:
        detail_text = " ".join(f"{key} {value}" for key, value in sorted(self.details.items()))
        return f"{self.summary} {self.source} {self.category} {self.requested_action} {detail_text}".lower()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity_hint"] = self.severity_hint.value
        return data

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SafetyEvent":
        try:
            severity = Severity(str(payload.get("severity_hint", "info")).lower())
        except ValueError:
            severity = Severity.INFO
        details = payload.get("details") or {}
        if not isinstance(details, dict):
            raise ValueError("details must be a JSON object")
        summary = str(payload.get("summary", "")).strip()
        if not summary:
            raise ValueError("summary is required")
        return cls(
            summary=summary,
            source=str(payload.get("source", "manual"))[:120],
            category=str(payload.get("category", "unspecified"))[:120],
            details=details,
            severity_hint=severity,
            requested_action=str(payload.get("requested_action", "observe"))[:120],
        )


@dataclass(frozen=True)
class Finding:
    agent_id: str
    agent_name: str
    team: str
    risk_score: float
    confidence: float
    matched_signals: tuple[str, ...]
    rationale: str
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SafetyDecision:
    run_id: str
    event_id: str
    status: DecisionStatus
    severity: Severity
    consensus_risk: float
    human_approval_required: bool
    execution_authorized: bool
    teams_reporting: int
    findings_count: int
    team_scores: dict[str, float]
    recommendations: tuple[str, ...]
    policy_reasons: tuple[str, ...]
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["severity"] = self.severity.value
        return data


@dataclass(frozen=True)
class RunReport:
    event: SafetyEvent
    decision: SafetyDecision
    findings: tuple[Finding, ...]

    def to_dict(self, include_findings: bool = True) -> dict[str, Any]:
        result = {
            "event": self.event.to_dict(),
            "decision": self.decision.to_dict(),
        }
        if include_findings:
            result["findings"] = [finding.to_dict() for finding in self.findings]
        return result

