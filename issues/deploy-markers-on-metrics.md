---
categories: [deployment-release, observability]
domains: [infrastructure, reliability]
---

# Deploy Markers on Metrics

**MUST** annotate dashboards and traces with deploy events (version, timestamp, actor) so regressions and incidents can be correlated to releases.

**Why:** Without deploy markers, every incident starts with "what changed?" guessed from memory; attackers exploiting a fresh vulnerable deploy hide behind that ambiguity.

**Detect:** grep CI/CD for annotations pushed to metrics (`deploy_event`, Grafana annotations API, `release` label on series); check dashboards show deploy lines.

**References:** Google SRE Workbook, DORA deploy frequency practices, Grafana annotations docs

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [observability](../categories/observability.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
