# Webhook Signature Verification

**MUST** Verify the provider HMAC over the raw body with constant-time comparison before acting on any webhook.

**Why:** Unsigned endpoints accept forged events — fake payments, refunds, account changes.

**Detect:** Handlers with no signature check; `hmac.compare_digest` absent; verification skipped in dev branches.

**References:** CWE-347, CWE-208, Stripe/GitHub webhook signing docs
