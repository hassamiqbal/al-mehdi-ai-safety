"""The canonical registry of 100 bounded safety agents."""

from __future__ import annotations

from .models import AgentSpec


TEAM_CATALOG: dict[str, dict[str, object]] = {
    "governance": {
        "mission": "Protect human authority, rights, accountability and controlled change.",
        "signals": ("bypass approval", "no human", "self authorize", "policy override", "unaccountable"),
        "roles": (
            ("human_authority", "Human Authority Guardian", ("human override", "operator ignored")),
            ("constitutional_policy", "Constitutional Policy Auditor", ("constitutional rule", "policy conflict")),
            ("approval_gate", "Approval Gatekeeper", ("approval bypass", "unauthorized approval")),
            ("scope_control", "Mission Scope Controller", ("scope expansion", "mission creep")),
            ("rights_review", "Human Rights Reviewer", ("coercion", "rights violation")),
            ("accountability", "Accountability Mapper", ("unknown owner", "no accountable person")),
            ("evidence_standard", "Evidence Standard Reviewer", ("unsupported claim", "missing evidence")),
            ("change_control", "Change Control Guardian", ("unreviewed change", "unsigned release")),
            ("due_process", "Due Process Reviewer", ("irreversible decision", "no appeal")),
            ("mission_integrity", "Mission Integrity Monitor", ("goal replacement", "objective changed")),
        ),
    },
    "monitoring": {
        "mission": "Detect abnormal behaviour, access patterns and resource use in owned systems.",
        "signals": ("anomaly", "unexpected", "spike", "unknown process", "telemetry gap"),
        "roles": (
            ("telemetry", "Telemetry Sentinel", ("missing telemetry", "logging disabled")),
            ("behaviour_drift", "Behaviour Drift Monitor", ("behaviour drift", "output shift")),
            ("resource_use", "Resource Use Monitor", ("cpu spike", "gpu spike", "memory spike")),
            ("identity", "Identity Activity Monitor", ("unknown identity", "impossible login")),
            ("permissions", "Permission Change Monitor", ("permission escalation", "admin granted")),
            ("network", "Network Boundary Monitor", ("unknown endpoint", "unexpected egress")),
            ("data_flow", "Data Flow Monitor", ("bulk transfer", "unusual download")),
            ("model_output", "Model Output Monitor", ("unsafe output", "hidden instruction")),
            ("dependency", "Dependency Health Monitor", ("dependency change", "package anomaly")),
            ("third_party", "Third-Party Monitor", ("vendor incident", "external service changed")),
        ),
    },
    "security": {
        "mission": "Identify misuse and defensive security threats without counterattacking.",
        "signals": ("attack", "exploit", "unauthorized", "malicious", "compromise"),
        "roles": (
            ("threat_intel", "Defensive Threat Analyst", ("indicator of compromise", "threat campaign")),
            ("prompt_injection", "Prompt Injection Detector", ("ignore previous", "system prompt", "jailbreak")),
            ("data_poisoning", "Data Poisoning Detector", ("poisoned data", "label manipulation")),
            ("secret_exposure", "Secret Exposure Monitor", ("api key", "credential leak", "secret")),
            ("supply_chain", "Supply Chain Defender", ("typosquat", "malicious package")),
            ("api_abuse", "API Abuse Monitor", ("rate abuse", "token theft")),
            ("container", "Container Security Reviewer", ("privileged container", "host mount")),
            ("model_theft", "Model Asset Guardian", ("model extraction", "weights exfiltration")),
            ("access_control", "Access Control Auditor", ("access bypass", "broken authorization")),
            ("incident_triage", "Security Triage Agent", ("active compromise", "security incident")),
        ),
    },
    "alignment": {
        "mission": "Assess goal integrity, truthfulness, corrigibility and bounded autonomy.",
        "signals": ("deception", "power seeking", "resist shutdown", "self replication", "goal drift"),
        "roles": (
            ("goal_drift", "Goal Drift Assessor", ("objective drift", "misaligned goal")),
            ("deception", "Deception Indicator Assessor", ("conceal", "mislead", "false report")),
            ("power_seeking", "Power-Seeking Heuristic Monitor", ("gain control", "acquire resources")),
            ("shutdown", "Shutdown Compliance Checker", ("ignore shutdown", "prevent stop")),
            ("corrigibility", "Corrigibility Assessor", ("resist correction", "reject feedback")),
            ("honesty", "Truthfulness Evaluator", ("fabricated", "unsupported certainty")),
            ("uncertainty", "Uncertainty Calibration Agent", ("overconfident", "no uncertainty")),
            ("value_conflict", "Value Conflict Assessor", ("human values conflict", "harm tradeoff")),
            ("autonomy_limit", "Autonomy Boundary Monitor", ("autonomous execution", "unsupervised action")),
            ("human_override", "Override Responsiveness Tester", ("override rejected", "operator command ignored")),
        ),
    },
    "data_governance": {
        "mission": "Protect data through minimisation, provenance, consent and access controls.",
        "signals": ("personal data", "sensitive data", "unknown provenance", "retention", "data leak"),
        "roles": (
            ("classification", "Data Classification Agent", ("unclassified data", "sensitivity unknown")),
            ("minimisation", "Data Minimisation Agent", ("excess data", "unnecessary fields")),
            ("provenance", "Data Provenance Verifier", ("source unknown", "provenance missing")),
            ("consent", "Consent Boundary Reviewer", ("consent missing", "secondary use")),
            ("retention", "Retention Policy Monitor", ("retained too long", "deletion overdue")),
            ("privacy", "Privacy Risk Assessor", ("re-identification", "pii", "phi")),
            ("quality", "Data Quality Monitor", ("invalid date", "duplicate record", "data corruption")),
            ("bias", "Dataset Bias Assessor", ("representation gap", "sampling bias")),
            ("access", "Dataset Access Guardian", ("unauthorized dataset", "public bucket")),
            ("synthetic", "Synthetic Data Reviewer", ("memorization", "membership inference")),
        ),
    },
    "evaluation": {
        "mission": "Measure safety, robustness, calibration, fairness and reproducibility.",
        "signals": ("evaluation failed", "benchmark drop", "unsafe test", "unreproducible", "calibration error"),
        "roles": (
            ("red_team", "Safe Red-Team Simulator", ("adversarial scenario", "red team")),
            ("robustness", "Robustness Evaluator", ("perturbation failure", "fragile model")),
            ("calibration", "Calibration Evaluator", ("miscalibrated", "brier")),
            ("hallucination", "Hallucination Evaluator", ("hallucination", "invented source")),
            ("fairness", "Fairness Evaluator", ("group disparity", "unfair outcome")),
            ("misuse", "Misuse Evaluation Agent", ("dual use", "misuse pathway")),
            ("cyber_safety", "Cyber-Safety Evaluator", ("unsafe code", "exploit generation")),
            ("benchmark", "Benchmark Integrity Agent", ("data leakage", "benchmark contamination")),
            ("reproducibility", "Reproducibility Agent", ("random seed missing", "environment mismatch")),
            ("regression", "Safety Regression Monitor", ("safety regression", "control failure")),
        ),
    },
    "containment": {
        "mission": "Recommend reversible containment actions for authorised human operators.",
        "signals": ("contain", "quarantine", "isolate", "revoke", "emergency stop"),
        "roles": (
            ("quarantine", "Quarantine Planner", ("quarantine service", "quarantine model")),
            ("kill_switch", "Emergency Stop Coordinator", ("kill switch", "stop service")),
            ("rate_limit", "Rate-Limit Planner", ("rate limit", "traffic surge")),
            ("network_isolation", "Network Isolation Planner", ("disconnect network", "block egress")),
            ("key_revocation", "Credential Revocation Planner", ("revoke key", "rotate secret")),
            ("rollback", "Rollback Planner", ("rollback release", "last known good")),
            ("dependency_freeze", "Dependency Freeze Planner", ("freeze dependency", "lock version")),
            ("sandbox", "Sandbox Integrity Verifier", ("sandbox escape", "boundary violation")),
            ("safe_mode", "Safe-Mode Planner", ("degraded mode", "read only mode")),
            ("recovery_gate", "Recovery Gatekeeper", ("resume service", "exit quarantine")),
        ),
    },
    "incident_response": {
        "mission": "Coordinate evidence, severity, communication and accountable remediation.",
        "signals": ("incident", "breach", "outage", "escalate", "postmortem"),
        "roles": (
            ("commander", "Incident Commander", ("incident declared", "command structure")),
            ("evidence", "Evidence Collector", ("collect evidence", "preserve logs")),
            ("severity", "Severity Classifier", ("critical impact", "severity level")),
            ("timeline", "Timeline Reconstructor", ("event timeline", "first observed")),
            ("communications", "Communications Drafter", ("status update", "notify stakeholders")),
            ("stakeholders", "Stakeholder Mapper", ("affected users", "system owner")),
            ("compliance", "Compliance Liaison", ("reportable incident", "regulatory notice")),
            ("remediation", "Remediation Tracker", ("fix owner", "remediation overdue")),
            ("postmortem", "Post-Incident Reviewer", ("root cause", "lessons learned")),
            ("handover", "Incident Handover Agent", ("shift handover", "context lost")),
        ),
    },
    "resilience": {
        "mission": "Preserve integrity and recoverability through tested, reversible controls.",
        "signals": ("backup failure", "integrity failure", "single point", "recovery failed", "service unavailable"),
        "roles": (
            ("backup", "Backup Assurance Agent", ("backup missing", "restore point")),
            ("failover", "Failover Readiness Agent", ("failover failed", "replica unavailable")),
            ("integrity", "Integrity Verification Agent", ("hash mismatch", "tampered record")),
            ("disaster_recovery", "Disaster Recovery Planner", ("disaster recovery", "regional outage")),
            ("continuity", "Service Continuity Agent", ("continuity risk", "critical dependency")),
            ("recovery_test", "Recovery Test Agent", ("restore test overdue", "untested recovery")),
            ("baseline", "Configuration Baseline Agent", ("config drift", "baseline mismatch")),
            ("chaos", "Bounded Chaos Test Planner", ("chaos experiment", "fault injection")),
            ("fallback", "Human Fallback Planner", ("manual fallback", "human procedure")),
            ("capacity", "Resilience Capacity Monitor", ("capacity exhausted", "queue backlog")),
        ),
    },
    "assurance": {
        "mission": "Maintain safety cases, documentation, control coverage and release evidence.",
        "signals": ("missing documentation", "control gap", "audit finding", "release blocked", "assurance failure"),
        "roles": (
            ("model_card", "Model Card Curator", ("model card missing", "limitation undocumented")),
            ("system_card", "System Card Curator", ("system card missing", "deployment context missing")),
            ("risk_register", "Risk Register Custodian", ("risk unowned", "risk register stale")),
            ("audit", "Independent Audit Agent", ("audit exception", "evidence missing")),
            ("compliance_map", "Control Mapping Agent", ("control unmapped", "requirement gap")),
            ("coverage", "Safety Control Coverage Agent", ("control coverage low", "untested control")),
            ("safety_case", "Safety Case Builder", ("claim unsupported", "assurance argument")),
            ("release", "Release Readiness Gate", ("release candidate", "failed gate")),
            ("independent_review", "Independent Review Coordinator", ("review conflict", "second reviewer missing")),
            ("transparency", "Transparency Report Agent", ("disclosure missing", "metric omitted")),
        ),
    },
}


def build_catalog() -> tuple[AgentSpec, ...]:
    """Build and validate the immutable 100-agent catalog."""
    agents: list[AgentSpec] = []
    for team_index, (team, data) in enumerate(TEAM_CATALOG.items(), start=1):
        team_mission = str(data["mission"])
        team_signals = tuple(str(item).lower() for item in data["signals"])
        for role_index, (slug, title, role_signals) in enumerate(data["roles"], start=1):
            agents.append(
                AgentSpec(
                    agent_id=f"AM-{team_index:02d}-{role_index:02d}",
                    name=str(title),
                    team=team,
                    mission=f"{team_mission} Primary responsibility: {str(title).lower()}.",
                    signals=tuple(dict.fromkeys(team_signals + tuple(str(s).lower() for s in role_signals))),
                    weight=1.0,
                    action_scope="recommend_only",
                )
            )
    if len(agents) != 100:
        raise RuntimeError(f"Catalog invariant failed: expected 100 agents, found {len(agents)}")
    if len({agent.agent_id for agent in agents}) != 100:
        raise RuntimeError("Catalog invariant failed: agent IDs must be unique")
    return tuple(agents)

