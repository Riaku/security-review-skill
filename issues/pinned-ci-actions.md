# Pinned CI Actions & Third-Party Pinned Dependencies (SHA-pinned, not floating tags)

**MUST** reference third-party CI actions and build dependencies by immutable commit SHA rather than mutable tags like `@v1`.

**Why:** Floating tags can be retagged overnight to attacker code that runs with your CI's tokens and secrets — the Codecov and tj-actions incidents proved it.

**Detect:** grep workflow YAML for `uses: owner/repo@v` (tag refs) vs `uses: owner/repo@<40-hex-sha>`; `renovate.json` pin configs, `dependabot` pin settings.

**References:** OWASP CI/CD Security Top 10 CICD-SEC-4, GitHub Actions security hardening, SLSA dependency provenance, CWE-829
