---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Protocol Security Requirements Match

**MUST** select each communication protocol by documented match between its security features and the stated requirements.

**Why:** Protocols get chosen for tooling convenience, then retrofitted with application-layer encryption that misses peer authentication. A recorded mapping exposes the gap before it ships.

**Detect:** Inspect the requirements traceability matrix for a protocol row per interface, listing the security features it does and does not provide.

**References:** ENISA Good Practices for IoT Security, https://www.enisa.europa.eu/publications/good-practices-for-security-of-iot-1
