---
categories: [cicd-pipeline-security, supply-chain]
domains: [infrastructure]
---

# CI Action Pinning (SHA not tag)

**MUST** reference third-party actions by full commit SHA rather than a mutable tag or branch name.

**Why:** A retagged or hijacked tag silently swaps in attacker-controlled code that runs with your workflow's permissions, as the tj-actions incident proved; the same trust-in-mutable-references lesson applies to every unpinned build input — compromised build systems and hijacked packages (SolarWinds, event-stream) show what runs with your pipeline's privileges when an upstream reference is subverted.

**Detect:** Grep `.github/workflows/*.yml` for `uses:` lines matching `@v[0-9]` or `@main` instead of 40-hex SHAs; check for unpinned `curl | bash` installers in Dockerfiles or CI scripts; verify renovate/dependabot pin settings; actionlint `pin-versions` rule.

**References:** OWASP A08:2021 Software and Data Integrity Failures, CWE-829, NIST SP 800-218 (SSDF), GitHub Actions security hardening guide, OWASP Top 10 CI/CD Security Risks CICD-SEC-3 (Dependency Chain Abuse), NIST SP 800-161
