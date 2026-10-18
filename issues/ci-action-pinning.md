# CI Action Pinning (SHA not tag)

**MUST** reference third-party actions by full commit SHA rather than a mutable tag or branch name.

**Why:** A retagged or hijacked tag silently swaps in attacker-controlled code that runs with your workflow's permissions, as the tj-actions incident proved; upstream tag compromises (SolarWinds, event-stream) extend the same lesson to every unpinned build input.

**Detect:** Grep `.github/workflows/*.yml` for `uses:` lines matching `@v[0-9]` or `@main` instead of 40-hex SHAs; check for unpinned `curl | bash` installers in Dockerfiles or CI scripts; verify renovate/dependabot pin settings; actionlint `pin-versions` rule.

**References:** OWASP CI Security CS2, CWE-829, NIST SP 800-218 PO.3, GitHub Actions security hardening guide, OWASP CI/CD Top 10 CICD-SEC-4, NIST SP 800-161
