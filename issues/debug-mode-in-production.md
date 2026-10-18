---
categories: [deployment-release, web-api-security]
domains: [backend, infrastructure]
---

# Debug/Dev Mode in Production

**MUST NOT** Ship production with debug mode, verbose traces, interactive debuggers, or profiling endpoints.

**Why:** Traceback pages leak source and secrets; debug consoles allow code execution.

**Detect:** `DEBUG = True`, `FLASK_DEBUG=1`, `app.run(debug`, exposed `/debug`, Werkzeug console.

**References:** OWASP A05:2021, CWE-489, CWE-215

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
