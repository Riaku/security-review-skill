---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Fleet Key Rotation

**MUST** rotate device keys through a central, scheduled rekey path rather than per-device manual steps.

**Why:** When rekeying needs an operator at each device, fleets converge on one shared key nobody rotates, so a single device compromise becomes a fleet compromise.

**Detect:** judgment — inspect provisioning and rekey runbooks for a central key-distribution path versus per-device manual steps, and look for a shared key literal in provisioning config.

**References:** NCSC Operational Technology: RF and key management principles, https://www.ncsc.gov.uk/collection/operational-technology
