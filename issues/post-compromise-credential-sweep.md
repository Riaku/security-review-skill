---
categories: [sre-incidents]
domains: [governance, reliability]
---

# Post-Compromise Credential Sweep

**MUST** after a credential exposure, sweep for attacker-created persistence, including new tokens, keys, users, and CI variables, not only use of the leaked credential.

**Why:** Revoking the exposed secret leaves the attacker's own credentials in place, and the incident reopens from that persistence path.

**Detect:** query audit logs for credential-creation events in the exposure window (CreateAccessKey, CreateToken, AddSSHKey, CI variable writes)

**References:** GitLab incident response runbook, https://docs.gitlab.com/security/responding_to_security_incidents/
