---
categories: [ai-llm, documentation-quality]
domains: [backend]
---

# Capability Envelope Documentation

**MUST** document each model-backed feature's knowledge limits, tested validity range, and intended human oversight, and surface them where decisions are made.

**Why:** Undocumented capability boundaries invite over-trust, and over-trust is the exploit: users act on output outside the range where it was ever validated.

**Detect:** read the feature's model card or docs for stated limits, tested scope, and oversight expectations, then check whether the UI repeats them.

**References:** NIST AI 600-1 MAP 2.2, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
