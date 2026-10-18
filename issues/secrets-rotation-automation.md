# Secrets Rotation Automation (scheduled/triggered rotation without downtime)

**MUST** rotate secrets automatically on schedule and immediately on suspected exposure, without manual steps or downtime.

**Why:** A leaked static secret stays valid forever; automation shrinks the attacker's usable window to the rotation interval.

**Detect:** Grep `rotation_period_days`, Secrets Manager rotation lambdas, Vault `ttl`/`lease`, ExternalSecret `refreshInterval`; IAM policies lacking `MaxAge`/rotation alarms (90 days typical); providers without rotation hooks in CI.

**References:** NIST SP 800-57, NIST SP 800-53 IA-5, CIS Control 6, OWASP ASVS V2.10.4

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
