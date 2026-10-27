---
categories: [api-design]
domains: [backend]
---

# Request Size Limits

**MUST** enforce a maximum request body size at the edge before parsing, rejecting oversized payloads with 413.

**Why:** Unbounded bodies let an attacker exhaust memory or CPU with one giant upload, bypassing per-request rate limits entirely.

**Detect:** `client_max_body_size 0`, absent `maxBodySize`/`limit` in Express/Flask/Spring config, no 413 handling.

**References:** OWASP API4:2023 Unrestricted Resource Consumption, CWE-400, OWASP ASVS V5.2, nginx client_max_body_size directive
