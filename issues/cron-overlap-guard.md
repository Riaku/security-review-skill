---
categories: [database, messaging-async]
domains: [data]
---

# Overlapping cron executions guarded by single-runner locks

**MUST** guard scheduled jobs with a single-runner lock (advisory lock, flock, or leader election) so a slow run cannot overlap the next scheduled tick.

**Why:** If a nightly job outlives its interval, two copies run at once: duplicate charges, double-sent emails, deadlocked locks, corrupted aggregates. The failure is intermittent — it appears only when data grows past the schedule window.

**Detect:** Inspect crontabs and systemd timers for jobs with no lock acquisition. Grep for `pg_try_advisory_lock`, `flock`, or distributed locks; check Kubernetes CronJobs for `concurrencyPolicy: Forbid`.

**Bad:**
```bash
# if the 02:00 run spills past 03:00, two run at once
0 2 * * * /app/report.sh
```

**Good:**
```bash
0 2 * * * flock -n /run/report.lock /app/report.sh || \
  logger "report skipped: already running"
```

**References:** Kubernetes CronJob concurrencyPolicy docs, PostgreSQL advisory locks, CWE-662 Improper Synchronization

---

**Part of:** [database](../categories/database.md) · [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
