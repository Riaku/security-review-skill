---
categories: [sre-incidents]
domains: [reliability]
---

# Chaos Engineering

**MAY** run controlled failure injection in production-like environments, scoped by blast radius and abort criteria.

**Why:** Untested redundancy is assumed redundancy; failover paths quietly rot between verified drills.

**Detect:** `chaos-mesh`, `litmus`, Gremlin config, absence of game-day logs, no abort/steady-state criteria in experiment manifests.

**References:** Principles of Chaos Engineering, Netflix Chaos Monkey, AWS FIS, NIST SP 800-34 drills
