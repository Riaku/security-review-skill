# Exposed Debug & Actuator Endpoints

**MUST NOT** expose framework debug or management endpoints (Spring Actuator `/env` `/heapdump`, Django `DEBUG=True`, `/phpinfo`, Rails `/debug`, pprof, adminer) on production interfaces.

**Why:** These endpoints dump env vars, heap memory, config, and internals — a single unauthenticated `/env` request can leak every secret in the service.

**Detect:** grep routes/config for `actuator`, `DEBUG`, `phpinfo`, `pprof`, `django-debug`; DAST-scan prod for `/env`, `/heapdump`, `/debug`, `/server-status`.

**References:** OWASP WSTG-CONF-04, CWE-489, CWE-200
