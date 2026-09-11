"""Dependency-free local HTTP API and safety dashboard."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from typing import Any
from urllib.parse import parse_qs, urlparse

from .evaluation import run_benchmark
from .models import SafetyEvent
from .orchestrator import SafetyOrchestrator
from .simulator import build_scenario, scenario_names


MAX_BODY_BYTES = 64 * 1024


class SafetyRequestHandler(BaseHTTPRequestHandler):
    server_version = "AlMehdi/0.1"

    @property
    def orchestrator(self) -> SafetyOrchestrator:
        return self.server.orchestrator  # type: ignore[attr-defined]

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'",
        )
        self.send_header("Cache-Control", "no-store")

    def _json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > MAX_BODY_BYTES:
            raise ValueError(f"Request body must be between 1 and {MAX_BODY_BYTES} bytes")
        raw = self.rfile.read(content_length)
        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object")
        return payload

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            page = files("al_mehdi.web").joinpath("index.html").read_text(encoding="utf-8")
            self._html(page)
        elif parsed.path == "/health":
            self._json(self.orchestrator.health())
        elif parsed.path == "/api/v1/agents":
            query = parse_qs(parsed.query)
            team = query.get("team", [""])[0]
            agents = self.orchestrator.list_agents()
            if team:
                agents = [agent for agent in agents if agent["team"] == team]
            self._json({"count": len(agents), "agents": agents})
        elif parsed.path == "/api/v1/scenarios":
            self._json({"scenarios": scenario_names()})
        elif parsed.path == "/api/v1/runs":
            query = parse_qs(parsed.query)
            try:
                limit = int(query.get("limit", ["10"])[0])
            except ValueError:
                limit = 10
            self._json({"records": self.orchestrator.audit.recent(limit)})
        elif parsed.path == "/api/v1/audit/verify":
            self._json(self.orchestrator.audit.verify_chain())
        else:
            self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            payload = self._read_json()
            if parsed.path == "/api/v1/analyze":
                report = self.orchestrator.analyze(SafetyEvent.from_dict(payload))
            elif parsed.path == "/api/v1/simulate":
                name = str(payload.get("scenario", ""))
                report = self.orchestrator.analyze(build_scenario(name))
            elif parsed.path == "/api/v1/evaluate":
                self._json(run_benchmark(self.orchestrator), HTTPStatus.CREATED)
                return
            else:
                self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
                return
            self._json(report.to_dict(include_findings=True), HTTPStatus.CREATED)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            self._json({"error": "invalid_request", "message": str(exc)}, HTTPStatus.BAD_REQUEST)
        except Exception:
            # Avoid exposing internal details to clients. Full logging can be added by an operator.
            self._json({"error": "internal_error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[http] {self.address_string()} - {format % args}")


class SafetyHTTPServer(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int], orchestrator: SafetyOrchestrator) -> None:
        super().__init__(address, SafetyRequestHandler)
        self.orchestrator = orchestrator


def serve(
    host: str = "127.0.0.1",
    port: int = 8080,
    database_path: str = "runtime/al_mehdi.db",
) -> None:
    if host not in {"127.0.0.1", "localhost"}:
        print("WARNING: non-loopback binding exposes the dashboard to your network.")
    orchestrator = SafetyOrchestrator(database_path=database_path)
    server = SafetyHTTPServer((host, port), orchestrator)
    print(f"Al-Mehdi dashboard: http://{host}:{port}")
    print("Mode: recommendation-only; external actuation is disabled.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Al-Mehdi.")
    finally:
        server.server_close()
