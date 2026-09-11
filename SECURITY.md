# Security Policy

## Supported version

Only the latest release is supported. Version 0.1.0 is an experimental, local, recommendation-only system.

## Reporting a vulnerability

Do not open a public issue containing exploit details, credentials, personal data or information about systems you do not own. Contact the repository owner privately through the security-advisory function on GitHub.

Include:

- affected version and component;
- a minimal reproduction using synthetic data;
- expected impact;
- suggested mitigation, if known.

Do not test against third-party systems. Do not access, retain or transmit data beyond what is necessary and authorised.

## Operational warning

The local HTTP service has no authentication in version 0.1.0. Keep it bound to `127.0.0.1`. The Docker example exposes it only on the loopback interface.

