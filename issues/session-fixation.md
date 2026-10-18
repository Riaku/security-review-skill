# Session Fixation

**MUST** regenerate the session identifier immediately after any successful authentication or privilege change.

**Why:** If the session ID survives login, an attacker who planted one earlier rides the victim's now-authenticated session undetected.

**Detect:** grep login handlers for missing `session.regenerate`, `session_id` unchanged post-auth, `secure`/`httpOnly` cookie flags absent on session cookies.

**References:** OWASP A07:2021, CWE-384, NIST SP 800-53 SC-25, OWASP Session Management Cheat Sheet
