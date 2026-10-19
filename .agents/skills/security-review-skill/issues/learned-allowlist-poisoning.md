---
categories: [web-api-security]
domains: [infrastructure]
---

# Learned Allowlists Poison Easily

**MUST** validate a traffic-learned allowlist against a clean baseline before enforcing it, because small contamination poisons the learned profile.

**Why:** A learned profile degrades at fractions of a percent of poisoned requests and then admits the attacker's payload shape as legitimate.

**Detect:** grep WAF and proxy config for learning or auto-tuning modes enabled against production traffic without a filtered training source.

**References:** WAF allowlist poisoning study, https://arxiv.org/abs/2609.06840
