---
categories: [sre-incidents]
domains: [reliability]
---

# On-Call

**SHOULD** rotate on-call across a staffed team with bounded hours and backup responders, not one heroic engineer.

**Why:** Solo on-call burns out or sleeps through pages; one responder is itself a single point of failure for coverage.

**Detect:** PagerDuty/Opsgenie rotation config, single `oncall:` contact in runbooks, no escalation chain.

**References:** Google SRE Book (on-call), OSHA fatigue guidance, NIST SP 800-61
