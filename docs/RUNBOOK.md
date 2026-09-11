# Operator Runbook

## 1. Verify before use

```bash
al-mehdi doctor
python -m unittest discover -s tests -v
```

Do not continue if the agent count is not 100 or audit health is degraded.

## 2. Start locally

```bash
al-mehdi serve
```

Use `127.0.0.1`. Do not expose the development service to the internet.

## 3. Begin with simulations

Run `normal_operation`, then `prompt_injection`, `goal_drift`, `data_exfiltration`, `supply_chain` and `audit_tamper`. Confirm that high-impact reports require human approval and never authorise execution.

## 4. Review a report

Check:

1. event source and evidence;
2. consensus risk and severity;
3. teams reporting;
4. matched signals and confidence;
5. recommended reversible response;
6. explicit `execution_authorized` value.

## 5. If the audit chain fails

- Stop using the affected environment.
- Preserve the database and surrounding logs as evidence.
- Compare with a trusted backup or external digest.
- Do not rewrite or "repair" the audit history.
- Start a clean environment only after accountable human review.

## 6. Recovery

Version 0.2.0 does not perform recovery actions. An authorised operator should follow the existing incident-response procedures of the system owner.
