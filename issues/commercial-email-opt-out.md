---
categories: [email-security, regulatory-frameworks]
domains: [backend, governance]
---

# Commercial Email Opt-Out

**MUST** include a functioning unsubscribe mechanism and a valid postal address in every commercial email, and treat unsubscribes as binding on all future sends.

**Why:** Opt-out and sender-identification duties are enforced per message — CAN-SPAM penalties accrue for every non-compliant email sent, so one template missing the footer exposes an entire campaign's volume.
**Detect:** read a bulk campaign template for an unsubscribe link and a physical postal address; check the `List-Unsubscribe` header and that opt-out addresses reach the suppression list consulted before send.
**References:** CAN-SPAM Act, 15 U.S.C. §7704, https://www.law.cornell.edu/uscode/text/15/7704
