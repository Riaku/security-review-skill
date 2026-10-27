---
categories: [authentication]
domains: [backend]
---

# MFA

**SHOULD** require a second factor for all administrative and remote-access accounts, enforced server-side after primary auth.

**Why:** Password-only admin access means one phished or breached credential grants full control with no second barrier.

**Detect:** grep admin/SSH/RDP login paths for missing `mfa`/`totp`/`webauthn` checks, MFA toggle client-side only, `mfa_enabled` field absent in user model.

**References:** OWASP API2:2023 Broken Authentication, NIST SP 800-63B §5.1, OWASP A07:2021, CWE-308, CIS Control 6.3
