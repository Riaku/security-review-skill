# Verification-Level Tiers (ASVS L1/L2/L3: basic / standard / privileged-app requirements)

**MUST** assign each app an ASVS tier (L1 basic, L2 sensitive data, L3 privileged) and verify controls at that level.

**Why:** Untiered apps get theater-grade checks on high-risk systems, leaving privileged-function gaps attackers exploit directly.

**Detect:** grep `ASVS`, `verification_level`, `baseline: L1|L2|L3` in security docs, scanner configs, requirement trackers.

**References:** OWASP ASVS 4.0.3, OWASP SAMM, NIST SP 800-53 control tailoring
