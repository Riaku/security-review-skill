# Sensitive endpoint exposure (actuator, /admin, .git, .env, debug routes, dashboards)

**MUST NOT** Expose admin panels, actuator endpoints, `.git`/`.env` files, or dashboards publicly; gate them behind auth.

**Why:** Leaked `.env` and `.git` hand attackers credentials and full source directly.

**Detect:** Reachable `/actuator`, `/admin`, `/.git/HEAD`, `/.env`, `/server-status`, `/metrics` without auth.

**References:** OWASP A05:2021, CWE-538, CWE-200, OWASP Testing Guide §12.2

---

**Part of:** [hardening-benchmarks](../categories/hardening-benchmarks.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
