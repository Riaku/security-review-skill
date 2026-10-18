# Credential Access Detection (keylogging, token theft, credential dumping patterns)

**SHOULD** detect credential harvesting: LSASS dumps, keylogging hooks, OAuth token replay, metadata-service credential scraping.

**Why:** Stolen credentials are the leading initial-access vector; catching the theft step stops breaches identity controls alone miss.

**Detect:** grep detection content for `T1003`, `lsass`, `mimikatz`, `secretsdump`, alerts on `169.254.169.254` access, token-replay rules.

**References:** MITRE ATT&CK TA0006/T1003, NIST SP 800-63B, CWE-522, GuardDuty credential-access detections

---

**Part of:** [authentication](../categories/authentication.md) · [observability](../categories/observability.md) · [backend](../domains/backend.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
