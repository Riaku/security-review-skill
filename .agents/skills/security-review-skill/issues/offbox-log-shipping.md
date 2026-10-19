---
categories: [observability]
domains: [infrastructure]
---

# Off-Box Log Shipping

**MUST** ship logs to a logically separate system in near real time so a compromised host cannot erase the record of its own activity.

**Why:** Local logs are the first artifact an intruder edits, and forensic value depends on the record already existing outside the blast radius.

**Detect:** grep for local-only logging (`FileHandler`, a `/var/log` volume, no forwarder sidecar) on services that emit security events.

**References:** OWASP ASVS v5.0 V16.4.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md, NIST SP 800-92
