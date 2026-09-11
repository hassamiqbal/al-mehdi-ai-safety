"""Command-line interface for operators and first-time users."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .models import SafetyEvent, Severity
from .orchestrator import SafetyOrchestrator
from .service import serve
from .simulator import build_scenario, scenario_names


def _db_path(value: str | None) -> str:
    return value or os.getenv("AL_MEHDI_DB", "runtime/al_mehdi.db")


def _print_report(report: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    decision = report["decision"]
    event = report["event"]
    assert isinstance(decision, dict) and isinstance(event, dict)
    print(f"Event: {event['summary']}")
    print(f"Decision: {decision['status']}")
    print(f"Consensus risk: {decision['consensus_risk']}/100 ({decision['severity']})")
    print(f"Teams reporting: {decision['teams_reporting']}/10")
    print(f"Human approval required: {decision['human_approval_required']}")
    print("External execution authorised: False")
    print("Recommendations:")
    for item in decision["recommendations"]:
        print(f"  - {item}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="al-mehdi",
        description="Human-governed 100-agent AI safety laboratory.",
    )
    parser.add_argument("--db", help="SQLite audit database path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Validate catalog and audit health")
    doctor.add_argument("--json", action="store_true")

    agents = subparsers.add_parser("agents", help="List registered agents")
    agents.add_argument("--team")
    agents.add_argument("--json", action="store_true")

    demo = subparsers.add_parser("demo", help="Run a safe synthetic scenario")
    demo.add_argument("scenario", nargs="?", default="prompt_injection", choices=scenario_names())
    demo.add_argument("--json", action="store_true")

    analyze = subparsers.add_parser("analyze", help="Analyze a manually described event")
    analyze.add_argument("--summary", required=True)
    analyze.add_argument("--source", default="manual")
    analyze.add_argument("--category", default="unspecified")
    analyze.add_argument("--severity", choices=[item.value for item in Severity], default="info")
    analyze.add_argument("--requested-action", default="observe")
    analyze.add_argument("--json", action="store_true")

    audit = subparsers.add_parser("audit-verify", help="Verify the hash-chained audit log")
    audit.add_argument("--json", action="store_true")

    server = subparsers.add_parser("serve", help="Start the local API and dashboard")
    server.add_argument("--host", default="127.0.0.1")
    server.add_argument("--port", type=int, default=8080)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    database_path = _db_path(args.db)

    if args.command == "serve":
        serve(args.host, args.port, database_path)
        return 0

    orchestrator = SafetyOrchestrator(database_path=database_path)
    if args.command == "doctor":
        health = orchestrator.health()
        if args.json:
            print(json.dumps(health, indent=2))
        else:
            print("Al-Mehdi system check")
            for key, value in health.items():
                print(f"  {key}: {value}")
        return 0 if health["status"] == "ok" else 1

    if args.command == "agents":
        items = orchestrator.list_agents()
        if args.team:
            items = [item for item in items if item["team"] == args.team]
        if args.json:
            print(json.dumps(items, indent=2))
        else:
            for item in items:
                print(f"{item['agent_id']}  {item['team']:<18}  {item['name']}")
            print(f"Total: {len(items)}")
        return 0

    if args.command == "demo":
        report = orchestrator.analyze(build_scenario(args.scenario))
        _print_report(report.to_dict(include_findings=args.json), args.json)
        return 0

    if args.command == "analyze":
        event = SafetyEvent(
            summary=args.summary,
            source=args.source,
            category=args.category,
            severity_hint=Severity(args.severity),
            requested_action=args.requested_action,
        )
        report = orchestrator.analyze(event)
        _print_report(report.to_dict(include_findings=args.json), args.json)
        return 0

    if args.command == "audit-verify":
        result = orchestrator.audit.verify_chain()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Audit chain valid: {result['valid']} ({result['checked']} records checked)")
        return 0 if result["valid"] else 1

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

