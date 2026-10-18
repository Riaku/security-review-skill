# Device Provisioning Identity

**SHOULD** provision each device with a unique, hardware-bound identity (per-device cert/keys, TPM/secure element) — never shared fleet credentials.

**Why:** One leaked shared device key or cert compromises every unit in the field; unique identities enable individual revocation and per-device attribution.

**Detect:** grep firmware/config for shared API keys, shared client certs, hardcoded device secrets; check for per-device cert enrollment flow (ACME/EST/custom) and a revocation path.

**References:** OWASP IoT Top 10 IOT DB1/credentials, FIDO/TPM device attestation, NIST IoT device identity guidance

---

**Part of:** [iot-embedded](../categories/iot-embedded.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [iot-embedded](../domains/iot-embedded.md) · [SKILL.md](../SKILL.md)
