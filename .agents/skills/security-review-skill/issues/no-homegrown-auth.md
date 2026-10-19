---
categories: [authentication]
domains: [backend]
---

# No Homegrown Auth

**MUST NOT** invent an authentication protocol or session-token format; use a maintained library or identity provider.

**Why:** Auth protocols carry decades of accumulated attack knowledge, and homegrown formats miss the known classes: algorithm confusion, fixation, replay.

**Detect:** grep for hand-built token minting (base64 of user id plus HMAC), custom `login`/`session` cookie formats, and password checks implemented outside the auth library.

**References:** OWASP Authentication Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html, NIST SP 800-63B-4 Digital Identity Guidelines, https://pages.nist.gov/800-63-4/sp800-63b.html
