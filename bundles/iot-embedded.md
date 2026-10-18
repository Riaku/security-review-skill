# iot-embedded — full checklist (3 items)

Firmware, OTA, and device-identity security.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Firmware Signing & Secure Boot

**MUST** sign firmware images and enforce signature verification at boot (secure boot chain) so unsigned or tampered images cannot run on devices.

**Why:** Unsigned firmware is the ultimate persistence layer — an attacker who flashes once owns the device permanently and it survives every software remediation.

**Detect:** grep build pipeline for signing steps (`osslsigncode`, `imgtool`, HSM calls); check bootloader verify-enforce (not just verify-log) mode; look for dev/test keys shipped in production images.

**References:** NIST SP 800-193 platform firmware resiliency, OWASP IoT Top 10 (IOT ASSET), Arm TrustZone/UEFI Secure Boot docs

# OTA Update Channel Integrity & Rollback Protection

**MUST** deliver OTA updates over authenticated channels with version anti-rollback so devices cannot be downgraded to vulnerable firmware.

**Why:** An unsigned or replayable update channel enables MITM firmware replacement; without anti-rollback, attackers force devices back to patched-out vulnerable versions.

**Detect:** check OTA endpoint auth + TLS pinning on device side; verify version monotonicity enforcement (min-version counters, fuse-burn) in bootloader; inspect update manifest signing.

**References:** OWASP IoT Top 10 IOT UPD, NIST IR 8259A, MCUboot anti-rollback docs

# Device Provisioning Identity

**SHOULD** provision each device with a unique, hardware-bound identity (per-device cert/keys, TPM/secure element) — never shared fleet credentials.

**Why:** One leaked shared device key or cert compromises every unit in the field; unique identities enable individual revocation and per-device attribution.

**Detect:** grep firmware/config for shared API keys, shared client certs, hardcoded device secrets; check for per-device cert enrollment flow (ACME/EST/custom) and a revocation path.

**References:** OWASP IoT Top 10 IOT DB1/credentials, FIDO/TPM device attestation, NIST IoT device identity guidance

