---
categories: [security-practices, testing-strategy]
domains: [governance]
---

# Control Effectiveness Testing

**MUST** test that each security control actually fires — lockout, filter rule, report endpoint, alert route — not merely that it is configured.

**Why:** A control deployed with a typo looks identical to a working one in a configuration review. Only a negative test that should trigger it proves the path is live.

**Detect:** command: an automated control test suite (for example a `pytest tests/security/test_controls.py` job or an active scanner run against staging) that triggers each control and asserts the block or alert.

**References:** OWASP Web Security Testing Guide, NIST SP 800-53 CA-8
