---
categories: [security-practices]
domains: [governance, infrastructure]
---

# Compensating Controls for Unpatchable Systems

**MUST** maintain pre-engineered compensating controls — network isolation, feature disablement, hardened access — for components that cannot be patched on the vendor's schedule.

**Why:** Most known-exploited vulnerabilities affect systems that cannot be patched in place, and few vendors ship workarounds, so the mitigation has to exist before the incident.

**Detect:** judgment: the compensating-control runbook entry for each unpatchable component

**References:** I Can't Patch My OT Systems!, https://arxiv.org/abs/2510.06951, CISA KEV catalog, https://www.cisa.gov/known-exploited-vulnerabilities-catalog
