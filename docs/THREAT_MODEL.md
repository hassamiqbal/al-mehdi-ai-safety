# Threat Model

## Protected assets

- Human decision authority
- Audit integrity and incident evidence
- Safety policies and agent catalog
- Model and system configuration
- Credentials, private data and governed research assets
- Availability of authorised services

## Considered threats

- Prompt injection and instruction smuggling
- Goal or behaviour drift
- Attempts to bypass approval or shutdown
- Secret exposure and unauthorised access
- Data poisoning, poor provenance and privacy leakage
- Dependency and container supply-chain compromise
- Telemetry suppression and audit tampering
- Resource exhaustion and service failure
- Misleading confidence or unsupported claims

## Mitigations in version 0.1.0

- No tool execution, shell access, credential store or outbound connector in the agent layer
- Deterministic and inspectable agent rules
- Exactly 100 stable agent identities checked at startup and in CI
- Central policy aggregation and ten-team quorum
- Human approval flag for non-observational actions
- Hard-coded `execution_authorized = false`
- Hash-chained local audit records
- Localhost-only default service binding
- Request-size limits, schema validation and safe error messages
- Synthetic evaluation scenarios and regression tests

## Out of scope

- Defending the global internet
- Predicting every behaviour of an advanced AI system
- Operating as a security operations centre replacement
- Automatically disabling third-party infrastructure
- Offensive testing of systems not explicitly owned and authorised
- Formal verification or formal differential-privacy guarantees

## Residual risks

Rules can miss unfamiliar phrasing, event sources can mislabel severity, local administrators can replace the whole database, and the prototype lacks authentication. It must remain an advisory research environment until these risks are addressed and independently reviewed.

