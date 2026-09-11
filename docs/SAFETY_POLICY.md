# Safety Policy

## Authority

Human operators retain final authority. Agent consensus is evidence for a decision, not permission to act.

## Prohibited capabilities

Al-Mehdi must not include:

- autonomous retaliation or offensive intrusion;
- credential theft, persistence, evasion or destructive malware;
- weapon targeting or control;
- uncontrolled self-replication or self-modification;
- covert surveillance of people;
- irreversible action without accountable human review;
- ingestion of data without lawful authority and purpose.

## Required controls

- Recommendation-only agents
- Deny-by-default external actions
- Reversible containment plans
- Human approval for high-impact decisions
- Evidence preservation
- Bounded compute and request sizes
- Complete audit records
- Safe synthetic evaluation before integration
- Independent review for material safety changes

## Severity response

| Level | System response |
| --- | --- |
| Info / low | Monitor and preserve telemetry |
| Medium | Escalate for human investigation |
| High | Recommend reversible containment |
| Critical | Recommend human-controlled emergency stop |

No response level authorises execution in version 0.1.0.

