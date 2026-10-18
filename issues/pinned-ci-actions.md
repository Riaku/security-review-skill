# Pinned CI Actions & Third-Party Pinned Dependencies (SHA-pinned, not floating tags)

**MUST** reference third-party CI actions by immutable commit SHA, never mutable tags like `@v1`.

**Why:** A floating tag can be retagged overnight to attacker code running with your CI's tokens — the tj-actions incident proved it.

**Detect:** grep workflow YAML for `uses: owner/repo@v` vs `@<40-hex-sha>`; renovate `pin` configs, dependabot pin settings.

**References:** OWASP CI/CD Top 10 CICD-SEC-4, GitHub Actions hardening, SLSA provenance, CWE-829
