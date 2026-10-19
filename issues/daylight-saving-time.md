---
categories: [correctness-pitfalls, sre-incidents]
domains: [backend, reliability]
---

# Daylight Saving Time

**SHOULD NOT** compute elapsed time or cron schedules by naive clock arithmetic across DST transitions; **SHOULD** test scheduled jobs and time logic across the spring-forward gap and fall-back overlap in the deployment timezone.

**Why:** Skipped and repeated local hours make jobs fire twice, never fire, or report impossible durations — a bug that hides for months and surfaces exactly at the transition.

**Detect:** Cron with fixed local hours, `timedelta(hours=1)` loops over calendar days, `TZ=America/` with `naive` datetimes, no test freezing the clock at a DST boundary (spring-forward gap, fall-back overlap) in the deployment timezone, scheduler docs silent on which timezone governs.

**References:** NIST SP 800-53 AU-8, IANA tzdb, crontab(5) NOTES on DST
