---
categories: [compliance-privacy, web-client-security]
domains: [frontend, governance]
---

# Session Replay Capture Scope

**MUST** gate session replay and input recording on disclosure and consent, and mask password, payment, and other sensitive fields before any capture leaves the browser.

**Why:** Recording what users type captures credentials, payment data, and private messages; undisclosed interception of communications is actionable under state wiretap statutes such as CIPA, and the recording is a processing purpose the original consent never covered.
**Detect:** grep the bundle for replay SDKs (`rrweb`, FullStory, Hotjar, LogRocket, Datadog Session Replay); confirm the init call sits behind the consent check and the block/mask selectors cover password, payment, and free-text inputs.
**References:** California Penal Code §630 et seq. (CIPA), GDPR Art. 5(1)(c), https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
