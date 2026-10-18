# Shift-Left Security (security earliest in the lifecycle)

**MUST** run SAST, dependency, and secret scanning in CI on every pull request, failing the build on high-severity findings rather than deferring them to pre-release.

**Why:** Defects caught in production cost orders of magnitude more than at commit time; late gates train teams to bypass them.

**Detect:** `.github/workflows` with `sast`/`semgrep`/`gitleaks` steps, `fail-on: high` in scanner config, pre-commit hooks

**References:** OWASP SAMM Security Testing, MS SDL, OWASP DevSecOps Maturity Model
