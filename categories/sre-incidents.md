# sre-incidents

Operational readiness: DR, incidents, SLOs, on-call.

## What this category covers

This category covers the operational contract around a service: the targets it promises, the process that responds when it misses them, and the recovery paths that exist before an emergency. Member items span SLOs, SLAs, error budgets, on-call and severity levels, incident response and post-incident review, runbooks and break-glass access, and the status-page communication path. They also cover recovery engineering — RTO and RPO, backups and restore drills, failover, availability zones and multi-region, graceful shutdown and connection draining — and the resilience obligations of regulated sectors. A reviewer should expect findings about a plan that exists only on paper, a target no one measures, or a recovery step that fails the first time it is exercised.

- Targets and budgets: SLOs, SLAs, error budgets, and RTO/RPO.
- Response process: severity levels, incident command, escalation, and outage comms.
- Preparedness: runbooks, break-glass access, and rehearsed drills.
- Recovery engineering: backups, restore verification, failover, and zone or region spread.
- Availability mechanics: health checks, graceful shutdown, connection draining, and statelessness.
- Learning and assurance: blameless post-incident review with tracked actions, chaos exercises, and sector obligations.

## What it does not cover

- [observability](../categories/observability.md) — instrumenting, logging, and alert routing belong there.
- [resilience](../categories/resilience.md) — in-code timeout, retry, and circuit-breaker patterns belong there.
- [deployment-release](../categories/deployment-release.md) — rollout and rollback mechanics belong there.

## What a finding here looks like

- An SLO is stated but has no measured indicator, dashboard, or error budget behind it.
- A backup job runs on schedule but no restore has ever been tested, and the first drill finds it unusable.
- Replicas sit in one availability zone, so a single zone failure removes all capacity.
- An incident has no named commander or severity level, and responders duplicate work while impact grows.
- A paged alert has no runbook a non-author can execute, or emergency access is either absent or standing.
