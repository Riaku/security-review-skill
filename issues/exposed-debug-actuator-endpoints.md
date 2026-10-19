---
categories: [web-api-security]
domains: [backend]
---

# Exposed Debug & Actuator Endpoints

**MUST** disable unused framework debug and management endpoints and restrict the rest to authenticated management access (`management.endpoints.web.exposure.include`, `management.server.port`); `/env`, `/heapdump`, `/phpinfo`, and `pprof` handlers are never reachable unauthenticated.

**Why:** These endpoints dump env vars, heap memory, config, and internals — a single unauthenticated `/env` request can leak every secret in the service.

**Detect:** grep routes/config for `actuator`, `DEBUG`, `phpinfo`, `pprof`, `django-debug`; DAST-scan prod for `/env`, `/heapdump`, `/debug`, `/server-status`.

**References:** OWASP WSTG-CONF-04, CWE-489, CWE-200
