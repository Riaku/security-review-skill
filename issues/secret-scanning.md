# Secret Scanning

**MUST** run automated secret scanning (gitleaks, trufflehog, GitHub push protection) on every commit and full-history scans before publishing any repository.

**Why:** Developers routinely commit live credentials under deadline pressure; without scanning, leaks ship silently to public or shared remotes.

**Detect:** `.gitleaks.toml`, `.pre-commit-config.yaml` with gitleaks/trufflehog hooks, absent GitHub `secret_scanning` settings in org config.

**References:** OWASP ASVS V2.10.2, CWE-540, CWE-319
