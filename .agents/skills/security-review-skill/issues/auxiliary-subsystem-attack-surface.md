---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Auxiliary Subsystem Attack Surface

**MUST** include secondary control subsystems such as battery, radio, and actuator controllers in the device threat model as reachable and often unauthenticated.

**Why:** Physical-effect subsystems get safety review but rarely adversarial review, so an unauthenticated battery or motor controller becomes remote code execution.

**Detect:** compare the interface inventory (buses, radios, companion-app channels) against the threat model's asset list.

**References:** E-Trojans: e-scooter security assessment (arXiv 2411.17184), https://arxiv.org/abs/2411.17184
