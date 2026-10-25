---
categories: [correctness-pitfalls, sre-incidents]
domains: [backend, reliability]
---

# Monotonic Clocks for Durations & Timeouts

**MUST** measure elapsed time and enforce in-process timeouts with a monotonic clock, never by subtracting wall-clock timestamps that a clock adjustment can move backwards.

**Why:** An NTP correction, an operator setting the date, or a VM resume can step the wall clock backwards in the middle of an interval, so the computed duration goes negative and the timeout either fires instantly or never fires at all — a failure mode that appears only in production and never in a test with a stable clock.

**Detect:** `time.time()`, `System.currentTimeMillis()`, `Date.now()`, `datetime.now()` used on both sides of a subtraction or to expire an in-process key; timer and rate-limiter helpers built on the wall clock; wall-clock `Instant` differences where a monotonic duration is needed. Prefer `time.monotonic()`, `clock_gettime(CLOCK_MONOTONIC)`, `System.nanoTime()`, `performance.now()`.

**References:** POSIX clock_gettime(2) CLOCK_MONOTONIC, https://man7.org/linux/man-pages/man2/clock_gettime.2.html, Go time package monotonic clock readings, https://pkg.go.dev/time#hdr-Monotonic_Clocks, Python time.monotonic, https://docs.python.org/3/library/time.html#time.monotonic
