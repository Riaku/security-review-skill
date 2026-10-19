---
categories: [secrets-crypto]
domains: [infrastructure]
---

# Negotiation Downgrade Protection

**MUST** reject a negotiation that omits a stronger mechanism both parties support instead of silently accepting the weaker option.

**Why:** A downgrade attack strips the strong option from the offer so the weaker path is chosen legitimately. If omission is accepted, the attacker never has to break the cryptography at all.

**Detect:** judgment: the negotiation code path and its test vectors — what the implementation does when the strong mechanism is removed from the peer's offer.

**References:** CWE-757 Selection of Less-Secure Algorithm During Negotiation
