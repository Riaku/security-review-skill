---
categories: [observability]
domains: [infrastructure]
---

# Log Destination Inventory

**MUST** keep a log inventory of what each layer logs, its destination, retention, and access, and emit only to documented destinations.

**Why:** An undocumented sink moves sensitive data outside the retention and access regime, and no later investigation can say where it went.

**Detect:** grep logger configuration (`handlers`, `appenders`, `syslog:`, `outputs`) and compare every destination against the inventory document.

**References:** OWASP ASVS v5.0 V16.2.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md
