# iot-embedded — full checklist (13 items)

Firmware, OTA, and device-identity security.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/iot-embedded.md](../categories/iot-embedded.md) · Index: [SKILL.md](../SKILL.md)

# Attestation Scope Declaration

**MUST** state the root-of-trust class and attested state scope — boot, runtime, update, erasure — whenever an attestation result is used as an authorization input.

**Why:** 'The device is attested' answers different questions depending on whether the root is hardware or software and which state was measured.

**Detect:** judgment: the attestation policy — which claims are consumed and what each claim actually proves

**References:** Remote attestation literature review, https://arxiv.org/abs/2105.02466

# Auxiliary Subsystem Attack Surface

**MUST** include secondary control subsystems such as battery, radio, and actuator controllers in the device threat model as reachable and often unauthenticated.

**Why:** Physical-effect subsystems get safety review but rarely adversarial review, so an unauthenticated battery or motor controller becomes remote code execution.

**Detect:** compare the interface inventory (buses, radios, companion-app channels) against the threat model's asset list.

**References:** E-Trojans: e-scooter security assessment (arXiv 2411.17184), https://arxiv.org/abs/2411.17184

# Device Provisioning Identity

**SHOULD** provision each device with a unique, hardware-bound identity (per-device cert/keys, TPM/secure element) — never shared fleet credentials.

**Why:** One leaked shared device key or cert compromises every unit in the field; unique identities enable individual revocation and per-device attribution.

**Detect:** grep firmware/config for shared API keys, shared client certs, hardcoded device secrets; check for per-device cert enrollment flow (ACME/EST/custom) and a revocation path.

**References:** OWASP IoT Top 10 I1 (Weak, Guessable, or Hardcoded Passwords), FIDO/TPM device attestation, NIST IoT device identity guidance

# Firmware Signing & Secure Boot

**MUST** sign firmware images and enforce signature verification at boot (secure boot chain) so unsigned or tampered images cannot run on devices.

**Why:** Unsigned firmware is the ultimate persistence layer — an attacker who flashes once owns the device permanently and it survives every software remediation.

**Detect:** grep build pipeline for signing steps (`sbsign`, `imgtool` (MCUboot), `openssl dgst -sign`, HSM calls); check bootloader verify-enforce (not just verify-log) mode; look for dev/test keys shipped in production images.

**References:** NIST SP 800-193 platform firmware resiliency, OWASP IoT Top 10 I4, Arm TrustZone/UEFI Secure Boot docs

# Fleet Key Rotation

**MUST** rotate device keys through a central, scheduled rekey path rather than per-device manual steps.

**Why:** When rekeying needs an operator at each device, fleets converge on one shared key nobody rotates, so a single device compromise becomes a fleet compromise.

**Detect:** judgment — inspect provisioning and rekey runbooks for a central key-distribution path versus per-device manual steps, and look for a shared key literal in provisioning config.

**References:** NCSC Operational Technology: RF and key management principles, https://www.ncsc.gov.uk/collection/operational-technology

# Bounded Contributor Influence

**SHOULD** weight and cap each contributor's influence on an aggregated dataset so a small number of spoofed inputs cannot move the aggregate.

**Why:** Fusion amplifies: a handful of fabricated reports can register a system-wide condition, and every downstream decision inherits the fabrication.

**Detect:** judgment: the aggregation rule — per-source weight caps and outlier damping

**References:** Anderson, Security Engineering 3rd ed., ch.25, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch25.pdf

# Hardware-Constrained Requirements

**MUST** validate security requirements against the target device's CPU, memory, power and radio limits before design freeze.

**Why:** A requirement the hardware cannot sustain gets silently dropped during implementation, usually the one protecting the update channel or key store. Constraints found late force insecure compromises.

**Detect:** Inspect the requirements doc for a hardware budget per requirement (crypto, TLS, logging, update verification).

**References:** ENISA Good Practices for IoT Security, https://www.enisa.europa.eu/publications/good-practices-for-security-of-iot-1

# Hardware Security Capability Audit

**MUST** verify which hardware protections a device actually provides and enables, rather than trusting the platform's security claims.

**Why:** The gap between silicon capability and what firmware enables is where most embedded exposure lives, and marketing material never documents it.

**Detect:** grep the startup and linker code for the protections being turned on (`MPU->CTRL`, `SAU->CTRL`, `TZEN`, `SCB->CCR`) and compare with the SoC's documented features.

**References:** SoK: Arm Cortex-M security (arXiv 2401.15289), https://arxiv.org/abs/2401.15289

# OTA Update Channel Integrity & Rollback Protection

**MUST** deliver OTA updates over authenticated channels with version anti-rollback so devices cannot be downgraded to vulnerable firmware.

**Why:** An unsigned or replayable update channel enables MITM firmware replacement; without anti-rollback, attackers force devices back to patched-out vulnerable versions.

**Detect:** check OTA endpoint auth + TLS pinning on device side; verify version monotonicity enforcement (min-version counters, fuse-burn) in bootloader; inspect update manifest signing.

**References:** OWASP IoT Top 10 I4 (Lack of Secure Update Mechanism), NIST IR 8259A, MCUboot anti-rollback docs

# Protocol Security Requirements Match

**MUST** select each communication protocol by documented match between its security features and the stated requirements.

**Why:** Protocols get chosen for tooling convenience, then retrofitted with application-layer encryption that misses peer authentication. A recorded mapping exposes the gap before it ships.

**Detect:** Inspect the requirements traceability matrix for a protocol row per interface, listing the security features it does and does not provide.

**References:** ENISA Good Practices for IoT Security, https://www.enisa.europa.eu/publications/good-practices-for-security-of-iot-1

# Shared Bus Node Trust

**MUST** rate-limit and authenticate each node's contribution to a shared bus or channel, so one subverted node cannot consume the medium for all.

**Why:** A bus that trusts every node lets one reprogrammed device transmit continuously and make the whole channel, and everything depending on it, unusable.

**Detect:** judgment: the bus protocol — per-node transmit quotas, bus-off handling, and message authentication

**References:** Anderson, Security Engineering 3rd ed., ch.25, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch25.pdf

# Bounded Wireless Discovery Window

**MUST** bound the discoverability window of every wireless interface — inquiry, advertising, broadcast — and stop it when the discovery or pairing task completes.

**Why:** Open-ended discoverability gives any nearby device a standing window to enumerate, probe, and attack the device.

**Detect:** grep for startDiscovery / startAdvertising calls that have no matching stop call or timeout

**References:** Google android-security-lints, https://github.com/google/android-security-lints

# Wireless Exposure Model

**MUST** treat every wireless channel as reachable by a remote attacker, and justify each one against the exposure it adds.

**Why:** Radio removes the physical-presence assumption the rest of the threat model was built on, so a device in a locked room is suddenly internet-adjacent.

**Detect:** grep the interface inventory for `ble`, `zigbee`, `lora`, `wifi`, `cellular`, and confirm each appears in the threat model with a remote attacker.

**References:** NCSC Operational Technology collection, https://www.ncsc.gov.uk/collection/operational-technology

