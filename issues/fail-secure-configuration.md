# Fail-Secure Configuration

**MUST** design components to fail in a secure state: auth failures deny access, TLS verification failures abort the connection, policy engine outages block rather than allow, and partial initialization never exposes privileged surfaces.

**Why:** Fail-open is the silent killer — an auth service timeout that defaults to "allowed" or a verifier that skips on error turns an outage into a breach window.

**Detect:** grep for `except: pass` / default-allow branches around authz and TLS verify calls; check `failOpen: false` on admission webhooks, `ssl_verify` defaults, circuit-breaker fallback behavior on security checks.

**References:** OWASP Secure Product Design Cheat Sheet (fail securely), NIST SP 800-162 fail-closed guidance
