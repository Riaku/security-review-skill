---
categories: [hardening-benchmarks]
domains: [infrastructure]
---

# Hardening Verified on Live System

**MUST** verify each hardening control against the running system's enforced behavior after reload and reboot, not against the configuration file that was supposed to apply it.

**Why:** Configuration text and enforced state diverge silently, so a baseline that passes file inspection can be absent at runtime.

**Detect:** kube-bench or lynis against the live host, then a post-reboot re-scan of the same controls

**References:** HardEval, https://arxiv.org/abs/2610.23685, CIS Benchmarks, https://www.cisecurity.org/cis-benchmarks
