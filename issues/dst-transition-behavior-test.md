---
categories: [correctness-pitfalls, sre-incidents]
domains: [backend, reliability]
---

# DST-Transition Behavior Test

**SHOULD** test scheduled jobs and time logic across DST transitions (spring-forward gap, fall-back overlap) in the deployment timezone.

**Why:** Cron jobs silently skip or double-fire at DST boundaries; "runs every 2h" becomes 23 or 25 runs twice a year — a bug that hides for months and hits exactly when you're asleep.

**Detect:** check for tests that freeze time at DST boundaries (e.g. 2026-03-08 02:30 US), cron schedules using UTC vs local TZ, and scheduler docs stating which timezone governs; flag local-TZ cron for critical jobs.

**References:** cron DST pitfalls (crontab(5) NOTES), NTP/timezone best practices, ICU timezone docs

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [sre-incidents](../categories/sre-incidents.md) · [backend](../domains/backend.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
