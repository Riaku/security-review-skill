---
categories: [documentation-quality]
domains: [backend]
---

# Simplified Technical English for Procedures

**SHOULD** write operational/procedural documentation in controlled language per ASD-STE100: short sentences (max ~25 words), one meaning per word, active voice, one instruction per step, no idioms.

**Why:** Procedures followed under stress by non-native speakers must be unambiguous — STE exists because aerospace maintenance deaths traced to prose ambiguity; the same failure mode applies to runbooks and security procedures.

**Detect:** for runbooks/install steps: check sentence length, one-action-per-step structure, controlled vocabulary consistency (no synonym rotation: "log in/sign in/login" for the same action); flag idiomatic or marketing prose in procedural sections.

**References:** ASD-STE100 Simplified Technical English (asd-ste100.org), aerospace/defense doc standards, runbook readability practice
