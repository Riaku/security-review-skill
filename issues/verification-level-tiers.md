# Verification-Level Tiers (ASVS L1/L2/L3: basic / standard / privileged-app requirements)

**MUST** assign every application an ASVS baseline (L1 threat-modeled, L2 sensitive data, L3 privileged) and verify controls at that tier.

**Why:** Untiered apps get either theater-grade checks for high-risk systems or gaps that privileged attackers exploit.

**Detect:** grep for `ASVS`, `verification_level`, `baseline: L1|L2|L3` in security docs, scanner configs, requirements trackers.

**References:** OWASP ASVS 4.0.3, OWASP SAMM, NIST SP 800-53 tailoring
