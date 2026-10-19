---
categories: [ai-llm, authentication]
domains: [backend]
---

# Agent Auth Strength Parity

**MUST NOT** let an automated agent reach privileged operations through weaker authentication than a human would need for the same operation.

**Why:** An agent holding broad permissions behind a static key is a privilege escalator: attack the weaker credential, inherit the stronger authority.

**Detect:** compare the agent's credential type against the operations in its tool manifest; a long-lived API key or unauthenticated local socket reaching admin actions is the finding.

**References:** NIST SP 800-207 §5.7, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 IA-5
