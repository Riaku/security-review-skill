---
categories: [authentication]
domains: [backend]
---

# Force Invalidation After Breach

**MUST** invalidate breached credentials and sessions server-side rather than relying on users to rotate them after notification.

**Why:** Measured post-breach response is a minority of affected users within months, so the compromised credential stays live unless the operator forces it.

**Detect:** grep the credential-compromise path for forced session invalidation, `password_reset_required`, or a token-version bump instead of an email-only notice.

**References:** Measurement of post-breach password change, https://arxiv.org/abs/2010.09853, NIST SP 800-63B-4 (credential recovery)
