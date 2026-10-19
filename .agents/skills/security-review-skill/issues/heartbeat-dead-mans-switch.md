---
categories: [observability]
domains: [reliability]
---

# Dead-man's-switch Heartbeat for Scheduled Jobs

**SHOULD** give every scheduled job a heartbeat that pages when the expected ping is missing, rather than alerting only on failure.

**Why:** A cron that never runs — disabled, deadlocked, or silently deleted — produces no error at all; only absence-of-beat reveals it.

**Detect:** grep schedulers for healthcheck pings (`healthchecks.io`, `deadman` checks, `K8s CronJob` success conditions); flag jobs with failure alerts but no liveness deadline.

**References:** Healthchecks.io dead-man pattern, Google SRE Workbook, CWE-778, K8s CronJob docs
