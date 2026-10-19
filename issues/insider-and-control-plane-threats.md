---
categories: [security-practices]
domains: [backend, governance]
---

# Insider and Control-Plane Threats

**MUST** model authorized-but-malicious insiders, colluding parties, and build or control-plane compromise as first-class threats, not as edge cases.

**Why:** Modern stacks have no defensible perimeter and privileged authority spread across contractors, vendors, and automation, so the actors the model ignores are the ones that succeed.

**Detect:** Read the threat model's actor list and confirm insider, third-party, and CI/control-plane attackers each have modelled paths.

**References:** TRACE threat modelling (arXiv 2606.22214), https://arxiv.org/abs/2606.22214
