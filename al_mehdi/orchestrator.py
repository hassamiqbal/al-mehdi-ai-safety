"""Concurrent orchestration of the bounded 100-agent council."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

from .agents import SafetyAgent
from .audit import AuditStore
from .catalog import build_catalog
from .models import RunReport, SafetyEvent
from .policy import HumanAuthorityPolicy


class SafetyOrchestrator:
    def __init__(
        self,
        database_path: str | Path = "runtime/al_mehdi.db",
        max_workers: int = 16,
    ) -> None:
        self.specs = build_catalog()
        self.agents = tuple(SafetyAgent(spec) for spec in self.specs)
        self.policy = HumanAuthorityPolicy()
        self.audit = AuditStore(database_path)
        self.max_workers = max(1, min(int(max_workers), 32))

    def analyze(self, event: SafetyEvent) -> RunReport:
        run_id = f"run_{uuid4().hex[:16]}"
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="al-mehdi") as pool:
            findings = tuple(pool.map(lambda agent: agent.evaluate(event), self.agents))
        decision = self.policy.decide(run_id, event, findings)
        report = RunReport(event=event, decision=decision, findings=findings)
        self.audit.save_report(report)
        return report

    def list_agents(self) -> list[dict[str, object]]:
        return [spec.to_dict() for spec in self.specs]

    def health(self) -> dict[str, object]:
        chain = self.audit.verify_chain()
        return {
            "status": "ok" if chain["valid"] else "degraded",
            "version": "0.2.0",
            "agents": len(self.agents),
            "teams": len({spec.team for spec in self.specs}),
            "mode": "recommend_only",
            "external_actuation": False,
            "audit_chain": chain,
        }
