"""Central policy engine. Agents never bypass this layer."""

from __future__ import annotations

from statistics import fmean

from .models import DecisionStatus, Finding, SafetyDecision, SafetyEvent, Severity


SEVERITY_FLOOR = {
    Severity.INFO: 0.0,
    Severity.LOW: 12.0,
    Severity.MEDIUM: 30.0,
    Severity.HIGH: 52.0,
    Severity.CRITICAL: 75.0,
}


def _severity_from_risk(risk: float) -> Severity:
    if risk >= 75:
        return Severity.CRITICAL
    if risk >= 50:
        return Severity.HIGH
    if risk >= 25:
        return Severity.MEDIUM
    if risk >= 10:
        return Severity.LOW
    return Severity.INFO


def _status_from_risk(risk: float) -> DecisionStatus:
    if risk >= 75:
        return DecisionStatus.EMERGENCY_STOP_RECOMMENDED
    if risk >= 50:
        return DecisionStatus.CONTAINMENT_RECOMMENDED
    if risk >= 25:
        return DecisionStatus.HUMAN_REVIEW
    return DecisionStatus.MONITOR


class HumanAuthorityPolicy:
    """Aggregate findings while preserving human authority and reversibility."""

    def decide(self, run_id: str, event: SafetyEvent, findings: tuple[Finding, ...]) -> SafetyDecision:
        if not findings:
            raise ValueError("At least one finding is required")

        grouped: dict[str, list[float]] = {}
        for finding in findings:
            grouped.setdefault(finding.team, []).append(finding.risk_score)

        # Each team contributes the mean of its three strongest assessments.
        team_scores = {
            team: round(fmean(sorted(scores, reverse=True)[:3]), 2)
            for team, scores in grouped.items()
        }
        ordered = sorted((finding.risk_score for finding in findings), reverse=True)
        top_decile = ordered[: max(1, len(ordered) // 10)]
        calculated_risk = (0.65 * fmean(team_scores.values())) + (0.35 * fmean(top_decile))
        # A trusted upstream severity hint acts as a conservative floor, never as a downgrade.
        consensus = round(max(calculated_risk, SEVERITY_FLOOR[event.severity_hint]), 2)
        status = _status_from_risk(consensus)
        human_required = status != DecisionStatus.MONITOR or event.requested_action.lower() not in {
            "observe",
            "report",
            "none",
        }

        ranked = sorted(findings, key=lambda item: (item.risk_score, item.confidence), reverse=True)
        recommendations = tuple(dict.fromkeys(item.recommendation for item in ranked[:20]))
        reasons = [
            "All agent outputs are advisory; direct external actuation is disabled.",
            "Any containment or recovery action requires an authenticated human operator.",
            "Evidence preservation and reversible controls take priority over destructive action.",
        ]
        if len(grouped) < 6:
            reasons.append("Insufficient team quorum; automatic escalation is required.")
            human_required = True

        return SafetyDecision(
            run_id=run_id,
            event_id=event.event_id,
            status=status,
            severity=_severity_from_risk(consensus),
            consensus_risk=consensus,
            human_approval_required=human_required,
            execution_authorized=False,
            teams_reporting=len(grouped),
            findings_count=len(findings),
            team_scores=dict(sorted(team_scores.items())),
            recommendations=recommendations,
            policy_reasons=tuple(reasons),
        )
