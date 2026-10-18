# Push Protection (block secrets at commit/push time)

**MUST** scan every commit and push for credentials and reject those containing live secrets before they enter history.

**Why:** A secret once committed stays in git history forever; rotation is the only true fix and is often missed.

**Detect:** Missing pre-commit/gitleaks/trufflehog hooks; no GitHub push protection or secret-scanning alerts enabled; `.git/hooks/pre-commit` absent from repo tooling.

**References:** CWE-798, NIST SP 800-218 PS.1, GitHub push protection docs, gitleaks / trufflehog / detect-secrets
