---
categories: [deployment-release, web-api-security]
domains: [backend, infrastructure]
---

# Debug/Dev Mode in Production

**MUST NOT** ship production with debug mode, verbose traces, interactive debuggers, or profiling endpoints.

**Why:** Traceback pages leak source and secrets; debug consoles allow code execution.

**Detect:** `DEBUG = True`, `FLASK_DEBUG=1`, `app.run(debug`, exposed `/debug`, Werkzeug console.

**References:** OWASP API8:2023 Security Misconfiguration, OWASP A05:2021, CWE-489, CWE-215
