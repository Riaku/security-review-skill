---
categories: [cicd-pipeline-security, hardening-benchmarks, security-practices]
domains: [backend, government-compliance, infrastructure]
---

# Patch management SLAs (MTTR targets by severity, exception tracking)

**MUST** define mean-time-to-remediate targets per severity (critical 24h, high 30d, medium 90d) covering both application dependencies and the base images of shipped artifacts, rebuilding and redeploying those images on a fixed cadence (weekly minimum) so long-lived images do not accumulate known-exploitable CVEs, and log every exception with owner and expiry date.

**Why:** Undated exceptions silently become permanent debt; SLA clocks make drift visible and auditable.

**Detect:** `sla` / `mttr` keys in policy docs, `waiver` / `exception` tracker files with `expires` fields; `.trivyignore` age, `imagePullPolicy: Always`, Renovate/Dependabot config, `fixVersions` in scanner reports

**References:** NIST SP 800-40 Rev. 4, CIS Control 7, PCI DSS 6.3.3, CWE-1104, CISA KEV, OWASP A06:2021
