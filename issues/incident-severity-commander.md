# Incident Severity Levels with a Designated Incident Commander

**MUST** assign a named incident commander per severity level at declaration, with coordination authority.

**Why:** Without a single decision-maker, engineers duplicate work and argue rollback timing while the outage widens.

**Detect:** severity matrix (`SEV1`–`SEV4`) in IR docs, `incident_commander` field in tickets, no commander in paging config.

**References:** NIST SP 800-61, Google SRE Workbook (incident command), ITIL incident management

---

**Part of:** [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
