# authentication — full checklist (79 items)

Identity, credentials, session lifecycle.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/authentication.md](../categories/authentication.md) · Index: [SKILL.md](../SKILL.md)

# Account Enumeration

**SHOULD NOT** reveal whether an account exists through differing responses, timing, or error messages on login, registration, and password-reset endpoints.

**Why:** Distinct "user not found" vs "wrong password" responses let attackers build a valid username list for targeted phishing or credential stuffing.

**Detect:** grep for `user not found`, `email already exists`, `invalid username` strings; differing HTTP status codes (404 vs 401) on auth endpoints.

**References:** OWASP A07:2021, CWE-204, CWE-203, NIST SP 800-63B-4 §3.2.2

# Account recovery and password-reset flow security (tokens, helpdesk takeover)

**MUST NOT** allow helpdesk or support staff to reset a user's password without a verified second channel (e.g. confirmed email + MFA challenge) and full audit logging.

**Why:** Social-engineering the helpdesk is the cheapest path to takeover; a single unverified reset request bypasses every other control.

**Detect:** grep support/reset tooling for missing identity-verification step, no `audit_log` on manual resets, reset-by-username-only admin endpoints without MFA gate.

**References:** NIST SP 800-63B §5.1.1.2, CWE-287, OWASP A07:2021, CWE-354

# Admin Reset Blindness

**MUST** let administrators trigger a password reset without ever setting, viewing, or learning the user's password.

**Why:** An admin who knows the user's password destroys non-repudiation: every later action by that account is plausibly the administrator's.

**Detect:** grep admin endpoints for a `new_password` or generated-password field targeting another user id.

**References:** OWASP ASVS v5.0 V6.4.6, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md

# Agent Auth Strength Parity

**MUST NOT** let an automated agent reach privileged operations through weaker authentication than a human would need for the same operation.

**Why:** An agent holding broad permissions behind a static key is a privilege escalator: attack the weaker credential, inherit the stronger authority.

**Detect:** compare the agent's credential type against the operations in its tool manifest; a long-lived API key or unauthenticated local socket reaching admin actions is the finding.

**References:** NIST SP 800-207 §5.7, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 IA-5

# Anomalous Authentication Detection (impossible travel, rare UA/IP)

**SHOULD** monitor for impossible-travel, rare user-agent, and unfamiliar-IP login patterns and trigger step-up MFA or alerting on anomalies.

**Why:** Without anomaly detection, an attacker logging in from a foreign IP with a stolen credential looks identical to the legitimate user and passes silently.

**Detect:** grep auth pipeline for absent `impossible_travel`, `geoip`, `ua_fingerprint` checks; no step-up MFA on new-device login; no alerting on geo-velocity anomalies.

**References:** OWASP A07:2021, CIS Control 8.3, MITRE ATT&CK T1078

# API Gateway / Edge Endpoints Deployed Without Authorizers

**MUST** attach an authorizer (IAM, JWT, Lambda/Cognito, or mTLS) to every deployed API route, with authorization denied by default rather than per-route opt-in.

**Why:** Routes created quickly for testing routinely reach production still marked `AUTH = NONE`; scanners find them within hours, and internal endpoints often carry admin-shaped functionality with the assumption that "nobody knows the URL."

**Detect:** In OpenAPI/Swagger specs check for missing or `security: []` operations; in SAM/CloudFormation look for `AuthorizationType: NONE` on `AWS::ApiGateway::Method`; on API Gateway v2 check `AuthorizationType` absent from routes. Also review ingress annotations and edge-function configs where auth middleware is applied per-route instead of globally.

**Bad:**
```yaml
MyMethod:
  Type: AWS::ApiGateway::Method
  Properties:
    AuthorizationType: NONE
    Integration: {Type: AWS_PROXY, Uri: !GetAtt AdminFn.Arn}
```

**Good:**
```yaml
MyMethod:
  Type: AWS::ApiGateway::Method
  Properties:
    AuthorizationType: COGNITO_USER_POOLS
    AuthorizerId: !Ref UserPoolAuthorizer
```

**References:** OWASP A01:2021, OWASP ASVS 4.1, AWS API Gateway authorization docs, CWE-306

# Default admin password, signing key and webhook auth on control planes

**MUST** replace a product's shipped default administrative password, set a unique token-signing key, and authenticate every webhook receiver before exposing a self-hosted control plane; ArgoCD's `admin` password and auto-generated `server.secretkey` are the canonical example (CWE-1188).

**Why:** ArgoCD ships with a known default admin and auto-generated signing key; an attacker who reaches the UI or webhook endpoint gains cluster-wide deploy control.

**Detect:** check `argocd-secret` for unchanged `admin.password`, default `server.secretkey`, webhook receivers without `secret`/HMAC verification, `admin.enabled: true` in values.

**References:** ArgoCD Security Guide, CWE-1188, OWASP A05:2021

# Authentication Pathway Parity

**MUST** enforce the same authentication strength on every pathway, including legacy APIs, support tooling, and partner integrations.

**Why:** Support portals, legacy APIs, and partner integrations quietly carry weaker auth than the main login, so the real security level is the minimum.

**Detect:** grep route registration against the auth middleware (`app.get(`, `router.post(`, `@app.route`) for handlers with no auth dependency or factor check.

**References:** OWASP ASVS v5.0 V6.1.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B

# Auto-Mounted Service Account Tokens in Pods That Don't Need the API

**SHOULD** set `automountServiceAccountToken: false` on pods and serviceaccounts that never call the Kubernetes API.

**Why:** An unnecessary mounted token is a standing credential an attacker with any file-read bug can use against the API server.

**Detect:** Pod specs without `automountServiceAccountToken: false`; mounted path `/var/run/secrets/kubernetes.io/serviceaccount` in non-API workloads.

**References:** CIS K8s 5.1.6, CWE-522, OWASP Kubernetes Top 10 K06, NIST SP 800-190 5.2

# Biometrics Secondary Only

**MUST** use biometrics only as a secondary factor paired with something the user has or knows.

**Why:** Biometrics cannot be revoked or reissued, and a copied or coerced fingerprint authenticates forever.

**Detect:** walk the login flow and check whether a biometric success alone issues a session.

**References:** OWASP ASVS v5.0 V6.5.7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B

# Force Invalidation After Breach

**MUST** invalidate breached credentials and sessions server-side rather than relying on users to rotate them after notification.

**Why:** Measured post-breach response is a minority of affected users within months, so the compromised credential stays live unless the operator forces it.

**Detect:** grep the credential-compromise path for forced session invalidation, `password_reset_required`, or a token-version bump instead of an email-only notice.

**References:** Measurement of post-breach password change, https://arxiv.org/abs/2010.09853, NIST SP 800-63B-4 (credential recovery)

# Breached & Common Password Blocklist

**SHOULD** reject new or changed passwords found in known-breached or common-password lists (e.g. HaveIBeenPwned k-anonymity API).

**Why:** Reusing a password exposed in a prior breach means credential-stuffing bots will try it against your service within hours of exposure.

**Detect:** grep password policy code for absent blocklist/pwned-password check and no `k-anonymity`/`pwnedPasswords` call; flag policies enforcing character-class composition rules instead of length plus blocklist (NIST SP 800-63B forbids composition rules).

**References:** NIST SP 800-63B §5.1.1.2, OWASP A07:2021, CWE-521, NCSC Pwned Passwords guidance

# Brute Force Protection

**MUST** rate-limit and lock out repeated failed authentication attempts per account and per source IP.

**Why:** Without throttling, automated credential-stuffing and dictionary attacks can try millions of passwords against a login form unimpeded.

**Detect:** grep login endpoints for missing `rate_limit`, `attempt_count`, `lockout` logic; no backoff on 401 responses; unlimited POST to `/login`.

**References:** OWASP A07:2021, CWE-307, NIST SP 800-63B §5.2.2, CIS Control 6.2

# Consent Revocation Surface

**MUST** give users a self-service view of granted authorizations and active tokens, with the ability to revoke each one.

**Why:** Consent without a revocation path accumulates invisible standing privilege that outlives the user's intent and the client's trustworthiness.

**Detect:** locate the connected-applications and active-sessions screens and check each grant can be revoked individually.

**References:** OWASP ASVS v5.0 V10.4.9, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md

# Cookie Flags: Secure, HttpOnly, SameSite

**MUST** set `Secure`, `HttpOnly`, and `SameSite=Lax` (or `Strict`) on every session cookie issued by the application.

**Why:** Missing flags let cookies leak over HTTP, be read by injected scripts, or ride cross-site requests, enabling session hijacking and CSRF.

**Detect:** grep `Set-Cookie`, `res.cookie(`, `document.cookie=`; inspect ingress/Envoy/nginx cookie-rewrite annotations for stripped flags.

**References:** RFC 6265, draft-ietf-httpbis-rfc6265bis §4.1.2.7 (SameSite), OWASP Session Management Cheat Sheet, CWE-1004, CWE-1275

# Credential Access Detection (keylogging, token theft, credential dumping patterns)

**SHOULD** detect credential harvesting: LSASS dumps, keylogging hooks, OAuth token replay, metadata-service credential scraping.

**Why:** Stolen credentials are the leading initial-access vector; catching the theft step stops breaches identity controls alone miss.

**Detect:** grep detection content for `T1003`, `lsass`, `mimikatz`, `secretsdump`, alerts on `169.254.169.254` access, token-replay rules.

**References:** MITRE ATT&CK TA0006/T1003, NIST SP 800-63B, CWE-522, GuardDuty credential-access detections

# Dedicated Service Accounts per Workload

**SHOULD NOT** run workloads under the `default` Kubernetes service account; each workload should declare a dedicated `serviceAccountName` scoped to exactly the API access it needs.

**Why:** The default SA is shared by every pod that doesn't override it, so any IAM or RBAC grant made for one workload silently applies to all of them, and audit logs cannot attribute an API call to the workload that made it. Dedicated identities are the prerequisite for least-privilege cloud IAM (IRSA/workload identity), per-workload RBAC, and meaningful `automountServiceAccountToken` control.

**Detect:** `spec.serviceAccountName` absent or `default` in Deployments/Pods/StatefulSets; `default` SA bound to any Role/ClusterRole beyond the baseline; IAM roles (e.g. EKS IRSA annotations) attached to workloads running as `default`. Policy engines: Kyverno `require-dedicated-service-accounts` / a equivalent admission rule.

**References:** CIS Kubernetes 5.1.5 (default service accounts not actively used), K8s service accounts docs, EKS IRSA / GKE Workload Identity guidance, aquasecurity/trivy-checks KSV010–KSV012

# Default & Weak Credentials in Shipped Software

**MUST NOT** ship software with default usernames/passwords or demo accounts enabled in production; force credential change on first login.

**Why:** Scanners sweep the internet for known default credentials (admin/admin, root/toor) and compromise unmodified deployments within minutes of exposure.

**Detect:** grep configs/seed files for `admin:admin`, `changeme`, `default_password`, hardcoded credentials in Docker images, demo accounts in fixtures shipped to prod.

**References:** CWE-1188, OWASP A05:2021, CIS Control 4.7, NIST SP 800-63B

# Lockout-Resistant Throttling

**MUST NOT** let failed-login throttling disable a known account; rate-limit per credential and source so an attacker cannot lock the owner out.

**Why:** Account-only lockout hands an attacker a denial-of-service switch against any known user; throttling per credential and source slows the attack without disabling the owner.

**Detect:** Login and OTP handlers that lock or disable the account after N failures, keyed on `username`/`email` alone.

**References:** Application Security Handbook: Trusted Devices, https://github.com/0xn3va/application-security-handbook/blob/main/Web%20Application/Concept%20of%20Trusted%20Devices/README.md

# Discovery Metadata Binding

**MUST** verify that discovered configuration metadata declares exactly the identifier used to fetch it, and that its TLS identity covers that identifier.

**Why:** Without the binding, an attacker publishes metadata for someone else's identifier and the client trusts the attacker's issuer, scopes, or endpoints.

**Detect:** grep `/.well-known/` metadata fetch code for an exact-match comparison of the returned identifier against the request identifier.

**References:** RFC 9728 OAuth Protected Resource Metadata, https://www.rfc-editor.org/rfc/rfc9728.html, RFC 8414 Authorization Server Metadata, https://www.rfc-editor.org/rfc/rfc8414.html

# Email Is Not a Factor

**MUST NOT** treat email possession as a single or second authentication factor; use a dedicated possession or knowledge factor.

**Why:** Email is guarded by the user's weakest password and readable by administrators, forwarding rules, and anyone who resets it.

**Detect:** grep MFA and step-up verification paths for `email` as the delivered or verified factor.

**References:** OWASP ASVS v5.0 V6.3.6, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B

# Embedded WebView Credential Entry

**MUST NOT** collect credentials inside a webview or embedded browser owned by another application; use the platform browser or the system authentication API.

**Why:** The host application can record every keystroke, auto-submit the form, and read the session cookie, so the credential is disclosed to a party the identity provider never authorized.

**Detect:** grep for `WebView`, `WKWebView`, `webview_flutter`, or `WebViewClient` loading an authorization or login URL.

**References:** RFC 8252 OAuth 2.0 for Native Apps, https://www.rfc-editor.org/rfc/rfc8252.html

# Exact Redirect URI Matching

**MUST** compare OAuth redirect URIs against a registered exact-match allowlist, rejecting wildcards, prefix matches, and unregistered ports or paths.

**Why:** Loose matching lets an attacker craft a URI that begins with the trusted value and receives the authorization code. One accepted prefix is a full account-takeover primitive.

**Detect:** grep OAuth client config and callback handlers for `redirect_uri` compared with `startsWith`, `contains`, a regex, or a wildcard entry; the comparison must be exact equality against a registered value.

**References:** OWASP OAuth 2.0 Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html, RFC 9700 OAuth 2.0 Security Best Current Practice, https://www.rfc-editor.org/rfc/rfc9700.txt

# Handoff Credential Reuse Detection

**MUST** reject a second redemption of an already-used authorization code or refresh token and revoke every token issued from that grant.

**Why:** Reuse of a redeemed credential is proof of theft, and quietly returning an error leaves the attacker's stolen tokens alive.

**Detect:** grep for a consumed-code or rotated-refresh store (`used_jti`, `code_consumed`, `refresh_token` family id) and for a revocation cascade on reuse.

**References:** OWASP ASVS v5.0 V10.4.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 6749 §4.1.2

# Identifier Is Not a Secret

**MUST NOT** authenticate with a serial number, MAC address, or other identifier that is printed on the device or shared with third parties.

**Why:** Identifiers are visible to dealers, registries, and anyone on the local link, so they leak by design and cannot be rotated after exposure.

**Detect:** grep serial, imei, mac_address values used in password comparison, token derivation, or as HMAC key material

**References:** Ross Anderson, Security Engineering (3rd ed.), https://www.cl.cam.ac.uk/~rja14/book.html

# Insufficient Randomness for Tokens and IDs

**MUST** generate session tokens, password resets, API keys, and invite codes from a cryptographically secure RNG (`secrets`, `crypto.randomBytes`, `SecureRandom`), never `random`/`Math.random`/sequential IDs.

**Why:** Predictable randomness lets attackers guess reset links and session tokens, taking over accounts without ever touching the password.

**Detect:** `Math.random()`, Python `random.` for tokens, `uuid1`/sequential IDs in auth flows, `rand()` in token generation code.

**References:** OWASP ASVS V3.2.2, CWE-330, NIST SP 800-90A

# JWT Algorithm Confusion / alg=none / Unverified Signatures

**MUST NOT** accept `alg: none` or allow the token header to select the verification algorithm; pin the expected algorithm server-side.

**Why:** If the verifier trusts the header's `alg`, an attacker switches to `none` or swaps RS256→HS256 to forge unsigned or HMAC-forged tokens.

**Detect:** grep for `jwt.decode` without `algorithms=[...]`, `alg.*none`, dynamic algorithm selection from token header, missing algorithm allowlist.

**References:** CWE-347, OWASP A02:2021, RFC 8725 §3.1, Auth0 JWT Algorithm Confusion advisory

# JWT Audience/Issuer Validation & kid/JWKS Abuse

**MUST** verify `iss` and `aud` claims against an explicit allowlist and pin `kid` to a trusted JWKS entry before accepting a token.

**Why:** Unpinned `kid` lets an attacker point the verifier at a rogue JWKS or reuse a token minted for a different service as valid here.

**Detect:** grep verifier config for missing `issuer`/`audience` checks, `jwks_uri` fetched without TLS pinning, `kid` resolved dynamically with no allowlist.

**References:** RFC 8725 §3.8-3.9, CWE-345, OWASP A02:2021, OIDC Core §3.1.3.7

# JWT Expiry

**MUST** set short-lived access tokens (15 minutes or less) with an explicit `exp` claim that the verifier rejects when past.

**Why:** A stolen or leaked long-lived JWT stays usable indefinitely, giving an attacker persistent API access with no way to expire out.

**Detect:** grep for `expiresIn`, `exp:` with values like `86400`, `7d`, `never`; missing `exp` claim in token payloads or verifier code.

**References:** OWASP A02:2021, CWE-613, RFC 7519 §4.1.4, NIST SP 800-63B §7.1

# Service Mesh Permissive mTLS and Direct-Pod-IP Bypass

**MUST NOT** treat permissive-mode mTLS as an access-control boundary; enforce STRICT mTLS per namespace and pair it with NetworkPolicies that block plaintext direct-pod-IP access.
**SHOULD** Where a service mesh is deployed, enforce mutual TLS in STRICT mode between sidecars and remove plaintext permissive fallbacks before production sign-off.

**Why:** Permissive mode accepts both meshed (mTLS) and raw plaintext traffic, so an attacker inside the cluster — or a compromised pod — simply bypasses the sidecar by dialing the pod IP on the plaintext port, and any authorization policy keyed on peer identity silently fails open for that path.

**Detect:** Check PeerAuthentication `mtls.mode: PERMISSIVE` (or mesh-wide default), AuthorizationPolicies that allow when principal is empty, CNI/network policies that don't restrict pod ports to sidecar traffic only, and services reachable on `podIP:port` in egress tests. Verify destination rules route through the service, not resolved pod endpoints. Also check `PeerAuthentication`/`DestinationRule` for `mtls.mode: STRICT` versus `PERMISSIVE`/`DISABLED`, and look for namespace-wide exemptions and `excludeOutboundPorts` annotations smuggling traffic around the mesh.

**Bad:**
```yaml
mtls:
  mode: PERMISSIVE   # plaintext to podIP:8080 still accepted
```

**Good:**
```yaml
mtls:
  mode: STRICT
# plus NetworkPolicy restricting the port to the mesh sidecar
```

**References:** Istio security docs (permissive mTLS caveats), Istio mTLS docs, NIST SP 800-207 Zero Trust, CNCF zero-trust whitepaper, OWASP Kubernetes Top 10, CWE-300

# MFA

**SHOULD** require a second factor for all administrative and remote-access accounts, enforced server-side after primary auth.

**Why:** Password-only admin access means one phished or breached credential grants full control with no second barrier.

**Detect:** grep admin/SSH/RDP login paths for missing `mfa`/`totp`/`webauthn` checks, MFA toggle client-side only, `mfa_enabled` field absent in user model.

**References:** NIST SP 800-63B §5.1, OWASP A07:2021, CWE-308, CIS Control 6.3

# Missing Authentication Middleware / Default-Deny Routing

**MUST** default-deny: every route requires authentication unless explicitly marked public via an allowlist.

**Why:** Route-by-route opt-in means any forgotten or newly added endpoint ships unauthenticated, exposing internal APIs to the internet.

**Detect:** grep router config for missing global auth middleware, routes without `@authenticated`/`requireAuth`, `public: true` as default, admin endpoints outside auth filter chain.

**References:** OWASP A01:2021, CWE-306, NIST SP 800-53 AC-3, CIS Control 6.7 (Centralize Access Control)

# No Forced Password Rotation

**MUST NOT** force periodic password rotation; keep credentials valid until compromise is suspected or the user rotates them.

**Why:** Calendar rotation produces minimal-delta variants of the same password and floods the reset channel, without removing any attacker's access.

**Detect:** grep for expiry-driven password policy (`password_expires`, `max_password_age`, `chage -M`, `pwdLastSet` enforcement).

**References:** OWASP ASVS v5.0 V6.2.10, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B §5.1.1.2

# No Homegrown Auth

**MUST NOT** invent an authentication protocol or session-token format; use a maintained library or identity provider.

**Why:** Auth protocols carry decades of accumulated attack knowledge, and homegrown formats miss the known classes: algorithm confusion, fixation, replay.

**Detect:** grep for hand-built token minting (base64 of user id plus HMAC), custom `login`/`session` cookie formats, and password checks implemented outside the auth library.

**References:** OWASP Authentication Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html, NIST SP 800-63B-4 Digital Identity Guidelines, https://pages.nist.gov/800-63-4/sp800-63b.html

# No Human Verification Controls

**MUST NOT** rely on users comparing codes, recognizing voices, or noticing warnings as a security control; the check must be cryptographic.

**Why:** Synthetic voice and video defeat channel authentication by human senses, and optional security prompts are ignored at scale.

**Detect:** in the auth or pairing flow, identify whether the only man-in-the-middle defence is a value the user is asked to compare.

**References:** RFC 8826 §4.3.2.2, https://www.rfc-editor.org/rfc/rfc8826.html

# No Implicit Session Creation

**MUST NOT** create or refresh a session without an explicit user action, so prefetch, bots, and link scanners cannot mint sessions.

**Why:** Silent creation multiplies sessions nobody asked for, each one a credential to steal, and lets a link previewer authenticate as the recipient.

**Detect:** grep session creation inside GET handlers and middleware that issues a cookie on any request.

**References:** OWASP ASVS v5.0 V7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x16-V7-Session-Management.md

# No Password Composition Rules

**MUST NOT** impose character-class composition rules on passwords; enforce a minimum length and accept long passphrases instead.

**Why:** Composition rules push users toward predictable transforms of familiar words, producing passwords that satisfy the meter and fall to the first dictionary.

**Detect:** grep password validation for upper/lower/digit/symbol regexes and for a `maxlength` that blocks passphrases.

**References:** OWASP ASVS v5.0 V6.2.5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B §5.1.1.2

# Non-Human Identity Governance (service accounts, machine creds inventoried and scoped)

**MUST** inventory every service account, API key, and machine credential with an owner, least-privilege scope, and expiry.

**Why:** Machine identities outnumber humans 50:1 and are rarely reviewed; orphaned service accounts become attackers' favorite door.

**Detect:** grep `service_account`, `api_key`, `client_secret` inventories, orphaned-credential reports, workload-identity configs.

**References:** NIST SP 800-63B, CIS Control 6, OWASP Non-Human Identities Top 10, CSA NHI guidance

# Non-Reassignable Identity

**MUST** identify users by an issuer-and-subject pair that cannot be reassigned, never by email, username, or phone number.

**Why:** Recycled identifiers hand a new holder the previous user's account: the email is reassigned and every grant keyed to it comes along.

**Detect:** grep for user lookup and account linking keyed on `email`, `username`, or `phone` instead of `(iss, sub)` or an immutable internal id.

**References:** OWASP ASVS v5.0 V10.3.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, CWE-287

# OAuth 2.0

**MUST** validate the `state` parameter on every authorization callback and use PKCE for public clients.

**Why:** Missing state/PKCE enables CSRF and authorization-code interception, letting an attacker bind a victim's code to their own session.

**Detect:** grep callback handlers for absent `state` checks, `response_type=token` in public clients, missing `code_verifier`/`code_challenge` in auth URL construction.

**References:** OWASP A01:2021, CWE-352, RFC 6749 §10.12, RFC 9700 §2.1/§4.7

# OAuth Mix-Up Defense

**MUST** validate the issuer identifier in both the authorization and token responses whenever a client can talk to more than one authorization server.

**Why:** Without per-response attribution, a malicious provider hands the client another provider's code, and the client completes the flow against the wrong authority.

**Detect:** grep the callback and token handlers for `iss` validation; a client configured with several providers that reads only `code` is exposed.

**References:** OWASP ASVS v5.0 V10.2.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 9207 (iss parameter), CWE-290

# OOB Code Transaction Binding

**MUST** bind every out-of-band code or approval request to the authentication transaction that created it, so it cannot satisfy another one.

**Why:** Unbound codes let an attacker trigger many flows, collect delivered codes, and apply any of them to the session being attacked.

**Detect:** grep OTP verification for lookup by code alone rather than by `(code, transaction_id)` or an equivalent server-side binding.

**References:** OWASP ASVS v5.0 V6.6.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md

# OpenID Connect

**MUST** validate the ID token's signature, `iss`, `aud`, and `nonce` before trusting any identity claim.

**Why:** Skipping ID token validation lets an attacker replay a token from another client or provider and be accepted as a different user.

**Detect:** grep for `id_token` usage without `verify`/`validate` calls, missing `nonce` in auth request, `aud` not checked against client ID.

**References:** OIDC Core §3.1.3.7, CWE-347, OWASP A02:2021, NIST SP 800-63B

# Hashed One-Time Secrets

**MUST** store one-time and recovery codes as salted hashes, so a database read does not hand an attacker the second factor.

**Why:** A plaintext code store hands an attacker the second factor along with the database.

**Detect:** grep for plaintext `otp`/`recovery_code` columns and confirm generation and verification both go through the hash.

**References:** OWASP ASVS v5.0 V6.5.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B

# Password Reset Flow Security

**MUST** issue single-use, high-entropy reset tokens with short expiry (≤15 min) over HTTPS, invalidated on use or password change.

**Why:** Reusable or long-lived reset tokens let an attacker who intercepts one take over an account at leisure, bypassing the password entirely.

**Detect:** grep reset handlers for tokens without `exp`/`used` flags, tokens in URL query strings logged by proxies, `md5(email)` as token, no rate limit on `/forgot-password`.

**References:** OWASP A07:2021, CWE-640, CWE-639, NIST SP 800-63B §5.1.1.2

# Per-Client Protocol Surface

**MUST** allow each client only the grant types, response types, response modes, and scopes it actually needs, validated at the authorization server.

**Why:** Client-chosen protocol parameters on a permissive endpoint are the raw material of downgrade and confusion attacks; removing the choice removes the class.

**Detect:** grep client registrations for `grant_types`, `response_types`, `response_modes`, and wildcard `scopes`.

**References:** OWASP ASVS v5.0 V10.4.11, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 9700 (OAuth 2.0 Security BCP)

# Phishing-Resistant MFA

**SHOULD** require phishing-resistant authenticators, such as passkeys or hardware tokens, for privileged and administrative accounts.

**Why:** Passwords, SMS codes, and push approvals are phishable and remain the primary initial-access route to account takeover.

**Detect:** grep identity-provider policy as code for `sms`, `voice`, `push`, and `password` still enabled for admin groups, and for `webauthn`/`fido2` as optional rather than required.

**References:** OWASP Multifactor Authentication Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html, OWASP Passkey Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Passkey_Security_Cheat_Sheet.html

# Phishing-Resistant Publisher MFA

**MUST** require phishing-resistant authentication for accounts that can publish artifacts or change package ownership.

**Why:** One-time codes are relayed through a proxy page in real time, so a phished maintainer still hands over a valid code. Hardware-bound credentials do not transfer.

**Detect:** IdP and registry policy: publish-capable accounts enforce FIDO2/WebAuthn rather than TOTP or SMS.

**References:** Filippo Valsorda: compromise survey, https://words.filippo.io/dispatches/compromise-survey/

# Push Bombing Defense

**MUST** rate-limit push authentication prompts and require number or context matching so repeated approvals cannot be fatigued through.

**Why:** An approve-anything prompt under volume turns the user into the attacker's second factor, one reflexive tap at a time.

**Detect:** grep push MFA config for number matching and a prompt rate limit (`number_matching`, `push_rate_limit`, `max_attempts`).

**References:** OWASP ASVS v5.0 V6.6.4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B

# Push-Token Binding & Rotation

**MUST** bind APNs/FCM device tokens to the authenticated user+device and invalidate on logout/account change; never accept a token from an unauthenticated registration.

**Why:** Unbound push tokens let an attacker register their device against someone's account (token swap) and receive their notifications — 2FA codes, account alerts, private messages.

**Detect:** grep push registration endpoints for auth requirement and user+device binding; check logout path unregisters tokens; flag token storage without account association or per-install rotation.

**References:** OWASP MASVS-AUTH, APNs/FCM security guidance, push-token hijacking CVEs

# Reauth Before Auth Change

**MUST** require full re-authentication before changing the email, phone, MFA enrolment, or recovery settings on an account.

**Why:** Those attributes are the account's recovery keys, so a hijacked session that can edit them converts temporary access into permanent ownership.

**Detect:** grep account-update handlers for those fields and check for a password or step-up check on the same path.

**References:** OWASP ASVS v5.0 V7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x16-V7-Session-Management.md, CWE-620

# Refresh Tokens

**SHOULD** store refresh tokens server-side with rotation on every use, invalidating the previous token after exchange.

**Why:** A static, non-rotating refresh token lets an attacker who steals one mint fresh access tokens forever, even after the user logs in again.

**Detect:** grep refresh endpoints for missing rotation (`old token reused`), refresh tokens kept in localStorage, no `revoked`/`rotated_at` column in token store.

**References:** OWASP A02:2021, CWE-523, RFC 6749 §6, RFC 9700 §4.14

# Retire Legacy OAuth Grants

**MUST** disable the implicit and resource-owner-password grants at the authorization server for every client, not only in individual client configuration.

**Why:** A per-client opt-out rots: any client added later inherits the dangerous flow because the capability still exists at the authority.

**Detect:** grep authorization-server config for `response_type=token`, `grant_types: [password]`, `allow_implicit`, `enable_ropc`.

**References:** OWASP ASVS v5.0 V10.4.4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 9700 (OAuth 2.0 Security BCP)

# Revocation as Best Effort

**MUST NOT** depend on revocation lookups as the primary control for a credential; cap lifetimes, reissue automatically, and treat revocation as a supplement.

**Why:** Revocation infrastructure fails open in practice — offline nodes, soft-fail responders, stale CRLs — so lifetime caps carry the real risk reduction.

**Detect:** grep credential lifetime settings (`expires_in`, `max_age`, `--ttl`) and every `ocsp`/`crl` reference; long lifetimes with only a revocation lookup is the finding.

**References:** RFC 9325 §7.5, https://www.rfc-editor.org/rfc/rfc9325.html, NIST SP 800-57 Part 1

# SAML Assertion Single Use

**MUST** process each SAML assertion at most once, rejecting any assertion ID already consumed within the assertion's validity window.

**Why:** Accepting an unsigned assertion is total authentication bypass, and a signed assertion replayed inside its window is the same bypass on a delay.

**Detect:** grep SAML validation for an assertion-ID replay cache keyed by `(issuer, assertion_id)` with retention at least the assertion lifetime.

**References:** OWASP ASVS v5.0 V6.8.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md

# SAML assertion validation and XML signature wrapping

**MUST** validate the SAML assertion's signature against a pinned IdP certificate and verify the signed element is the one consumed, rejecting wrapping attacks.

**Why:** XML signature wrapping lets an attacker embed a validly-signed assertion inside a malicious one, tricking the SP into trusting attacker-controlled attributes.

**Detect:** grep SAML consumer for missing `signature` validation, no certificate pinning, parsing `Assertion` without checking `Signature` reference URI, `xmldsig` verification skipped.

**References:** CWE-347, OWASP A02:2021, CVE-2017-11427, SAML Security BCP §4.1.5

# Sender-Constrained Tokens

**SHOULD** bind access tokens to the client that requested them, using proof-of-possession or mTLS, wherever bearer theft is in scope.

**Why:** A pure bearer token is usable by anyone who copies it, from anywhere, for its whole lifetime.

**Detect:** grep token issuance and client config for `DPoP`, `cnf` claim, or mTLS binding; flag tokens stored in `localStorage` or `sessionStorage`.

**References:** OWASP OAuth 2.0 Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html

# Session-Bound Key Verification

**MUST** bind a presented certificate or key to the session it was negotiated for, and terminate the channel when the binding does not match.

**Why:** A valid certificate that is not tied to this session admits any holder of any valid certificate as a man in the middle.

**Detect:** grep for fingerprint or channel-binding comparison in the handshake (`sdp fingerprint`, `tls-server-end-point`, `ExportKeyingMaterial`); its absence means the key is trusted on chain validity alone.

**References:** OWASP ASVS v5.0 V17.2.8, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x26-V17-WebRTC.md, RFC 5705 (keying material exporters), CWE-295

# Session Context Binding

**SHOULD** record client context at session establishment and treat a significant mid-session change as a step-up signal, never as proof of identity.

**Why:** A stolen session cookie replays from a different network and device. Comparing context catches the reuse, while treating a matching context as authentication would let an attacker who copied it through.

**Detect:** grep session creation for stored client context fields (address, user agent, locale) and for a comparison on later requests; flag comparisons that grant access on match.

**References:** OWASP Cookie Theft Mitigation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Cookie_Theft_Mitigation_Cheat_Sheet.html, NIST SP 800-63B session binding guidance

# Session Fixation

**MUST** regenerate the session identifier immediately after any successful authentication or privilege change.

**Why:** If the session ID survives login, an attacker who planted one earlier rides the victim's now-authenticated session undetected.

**Detect:** grep login handlers for missing `session.regenerate`, `session_id` unchanged post-auth, `secure`/`httpOnly` cookie flags absent on session cookies.

**References:** OWASP A07:2021, CWE-384, OWASP Session Management Cheat Sheet

# Session invalidation on credential change and logout

**MUST** invalidate all existing sessions and tokens when a user changes their password, email, or MFA settings.

**Why:** If old sessions survive a credential change, an attacker's stolen session stays alive after the victim rotates their password in response to a breach.

**Detect:** grep password/email-change handlers for missing `invalidate_all_sessions`, `revoke_tokens`, or session-store purge; old JWTs still accepted post-change.

**References:** NIST SP 800-63B §5.1.1.2, OWASP A07:2021, CWE-613, RFC 7009

# Session Lifetime Limits

**MUST** enforce both an idle timeout and an absolute maximum session lifetime, requiring re-authentication when either is exceeded.

**Why:** An idle timeout alone lets a continuously refreshed session live forever, while an absolute cap alone leaves an unattended terminal authenticated. A stolen cookie only needs to be kept warm.

**Detect:** grep session and cookie configuration for `maxAge`, `idleTimeout`, `expires`, and refresh-token lifetime; flag sessions with no absolute cap or refresh that extends past it.

**References:** OWASP Session Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html, NIST SP 800-63B reauthentication requirements

# Session Visibility

**MUST** give users a list of their active sessions with per-session termination, and administrators the same per-user and global view.

**Why:** A session the user cannot see is one they cannot revoke, so a stolen cookie stays live until expiry with no visible trace.

**Detect:** open the account security page and the admin session table and check both list device, time, and a revoke action.

**References:** OWASP ASVS v5.0 V7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x16-V7-Session-Management.md

# Trusted Display for Signing

**MUST** include the display path that shows a user what they approve inside the trusted boundary, or the signature attests only to what a compromised host chose to show.

**Why:** Certifying the signing device while the adjacent screen is attacker-controlled produces valid signatures on transactions the user never saw.

**Detect:** judgment: the approval flow — which machine renders the transaction details, and whether it is inside the evaluated boundary

**References:** Anderson, Security Engineering 1st ed., ch.23, https://www.cl.cam.ac.uk/~rja14/book.html

# Social Login Account-Linking Takeover

**SHOULD NOT** auto-link a social identity (Google/GitHub) to an existing local account by matching email alone without verifying the user controls that account.

**Why:** An attacker registers a social account using the victim's email, then logs in and gets auto-linked to the victim's existing profile with full access.

**Detect:** grep OAuth callback for auto-link on `email` match without prior password/MFA confirmation, missing `account_linking` verification step, `findOrCreate` by email.

**References:** OWASP A07:2021, CWE-287, CWE-346, Auth0 Account Linking Vulnerability advisory

# SSO Global Logout

**MUST** terminate the session at every relying party when logout happens at the identity provider.

**Why:** A half-logout leaves the identity provider's session alive, so returning to the portal re-enters every application without authentication.

**Detect:** grep for back-channel or front-channel logout endpoints and for per-app session termination, then test logout-then-reenter.

**References:** OWASP WSTG Session Management Testing, https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/

# Step-Up Authentication

**MUST** require fresh re-authentication for high-consequence operations such as payments, credential changes, and privilege grants.

**Why:** A live session proves someone logged in earlier, not that the account owner is the person performing this action now.

**Detect:** grep the money-change, email-change, password-change, and role-grant handlers for a `reauth`, `auth_time`, `amr`, or MFA-challenge check; absence is the finding.

**References:** OWASP Transaction Authorization Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html, NIST SP 800-63B, https://pages.nist.gov/800-63-3/sp800-63b.html

# Strong Client Authentication

**MUST** authenticate confidential clients with proof-of-possession methods such as mutual TLS or signed assertions, not shared client secrets.

**Why:** Shared secrets leak through config, logs, and support tickets, and knowledge alone cannot show that the caller is the client it claims to be.

**Detect:** grep OAuth client config and token requests for `client_secret` where `private_key_jwt` or `tls_client_auth` is available.

**References:** OWASP ASVS v5.0 V10.4.16, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 8705 (mTLS client auth)

# Timing Attacks

**MUST** compare secrets (password hashes, tokens, API keys) using constant-time comparison functions.

**Why:** Early-exit string comparison leaks byte-by-byte match timing, letting a remote attacker reconstruct valid secrets through repeated requests.

**Detect:** grep for `==` or `===` comparing hashes/tokens instead of `hmac.compare_digest`, `crypto.timingSafeEqual`, or `MessageDigest.isEqual`.

**References:** CWE-208, CWE-203, OWASP A02:2021, NIST SP 800-53 SC-8

# Token Entropy and Lifetime

**MUST** size token entropy and lifetime together, so a token under 128 bits of entropy is rate-limited and expires within minutes.

**Why:** Entropy and validity multiply into brute-force feasibility; a slightly weak identifier that expires in minutes is a different risk from one valid for a week.

**Detect:** grep token generation and its TTL side by side (`secrets.token_hex(8)`, `uuid1`, `random`) against `expires_in`, `max_age`, and session timeout config.

**References:** OWASP WSTG Session Management Schema, https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/06-Session_Management/01-Session_Management_Schema.md

# Token Payload Confidentiality

**MUST NOT** put sensitive data or personal identifiers in client-readable token payloads; a signature proves origin, it does not hide content.

**Why:** Tokens are readable by the client and by every system they pass through, and encoded payloads get logged and cached like any other header.

**Detect:** grep token signing call sites for claims carrying `email`, `phone`, `ssn`, `address`, `dob`, `role` lists, or internal identifiers.

**References:** OWASP JSON Web Token Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html

# Token Replay Prevention

**MUST** give every single-use token a unique identifier and reject a second presentation of an identifier already consumed.

**Why:** Without a unique identifier a token replays indefinitely inside its validity window, and revocation cannot tell the stolen copy from the original. A reuse cache is what makes single use enforceable.

**Detect:** grep issuance of reset, verification, invitation and refresh tokens for a `jti`/nonce claim plus a store that records consumed identifiers; absence of either, or a record that is written after the action instead of atomically with it, is the finding.

**References:** OWASP JSON Web Token Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html, RFC 7519 §4.1.7 (jti)

# Token Revocation & Logout Invalidation

**MAY** rely on short expiry alone for stateless tokens, but MUST provide a revocation list or denylist for high-value sessions where immediate logout is required.

**Why:** A pure stateless JWT cannot be logged out; a stolen token keeps working until expiry even after the user hits logout.

**Detect:** grep logout handler for missing token blacklist/`jti` denylist, no `/revoke` endpoint, Redis denylist absent, logout only clears client cookie.

**References:** RFC 7009 §2.1 (revocation request), OWASP A02:2021, NIST SP 800-53 SC-23

# Token Type Verification

**MUST** verify a token's declared type and required event claims before acting on it, including logout and error tokens.

**Why:** Without a type check any signed token is accepted anywhere, so a re-purposed identity token becomes a logout trigger or a session mint.

**Detect:** grep for `typ` and `events` claim validation in token consumers; a logout endpoint that accepts any well-signed JWT is the finding.

**References:** OWASP ASVS v5.0 V10.5.5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 8417 (Security Event Tokens), CWE-290

# Trusted Time for TOTP

**MUST** validate time-based codes against a trusted server time source, never a client-supplied or unsynchronized clock.

**Why:** Reading the clock from the request turns the validity window into attacker-controlled slack that keeps a stolen code alive.

**Detect:** grep TOTP verification for a time value taken from the request body or headers instead of the server clock.

**References:** OWASP ASVS v5.0 V6.5.8, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, RFC 6238 (TOTP)

# Uniform Failure Responses

**MUST** complete the expensive security check before returning a failure, so that rejection timing does not reveal whether the account, token, or key exists.

**Why:** A fast 'not found' and a slow 'wrong secret' are the same oracle in different units; attackers measure microseconds, not messages.

**Detect:** grep verification handlers for an early return before the hash comparison or the key lookup (unknown user, malformed token, missing key), and for per-cause error strings; the not-found path that skips the expensive check is the finding.

**References:** Lucky Thirteen timing analysis, https://www.imperialviolet.org/2013/02/04/luckythirteen.html, CWE-203 Observable Discrepancy

# Verify Signature Before Parsing

**MUST** verify the signature or MAC over a token or message before parsing its contents or making any decision from them.

**Why:** Parsing first runs attacker-chosen bytes through a parser with elevated trust and leaks oracle behaviour for tokens that will be rejected anyway.

**Detect:** grep decode-then-verify order: `jwt.decode(..., verify=False)`, `verify_signature: false`, claims read before `verify(`/`hmac.compare_digest`, and `json.loads` on a webhook body before its HMAC check.

**References:** OWASP JSON Web Token Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html, Critical vulnerabilities in JSON Web Token libraries, https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/

# Weakest Auth Assumption

**MUST** assume the weakest authentication method when an identity provider omits strength or recency metadata, and document that fallback.

**Why:** Missing metadata resolves to the hoped-for value by default, so an upstream that cannot report MFA silently grants access reserved for MFA sessions.

**Detect:** grep `acr`, `amr`, and `auth_time` handling for branches that treat an absent claim as sufficient.

**References:** OWASP ASVS v5.0 V6.8.4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, OpenID Connect Core §2

# Workload Identity / IRSA Audience and Claim Validation Gaps

**MUST** validate the audience (`aud`) and issuer (`iss`) claims on every federated workload token and scope each identity to the single service it is meant to reach.

**Why:** If a token minted for service A is accepted by service B without audience checks, any workload holding the weaker token can impersonate the stronger one — cross-service confusion that bypasses IAM entirely.

**Detect:** In STS `AssumeRoleWithWebIdentity` trust policies, check `Condition.StringEquals` on `token.actions.githubusercontent.com:aud` and `:sub` (repo + ref, not just `repo:*`). For SPIFFE/IRSA reviews, look for trust policies matching only the issuer URL with no audience or subject constraints, and app code that skips `aud` verification in JWT libraries (`verify_aud=False`).

**Bad:**
```json
"Condition": {"StringEquals": {
  "token.actions.githubusercontent.com:iss": "https://token.actions.githubusercontent.com"}}
```

**Good:**
```json
"Condition": {"StringEquals": {
  "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
  "token.actions.githubusercontent.com:sub": "repo:acme/deploy:ref:refs/heads/main"}}
```

**References:** CWE-287, OWASP ASVS 3.5, AWS IRSA trust policy docs, SPIFFE threat model

