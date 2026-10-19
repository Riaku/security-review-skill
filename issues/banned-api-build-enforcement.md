---
categories: [security-practices]
domains: [backend]
---

# Banned API Build Enforcement

**MUST** enforce banned-function lists mechanically at build time so forbidden calls fail compilation or lint rather than review.

**Why:** Review attention is finite and memory is worse; a dangerous call that only a reviewer might catch survives until the day it does not.

**Detect:** Banned-API analyzer rules wired into the build (DevSkim rules, CodeQL custom queries); re-add a banned call and confirm CI fails.

**References:** DevSkim, https://github.com/microsoft/DevSkim, SAFECode Fundamental Practices v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf
