# Contributing

Al-Mehdi welcomes defensive AI-safety improvements that preserve meaningful human control.

## Before proposing a change

1. Read `docs/SAFETY_POLICY.md` and `docs/THREAT_MODEL.md`.
2. Use synthetic or explicitly authorised data only.
3. Add tests for expected behaviour and safe failure.
4. Run the full local validation suite.
5. Explain how human authority, reversibility and auditability are preserved.

## Changes that will not be accepted

- autonomous retaliation or offensive intrusion;
- credential theft, persistence, evasion or destructive payloads;
- weapon or surveillance integration;
- uncontrolled self-modification or replication;
- removal of approval, audit or containment safeguards;
- real personal, clinical, confidential or governed data.

The 100-agent invariant and `recommend_only` action scope are release gates.

