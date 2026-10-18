# CI Action Pinning (SHA not tag)

**MUST** reference third-party actions by full commit SHA rather than a mutable tag or branch name.

**Why:** A retagged or hijacked tag silently swaps in attacker-controlled code that runs with your workflow's permissions.

**Detect:** Grep `.github/workflows/*.yml` for `uses:` lines matching `@v[0-9]` or `@main` instead of 40-hex SHAs; actionlint `pin-versions` rule.

**References:** OWASP CI Security CS2, CWE-829, NIST SP 800-218 PO.3, GitHub Actions security hardening guide
