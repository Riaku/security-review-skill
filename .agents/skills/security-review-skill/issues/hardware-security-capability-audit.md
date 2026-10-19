---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Hardware Security Capability Audit

**MUST** verify which hardware protections a device actually provides and enables, rather than trusting the platform's security claims.

**Why:** The gap between silicon capability and what firmware enables is where most embedded exposure lives, and marketing material never documents it.

**Detect:** grep the startup and linker code for the protections being turned on (`MPU->CTRL`, `SAU->CTRL`, `TZEN`, `SCB->CCR`) and compare with the SoC's documented features.

**References:** SoK: Arm Cortex-M security (arXiv 2401.15289), https://arxiv.org/abs/2401.15289
