---
categories: [payments-fraud, secrets-crypto]
domains: [backend]
---

# Per-Message Signing

**MUST** sign individual messages in multi-hop high-value transactions so integrity survives every intermediary, not just each transport leg.

**Why:** Transport encryption ends at each hop, so a compromised or curious intermediary can alter a payment instruction that every leg delivered intact.

**Detect:** read the payment or approval flow and check whether the instruction carries a signature the final party verifies, or only hop-by-hop TLS.

**References:** OWASP ASVS v5.0 V4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x13-V4-API-and-Web-Service.md, NIST SP 800-53 SC-8
