# Job Age SLO

**MUST** track age of the oldest pending job as a first-class SLO with alerting, not merely queue count or throughput.

**Why:** A backlog of 100 items averaging 1 second looks healthy while one job waits 45 minutes — count-based metrics hide tail latency entirely.

**Detect:** grep dashboards/alerts for `oldest_job_age`, `job_age_seconds`, `head_of_line_blocking`; absence of max-age alerts alongside queue-depth alerts.

**References:** Google SRE Workbook tail latency, NIST SP 800-53 AU-6, SLI/SLO practice

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [observability](../categories/observability.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
