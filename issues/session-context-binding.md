---
categories: [authentication]
domains: [backend]
---

# Session Context Binding

**SHOULD** record client context at session establishment and treat a significant mid-session change as a step-up signal, never as proof of identity.

**Why:** A stolen session cookie replays from a different network and device. Comparing context catches the reuse, while treating a matching context as authentication would let an attacker who copied it through.

**Detect:** grep session creation for stored client context fields (address, user agent, locale) and for a comparison on later requests; flag comparisons that grant access on match.

**References:** OWASP Cookie Theft Mitigation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Cookie_Theft_Mitigation_Cheat_Sheet.html, NIST SP 800-63B session binding guidance
