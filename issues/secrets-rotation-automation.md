# Secrets Rotation Automation (scheduled/triggered rotation without downtime)

**MUST** rotate secrets automatically on schedule and immediately on suspected exposure, without manual steps or downtime.

**Why:** A leaked static secret stays valid forever; automation shrinks the attacker's usable window to the rotation interval.

**Detect:** grep `rotation_period_days`, Secrets Manager rotation lambdas, Vault `ttl`/`lease` config, ExternalSecret `refreshInterval`, `rotate_credentials` jobs.

**References:** NIST SP 800-57 (key management), NIST SP 800-53 IA-5, CIS Control 6, AWS Secrets Manager rotation practices
