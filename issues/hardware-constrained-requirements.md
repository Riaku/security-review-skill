---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Hardware-Constrained Requirements

**MUST** validate security requirements against the target device's CPU, memory, power and radio limits before design freeze.

**Why:** A requirement the hardware cannot sustain gets silently dropped during implementation, usually the one protecting the update channel or key store. Constraints found late force insecure compromises.

**Detect:** Inspect the requirements doc for a hardware budget per requirement (crypto, TLS, logging, update verification).

**References:** ENISA Good Practices for IoT Security, https://www.enisa.europa.eu/publications/good-practices-for-security-of-iot-1
