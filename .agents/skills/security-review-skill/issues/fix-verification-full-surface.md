---
categories: [testing-strategy]
domains: [backend]
---

# Verify Fixes Beyond The Finding

**MUST** verify a security fix by re-running the full scanner set plus a behavioral exploit test, never by the disappearance of one finding.

**Why:** A change can silence the named check while leaving sibling findings, breaking behavior, or missing the security intent entirely.

**Detect:** command re-run every configured scanner and the exploit test for the class, then diff the complete result set before and after the fix.

**References:** TerraProbe repair verification, https://arxiv.org/abs/2606.26590
