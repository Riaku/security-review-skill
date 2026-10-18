---
categories: [correctness-pitfalls]
domains: [backend]
---

# Daylight Saving Time

**SHOULD NOT** compute elapsed time or cron schedules by naive clock arithmetic across DST transitions.

**Why:** Skipped and repeated local hours make jobs fire twice, never fire, or report impossible durations.

**Detect:** Cron with fixed local hours, `timedelta(hours=1)` loops over calendar days, `TZ=America/` with `naive` datetimes, missing DST tests near March/November.

**References:** CWE-1091, NIST SP 800-53 AU-8, IANA tzdb

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
