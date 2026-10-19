---
categories: [correctness-pitfalls]
domains: [backend]
---

# Abort on Unexpected Error

**MUST** stop the current operation when an unanticipated exception reaches a generic handler, because application state is unknown.

**Why:** Continuing after an unexpected fault means acting on partially applied state - the path to double-spend, skipped authorization or silent corruption.

**Detect:** `catch (Exception`/`except Exception:`/`catch (Throwable` blocks that log and continue instead of rethrowing or aborting the unit of work.

**References:** SAFECode Fundamental Practices v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf
