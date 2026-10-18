# Capacity Planning

**MUST** forecast capacity against projected peak (not average) load with explicit headroom, reviewed on a recurring cadence tied to growth data.

**Why:** Planning to average utilization guarantees saturation at the first promotional spike or seasonal peak, turning a predictable event into an outage.

**Detect:** grep runbooks/planning docs for `headroom`, `peak_utilization`, `capacity_forecast`, growth-rate assumptions; check dashboards for peak-vs-average reporting and review-date stamps.

**References:** Google SRE Book capacity planning, NIST SP 800-184, ITIL Capacity Management

---

**Part of:** [scaling-capacity](../categories/scaling-capacity.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
