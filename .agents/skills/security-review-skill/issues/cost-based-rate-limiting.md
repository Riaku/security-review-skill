---
categories: [resilience]
domains: [reliability]
---

# Cost-Based Rate Limiting

**SHOULD** limit consumption by the cost of the work requested, such as rows, bytes, tokens, or execution time, not by request count alone.

**Why:** One expensive query and one cheap one count equally under a per-request limit, so an attacker spends your capacity with very few requests.

**Detect:** grep rate limiter configuration for keys on request count only; check whether row, byte, or cost limits are enforced separately

**References:** Site Reliability Engineering (O'Reilly, 2016), handling overload
