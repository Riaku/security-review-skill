# Patch cadence and remediation SLAs for known CVEs in production images

**MUST** rebuild and redeploy base images on a fixed cadence (weekly minimum), remediating critical CVEs within 24 hours of disclosure.

**Why:** Long-lived images accumulate known-exploitable CVEs that scanners flag forever and worms exploit within days.

**Detect:** `.trivyignore` age, `imagePullPolicy: Always`, Renovate/Dependabot config, `fixVersions` in scanner reports

**References:** CWE-1104, CISA KEV, NIST SP 800-40, OWASP A06:2021
