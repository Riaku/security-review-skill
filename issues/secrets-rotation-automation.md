# Secrets Rotation Automation (scheduled/triggered rotation without downtime)

**MUST** rotate secrets automatically on a schedule and immediately upon suspected exposure, without manual intervention or service downtime.

**Why:** A leaked static secret stays valid forever; automation shrinks the attacker's window from "indefinitely" to the rotation interval.

**Detect:** grep for `rotation_period_days`, AWS Secrets Manager rotation lambdas, Vault `lease`/`ttl` settings, `rotate_credentials` jobs, ExternalSecret `refreshInterval`.

**References:** NIST SP 800-57 (key management), NIST SP 800-53 IA-5, CIS Control 6, AWS Secrets Manager rotation best practices
