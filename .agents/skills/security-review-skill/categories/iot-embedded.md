# iot-embedded

Firmware, OTA, and device-identity security.

## What this category covers

This category covers the security of the device itself and the channel that updates it, where a single failure is permanent because the attacker owns the hardware. Items span per-device provisioning identity, firmware signing and secure-boot verification, and OTA delivery integrity with rollback protection. It is a small category carried by three items, so a reviewer should not expect the finer points of device lifecycle security to be covered here.

- Device identity and provisioning — unique, hardware-bound per-device keys or certificates, with an enrollment and revocation path.
- Firmware signing and secure boot — signed images and bootloader verification enforced rather than logged, with no development or test keys in production images.
- OTA delivery integrity — authenticated update endpoints, device-side TLS pinning, and signed update manifests.
- Update rollback protection — version monotonicity enforced in the bootloader so devices cannot be downgraded to vulnerable firmware.

## What it does not cover

- [secrets-crypto](../categories/secrets-crypto.md) — key storage, rotation, and crypto-primitive choice for application secrets belong there; the per-device identity and its enrollment flow are scoped here.
- [supply-chain](../categories/supply-chain.md) — dependency provenance, reproducible builds, and signed build provenance belong there; firmware signing and secure-boot verification are scoped here.
- [cloud-network](../categories/cloud-network.md) — network topology, TLS termination, and egress control belong there; the device-side update channel and its pinning are scoped here.

## What a finding here looks like

- A single fleet-wide API key or client certificate baked into firmware, so one extraction compromises every unit.
- A bootloader configured to log signature failures instead of enforcing them, or signed with a development key shipped in production.
- An OTA endpoint with no device-side TLS pinning or update-manifest signing, so an on-path attacker can replace firmware.
- No version anti-rollback enforcement, so a device can be downgraded to patched-out vulnerable firmware.
