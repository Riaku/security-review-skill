---
categories: [observability, security-practices]
domains: [backend, reliability]
---

# Admin Activity Review

**SHOULD** periodically review administrative actions (config changes, permission grants, data exports) against expected operations, on a defined cadence.

**Why:** Insider misuse and compromised admin accounts both hide in plain sight; unreviewed admin logs are a detection gap no amount of collection fixes.

**Detect:** check for scheduled admin-log review (CloudTrail console history, K8s audit webhook, DBA action log) with named reviewer and findings tracked; flag "logs exist but nobody reviews them".

**References:** NIST 800-53 AU-6 review, SOC2 CC7 monitoring, CIS 1.10/8.x log review
