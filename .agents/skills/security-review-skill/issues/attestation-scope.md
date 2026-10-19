---
categories: [iot-embedded]
domains: [infrastructure]
---

# Attestation Scope Declaration

**MUST** state the root-of-trust class and attested state scope — boot, runtime, update, erasure — whenever an attestation result is used as an authorization input.

**Why:** 'The device is attested' answers different questions depending on whether the root is hardware or software and which state was measured.

**Detect:** judgment: the attestation policy — which claims are consumed and what each claim actually proves

**References:** Remote attestation literature review, https://arxiv.org/abs/2105.02466
