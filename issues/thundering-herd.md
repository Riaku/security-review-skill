# Thundering Herd

**SHOULD** stop many waiters waking at once on one cache expiry via single-flight refresh, stale-while-revalidate, or randomized TTLs.

**Why:** A hot key expiring sends thousands of requests straight to the database.

**Detect:** grep identical `ttl` on hot keys, fixed `expireAt`, missing `singleflight` or `stale-while-revalidate`, notify-all locks.

**References:** Thundering herd problem, Cloudflare stale-while-revalidate, nginx cache lock, CWE-1340, REL11-BP04

---

**Part of:** [resilience](../categories/resilience.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
