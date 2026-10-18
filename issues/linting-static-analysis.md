---
categories: [cicd-pipeline-security, testing-strategy]
domains: [backend, infrastructure]
---

# Linting & Static Analysis Enforced in CI (linter, type checker, SAST)

**MUST** fail the pipeline when linters, type checkers, or SAST scans report findings, not merely log them as warnings.

**Why:** Advisory-only scans are ignored at scale; vulnerable code merges unchecked because nothing blocks it, and defects caught in production cost orders of magnitude more than at commit time.

**Detect:** Workflow steps without `--exit-code`/`fail-on-error`; `continue-on-error: true` on scan jobs; SAST action with `level: warning`; missing ruff/mypy/semgrep/codeql steps entirely; pre-commit hooks running the same checks earliest in the lifecycle.

**References:** OWASP CI/CD Top 10 CICD-SEC-10, CWE-1156, NIST SP 800-218 (SSDF), GitHub Code Scanning (CodeQL) docs, OWASP SAMM Security Testing, OWASP DevSecOps Maturity Model

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
