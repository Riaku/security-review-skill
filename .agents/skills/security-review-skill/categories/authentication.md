# authentication

Identity, credentials, session lifecycle.

## What this category covers

This category covers proving who a caller is and keeping that proof valid over time: the credential at rest and in transit, the protocols that issue it, the session or token that carries it, and everything that must invalidate it. The items span password handling (breach blocklists, reset and recovery flows, account enumeration), login hardening (brute-force protection, multi-factor authentication), and the validation details that stop forged or confused tokens in OAuth 2.0, OpenID Connect, SAML, and JWT. They also cover session mechanics (cookie flags, fixation, rotation and revocation on logout or credential change) and non-human or federated identities (service accounts, workload identity, device push tokens, mesh mTLS). Expect findings that describe a way identity can be assumed without the credential: an unverified claim, a session that survives a password change, or a reset token that can be reused.

- Password and credential lifecycle: breach blocklists, reset and recovery flows, reset tokens, and account enumeration.
- Session and token mechanics: cookie flags, fixation, JWT expiry and claim validation, refresh rotation, revocation, and logout.
- Federated and protocol login: OAuth 2.0, OpenID Connect, SAML assertion validation, and social-login account linking.
- Second factors and anti-automation: multi-factor authentication enforcement, brute-force and lockout controls.
- Non-human and workload identity: dedicated service accounts, machine-credential governance, workload-identity claim validation, and push-token binding.

## What it does not cover

- [authorization-access-control](../categories/authorization-access-control.md) — the permission decision made after identity is established belongs there.
- [secrets-crypto](../categories/secrets-crypto.md) — the storage primitives behind credentials (password hashing parameters, key management, cipher choice) belong there.
- [web-api-security](../categories/web-api-security.md) — injection and request-framing attacks belong there even when they target a login endpoint, as do bot and abuse challenges on login, signup, and reset.
- [multi-tenancy](../categories/multi-tenancy.md) — deriving the tenant from the authenticated request and isolating tenants belongs there.

## What a finding here looks like

- A token verifier that accepts the algorithm named in the token header, so an unsigned or re-signed token passes.
- A login or reset response that reveals whether an account exists through its error text or timing.
- A session identifier reused after successful login, so a pre-set cookie becomes an authenticated session.
- Existing sessions that remain valid after a password or second-factor change because nothing invalidates them.
- A reset or invitation token that still works after first use or past a short expiry window.
