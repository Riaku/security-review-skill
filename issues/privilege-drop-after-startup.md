---
categories: [hardening-benchmarks]
domains: [infrastructure]
---

# Privilege Drop After Startup

**MUST** drop elevated privileges immediately after the startup work that required them, before serving any request.

**Why:** A daemon that keeps root after binding its port turns any code-execution bug into host compromise. The window should be milliseconds, not process lifetime.

**Detect:** A process starting as root with no `setuid(`/`setgid(`/`capset`/`PR_CAPBSET_DROP`, or a unit file with no `User=`.

**References:** NCSC ICT security guidelines for web applications, https://www.ncsc.nl/webapplicaties/ict-beveiligingsrichtlijnen-webapplicaties
