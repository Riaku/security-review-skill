---
categories: [authentication, observability]
domains: [backend, reliability]
---

# Anomalous Authentication Detection (impossible travel, rare UA/IP)

**SHOULD** monitor for impossible-travel, rare user-agent, and unfamiliar-IP login patterns and trigger step-up MFA or alerting on anomalies.

**Why:** Without anomaly detection, an attacker logging in from a foreign IP with a stolen credential looks identical to the legitimate user and passes silently.

**Detect:** grep auth pipeline for absent `impossible_travel`, `geoip`, `ua_fingerprint` checks; no step-up MFA on new-device login; no alerting on geo-velocity anomalies.

**References:** NIST SP 800-63B §7.2, OWASP A07:2021, CIS Control 8.3, MITRE ATT&CK T1078

---

**Part of:** [authentication](../categories/authentication.md) · [observability](../categories/observability.md) · [backend](../domains/backend.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
