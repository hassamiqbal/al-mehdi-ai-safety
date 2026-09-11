# Architecture

## Design objective

Al-Mehdi demonstrates how a large logical agent council can remain understandable, testable and subordinate to human authority. It avoids one hundred independent model calls. Instead, one immutable catalog supplies one hundred specialised evaluators to a bounded concurrent orchestrator.

## Components

### Agent catalog

`al_mehdi/catalog.py` defines ten teams and ten stable roles per team. Startup fails unless the registry contains exactly 100 unique IDs. Every specification has `action_scope = recommend_only`.

### Safety agents

`al_mehdi/agents.py` converts event text and trusted severity hints into explainable risk findings. Each finding includes the matched signals, confidence, risk score, rationale and recommendation.

### Orchestrator

`al_mehdi/orchestrator.py` evaluates all agents with a bounded thread pool. It has no outbound-network or shell-execution adapter.

### Human Authority Policy

`al_mehdi/policy.py` aggregates the strongest assessments from every team, requires team quorum and applies conservative severity floors. The policy always returns `execution_authorized = false`.

### Audit store

`al_mehdi/audit.py` stores each complete run as canonical JSON in SQLite. Each record incorporates the previous record hash, forming a SHA-256 chain. `audit-verify` detects modification, deletion from the middle of the chain or broken linkage. External anchoring is a future control.

### API and dashboard

`al_mehdi/service.py` uses Python's standard library to serve a local dashboard and JSON endpoints. Requests are limited to 64 KiB, errors do not expose stack traces and security headers are included. The default listener is `127.0.0.1`.

## Trust boundaries

| Boundary | Trusted | Untrusted |
| --- | --- | --- |
| Event intake | Schema validation and size limit | Event text and event source |
| Agent layer | Catalog identity and code | Any single agent finding |
| Policy layer | Human-authority invariants | Severity claims without corroboration |
| Storage | Local process at write time | Later file or database modification |
| Operator | Authenticated, accountable person | Anonymous remote instruction |

## Extension rule

New model providers or infrastructure adapters must be placed behind a deny-by-default interface and cannot be enabled merely by configuration. Their introduction requires a threat-model update, approval design, tests and a reviewed release.

