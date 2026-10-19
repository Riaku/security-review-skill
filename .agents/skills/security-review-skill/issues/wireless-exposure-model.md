---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Wireless Exposure Model

**MUST** treat every wireless channel as reachable by a remote attacker, and justify each one against the exposure it adds.

**Why:** Radio removes the physical-presence assumption the rest of the threat model was built on, so a device in a locked room is suddenly internet-adjacent.

**Detect:** grep the interface inventory for `ble`, `zigbee`, `lora`, `wifi`, `cellular`, and confirm each appears in the threat model with a remote attacker.

**References:** NCSC Operational Technology collection, https://www.ncsc.gov.uk/collection/operational-technology
