---
categories: [scaling-capacity]
domains: [reliability]
---

# Autoscaling

**SHOULD NOT** scale on metrics an attacker can inflate cheaply (raw request count, queue depth) without a max-replica ceiling and scale-up stabilization window.

**Why:** A flood or spam burst can trigger runaway scale-out, exhausting cluster quota and cloud budget while serving nothing legitimate.

**Detect:** grep HPA/KEDA configs for `maxReplicas`, `stabilizationWindowSeconds`, target metric source; flag missing ceilings or scale-up driven by unauthenticated request rate.

**References:** CWE-770, OWASP ASVS 14.2, AWS Well-Architected REL08-BP05
