---
categories: [resilience]
domains: [reliability]
---

# Protective Failure and Recovery

**MUST** verify that failover and restore paths do not reintroduce weaker authentication or resurrect revoked credentials.

**Why:** A standby with weaker auth, or a restore that revives revoked credentials, turns one outage into two incidents.

**Detect:** Walk the failover and restore runbook; name the authentication posture of the standby and which revoked credentials a restore would revive.

**References:** NIST SP 800-160v1r1, https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v1r1.pdf
