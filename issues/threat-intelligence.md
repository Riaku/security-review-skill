# Threat Intelligence Integration

**MUST** ingest threat feeds, IOCs, and vendor advisories into ops tooling with automated matching against the estate.

**Why:** Unconsumed intelligence is unread email; a known exploited CVE sits unnoticed until it hits your stack.

**Detect:** IOC feeds in SIEM config, `threat_intel` integrations, no advisory-to-asset matching in the scanner.

**References:** NIST SP 800-150, MITRE ATT&CK, MISP threat sharing, CISA KEV catalog

---

**Part of:** [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
