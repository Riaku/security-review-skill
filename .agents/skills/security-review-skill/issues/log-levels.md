---
categories: [observability]
domains: [reliability]
---

# Log Levels

**SHOULD NOT** ship production builds with debug or trace level logging enabled by default.

**Why:** Verbose levels routinely dump tokens, session payloads, and internal state that attackers read straight off log aggregators.

**Detect:** grep config for `LOG_LEVEL=debug`, `level: trace`, `logging.DEBUG`, `debug = true` in prod env files, Helm values, or Dockerfiles.

**References:** OWASP Logging Cheat Sheet, CWE-532, MASVS-STORAGE-3
