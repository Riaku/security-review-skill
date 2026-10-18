# SLOs

**MUST** define measurable service level indicators with explicit error targets, wired to live dashboards.

**Why:** An unmeasured SLO is a guess; teams cannot tell degradation from noise until customers file tickets.

**Detect:** `slo:`/`sli:` in config, burn-rate alerts in Prometheus rules, absence of latency/availability metrics, dashboard-less target docs.

**References:** Google SRE Workbook (SLO chapter), Prometheus recording rules, ISO 20000

---

**Part of:** [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
