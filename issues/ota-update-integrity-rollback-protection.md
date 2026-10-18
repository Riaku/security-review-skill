---
categories: [iot-embedded]
domains: [iot-embedded]
---

# OTA Update Channel Integrity & Rollback Protection

**MUST** deliver OTA updates over authenticated channels with version anti-rollback so devices cannot be downgraded to vulnerable firmware.

**Why:** An unsigned or replayable update channel enables MITM firmware replacement; without anti-rollback, attackers force devices back to patched-out vulnerable versions.

**Detect:** check OTA endpoint auth + TLS pinning on device side; verify version monotonicity enforcement (min-version counters, fuse-burn) in bootloader; inspect update manifest signing.

**References:** OWASP IoT Top 10 IOT UPD, NIST IR 8259A, MCUboot anti-rollback docs

---

**Part of:** [iot-embedded](../categories/iot-embedded.md) · [iot-embedded](../domains/iot-embedded.md) · [SKILL.md](../SKILL.md)
