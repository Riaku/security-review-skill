---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Bounded Wireless Discovery Window

**MUST** bound the discoverability window of every wireless interface — inquiry, advertising, broadcast — and stop it when the discovery or pairing task completes.

**Why:** Open-ended discoverability gives any nearby device a standing window to enumerate, probe, and attack the device.

**Detect:** grep for startDiscovery / startAdvertising calls that have no matching stop call or timeout

**References:** Google android-security-lints, https://github.com/google/android-security-lints
