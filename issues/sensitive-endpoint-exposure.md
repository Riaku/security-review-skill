---
categories: [hardening-benchmarks, web-api-security]
domains: [backend, government-compliance]
---

# Sensitive endpoint exposure (actuator, /admin, .git, .env, debug routes, dashboards)

**MUST NOT** Expose admin panels, actuator endpoints, `.git`/`.env` files, debug routes, or dashboards publicly; gate them behind auth, and **MUST** disable unused framework debug and management endpoints while restricting the rest to authenticated management access (`management.endpoints.web.exposure.include`, `management.server.port`), so `/env`, `/heapdump`, `/phpinfo`, `pprof`, and `/server-status` are never reachable unauthenticated.

**Why:** Leaked `.env` and `.git` hand attackers credentials and full source directly, and debug or management endpoints dump environment variables, heap memory, and internal configuration — a single unauthenticated `/env` request can leak every secret in the service.

**Detect:** Reachable `/actuator`, `/admin`, `/.git/HEAD`, `/.env`, `/server-status`, `/metrics` without auth; grep routes and config for `actuator`, `DEBUG`, `phpinfo`, `pprof`, `django-debug`, and DAST-scan production for `/env`, `/heapdump`, `/debug`.

**References:** OWASP A05:2021, CWE-538, CWE-200, CWE-489, OWASP WSTG-CONF-04, OWASP WSTG-CONF-05
