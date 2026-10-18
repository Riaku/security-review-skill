# Sensitive endpoint exposure (actuator, /admin, .git, .env, debug routes, dashboards)

**MUST NOT** Expose admin panels, actuator endpoints, `.git`/`.env` files, or dashboards publicly; gate them behind auth.

**Why:** Leaked `.env` and `.git` hand attackers credentials and full source directly.

**Detect:** Reachable `/actuator`, `/admin`, `/.git/HEAD`, `/.env`, `/server-status`, `/metrics` without auth.

**References:** OWASP A05:2021, CWE-538, CWE-200, OWASP Testing Guide §12.2
