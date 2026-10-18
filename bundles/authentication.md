# authentication — full checklist (33 items)

Identity, credentials, session lifecycle.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [authentication](../categories/authentication.md) · index: [SKILL.md](../SKILL.md)

# Account Enumeration

**SHOULD NOT** reveal whether an account exists through differing responses, timing, or error messages on login, registration, and password-reset endpoints.

**Why:** Distinct "user not found" vs "wrong password" responses let attackers build a valid username list for targeted phishing or credential stuffing.

**Detect:** grep for `user not found`, `email already exists`, `invalid username` strings; differing HTTP status codes (404 vs 401) on auth endpoints.

**References:** OWASP A07:2021, CWE-204, CWE-203, NIST SP 800-63B §5.2.3

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Account recovery and password-reset flow security (tokens, helpdesk takeover)

**MUST NOT** allow helpdesk or support staff to reset a user's password without a verified second channel (e.g. confirmed email + MFA challenge) and full audit logging.

**Why:** Social-engineering the helpdesk is the cheapest path to takeover; a single unverified reset request bypasses every other control.

**Detect:** grep support/reset tooling for missing identity-verification step, no `audit_log` on manual resets, reset-by-username-only admin endpoints without MFA gate.

**References:** NIST SP 800-63B §5.1.1.2, CWE-287, OWASP A07:2021, CWE-354

---

**Part of:** [authentication](../categories/authentication.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Anomalous Authentication Detection (impossible travel, rare UA/IP)

**SHOULD** monitor for impossible-travel, rare user-agent, and unfamiliar-IP login patterns and trigger step-up MFA or alerting on anomalies.

**Why:** Without anomaly detection, an attacker logging in from a foreign IP with a stolen credential looks identical to the legitimate user and passes silently.

**Detect:** grep auth pipeline for absent `impossible_travel`, `geoip`, `ua_fingerprint` checks; no step-up MFA on new-device login; no alerting on geo-velocity anomalies.

**References:** NIST SP 800-63B §7.2, OWASP A07:2021, CIS Control 8.3, MITRE ATT&CK T1078

---

**Part of:** [authentication](../categories/authentication.md) · [observability](../categories/observability.md) · [backend](../domains/backend.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

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

---

**Part of:** [authentication](../categories/authentication.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# ArgoCD-Specific: Default Admin Password, JWT Signing Key, Webhook Auth

**MUST** replace ArgoCD's default `admin` password, set a unique `server.signingkey`, and authenticate all webhook receivers before exposing the API.

**Why:** ArgoCD ships with a known default admin and auto-generated signing key; an attacker who reaches the UI or webhook endpoint gains cluster-wide deploy control.

**Detect:** check `argocd-secret` for unchanged `admin.password`, default `server.signingkey`, webhook receivers without `secret`/HMAC verification, `admin.enabled: true` in values.

**References:** ArgoCD Security Guide, CWE-1188, CVE-2023-22482, OWASP A05:2021

---

**Part of:** [authentication](../categories/authentication.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [deployment-release](../categories/deployment-release.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Auto-Mounted Service Account Tokens in Pods That Don't Need the API

**SHOULD** set `automountServiceAccountToken: false` on pods and serviceaccounts that never call the Kubernetes API.

**Why:** An unnecessary mounted token is a standing credential an attacker with any file-read bug can use against the API server.

**Detect:** Pod specs without `automountServiceAccountToken: false`; mounted path `/var/run/secrets/kubernetes.io/serviceaccount` in non-API workloads.

**References:** CIS K8s 5.1.5, CWE-522, OWASP K8s PS1, NIST SP 800-190 5.2

---

**Part of:** [authentication](../categories/authentication.md) · [containers-k8s](../categories/containers-k8s.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Breached & Common Password Blocklist

**SHOULD** reject new or changed passwords found in known-breached or common-password lists (e.g. HaveIBeenPwned k-anonymity API).

**Why:** Reusing a password exposed in a prior breach means credential-stuffing bots will try it against your service within hours of exposure.

**Detect:** grep password policy code for absent blocklist/pwned-password check, no `k-anonymity`/`pwnedPasswords` call, min-length-only policy with no composition rules.

**References:** NIST SP 800-63B §5.1.1.2, OWASP A07:2021, CWE-521, NCSC Pwned Passwords guidance

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Brute Force Protection

**MUST** rate-limit and lock out repeated failed authentication attempts per account and per source IP.

**Why:** Without throttling, automated credential-stuffing and dictionary attacks can try millions of passwords against a login form unimpeded.

**Detect:** grep login endpoints for missing `rate_limit`, `attempt_count`, `lockout` logic; no backoff on 401 responses; unlimited POST to `/login`.

**References:** OWASP A07:2021, CWE-307, NIST SP 800-63B §5.2.2, CIS Control 6.2

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Cookie Flags: Secure, HttpOnly, SameSite

**MUST** set `Secure`, `HttpOnly`, and `SameSite=Lax` (or `Strict`) on every session cookie issued by the application.

**Why:** Missing flags let cookies leak over HTTP, be read by injected scripts, or ride cross-site requests, enabling session hijacking and CSRF.

**Detect:** grep `Set-Cookie`, `res.cookie(`, `document.cookie=`; inspect ingress/Envoy/nginx cookie-rewrite annotations for stripped flags.

**References:** RFC 6265bis, OWASP Session Management Cheat Sheet, CWE-1004, CWE-1275

---

**Part of:** [authentication](../categories/authentication.md) · [web-client-security](../categories/web-client-security.md) · [backend](../domains/backend.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)

# Credential Access Detection (keylogging, token theft, credential dumping patterns)

**SHOULD** detect credential harvesting: LSASS dumps, keylogging hooks, OAuth token replay, metadata-service credential scraping.

**Why:** Stolen credentials are the leading initial-access vector; catching the theft step stops breaches identity controls alone miss.

**Detect:** grep detection content for `T1003`, `lsass`, `mimikatz`, `secretsdump`, alerts on `169.254.169.254` access, token-replay rules.

**References:** MITRE ATT&CK TA0006/T1003, NIST SP 800-63B, CWE-522, GuardDuty credential-access detections

---

**Part of:** [authentication](../categories/authentication.md) · [observability](../categories/observability.md) · [backend](../domains/backend.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Dedicated Service Accounts per Workload

**SHOULD NOT** run workloads under the `default` Kubernetes service account; each workload **SHOULD** declare a dedicated `serviceAccountName` scoped to exactly the API access it needs.

**Why:** The default SA is shared by every pod that doesn't override it, so any IAM or RBAC grant made for one workload silently applies to all of them, and audit logs cannot attribute an API call to the workload that made it. Dedicated identities are the prerequisite for least-privilege cloud IAM (IRSA/workload identity), per-workload RBAC, and meaningful `automountServiceAccountToken` control.

**Detect:** `spec.serviceAccountName` absent or `default` in Deployments/Pods/StatefulSets; `default` SA bound to any Role/ClusterRole beyond the baseline; IAM roles (e.g. EKS IRSA annotations) attached to workloads running as `default`. Policy engines: Kyverno `require-dedicated-service-accounts` / a equivalent admission rule.

**References:** CIS Kubernetes 5.1.4 (minimize default SA admission), K8s service accounts docs, EKS IRSA / GKE Workload Identity guidance, aquasecurity/trivy-checks KSV010–KSV012

---

**Part of:** [authentication](../categories/authentication.md) · [containers-k8s](../categories/containers-k8s.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Default & Weak Credentials in Shipped Software

**MUST NOT** ship software with default usernames/passwords or demo accounts enabled in production; force credential change on first login.

**Why:** Scanners sweep the internet for known default credentials (admin/admin, root/toor) and compromise unmodified deployments within minutes of exposure.

**Detect:** grep configs/seed files for `admin:admin`, `changeme`, `default_password`, hardcoded credentials in Docker images, demo accounts in fixtures shipped to prod.

**References:** CWE-1188, OWASP A05:2021, CIS Control 5.4, NIST SP 800-118

---

**Part of:** [authentication](../categories/authentication.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Insufficient Randomness for Tokens and IDs

**MUST** generate session tokens, password resets, API keys, and invite codes from a cryptographically secure RNG (`secrets`, `crypto.randomBytes`, `SecureRandom`), never `random`/`Math.random`/sequential IDs.

**Why:** Predictable randomness lets attackers guess reset links and session tokens, taking over accounts without ever touching the password.

**Detect:** `Math.random()`, Python `random.` for tokens, `uuid1`/sequential IDs in auth flows, `rand()` in token generation code.

**References:** OWASP ASVS V3.2.2, CWE-330, NIST SP 800-90A

---

**Part of:** [authentication](../categories/authentication.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# JWT Algorithm Confusion / alg=none / Unverified Signatures

**MUST NOT** accept `alg: none` or allow the token header to select the verification algorithm; pin the expected algorithm server-side.

**Why:** If the verifier trusts the header's `alg`, an attacker switches to `none` or swaps RS256→HS256 to forge unsigned or HMAC-forged tokens.

**Detect:** grep for `jwt.decode` without `algorithms=[...]`, `alg.*none`, dynamic algorithm selection from token header, missing algorithm allowlist.

**References:** CWE-347, OWASP A02:2021, RFC 8725 §3.1, Auth0 JWT Algorithm Confusion advisory

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# JWT Audience/Issuer Validation & kid/JWKS Abuse

**MUST** verify `iss` and `aud` claims against an explicit allowlist and pin `kid` to a trusted JWKS entry before accepting a token.

**Why:** Unpinned `kid` lets an attacker point the verifier at a rogue JWKS or reuse a token minted for a different service as valid here.

**Detect:** grep verifier config for missing `issuer`/`audience` checks, `jwks_uri` fetched without TLS pinning, `kid` resolved dynamically with no allowlist.

**References:** RFC 8725 §3.3-3.4, CWE-345, OWASP A02:2021, OIDC Core §3.1.3.7

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# JWT Expiry

**MUST** set short-lived access tokens (15 minutes or less) with an explicit `exp` claim that the verifier rejects when past.

**Why:** A stolen or leaked long-lived JWT stays usable indefinitely, giving an attacker persistent API access with no way to expire out.

**Detect:** grep for `expiresIn`, `exp:` with values like `86400`, `7d`, `never`; missing `exp` claim in token payloads or verifier code.

**References:** OWASP A02:2021, CWE-613, RFC 7519 §4.1.4, NIST SP 800-107

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Service Mesh Permissive mTLS and Direct-Pod-IP Bypass

**MUST NOT** treat permissive-mode mTLS as an access-control boundary; enforce STRICT mTLS per namespace and pair it with NetworkPolicies that block plaintext direct-pod-IP access.

**Why:** Permissive mode accepts both meshed (mTLS) and raw plaintext traffic, so an attacker inside the cluster — or a compromised pod — simply bypasses the sidecar by dialing the pod IP on the plaintext port, and any authorization policy keyed on peer identity silently fails open for that path.

**Detect:** Check PeerAuthentication `mtls.mode: PERMISSIVE` (or mesh-wide default), AuthorizationPolicies that allow when principal is empty, CNI/network policies that don't restrict pod ports to sidecar traffic only, and services reachable on `podIP:port` in egress tests. Verify destination rules route through the service, not resolved pod endpoints.

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

**References:** Istio security docs (permissive mTLS caveats), OWASP Kubernetes Top 10, CWE-300

---

**Part of:** [authentication](../categories/authentication.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# MFA

**SHOULD** require a second factor for all administrative and remote-access accounts, enforced server-side after primary auth.

**Why:** Password-only admin access means one phished or breached credential grants full control with no second barrier.

**Detect:** grep admin/SSH/RDP login paths for missing `mfa`/`totp`/`webauthn` checks, MFA toggle client-side only, `mfa_enabled` field absent in user model.

**References:** NIST SP 800-63B §5.1, OWASP A07:2021, CWE-308, CIS Control 6.3

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Missing Authentication Middleware / Default-Deny Routing

**MUST** default-deny: every route requires authentication unless explicitly marked public via an allowlist.

**Why:** Route-by-route opt-in means any forgotten or newly added endpoint ships unauthenticated, exposing internal APIs to the internet.

**Detect:** grep router config for missing global auth middleware, routes without `@authenticated`/`requireAuth`, `public: true` as default, admin endpoints outside auth filter chain.

**References:** OWASP A01:2021, CWE-306, NIST SP 800-53 AC-3, CIS Control 4.5

---

**Part of:** [authentication](../categories/authentication.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Non-Human Identity Governance (service accounts, machine creds inventoried and scoped)

**MUST** inventory every service account, API key, and machine credential with an owner, least-privilege scope, and expiry.

**Why:** Machine identities outnumber humans 50:1 and are rarely reviewed; orphaned service accounts become attackers' favorite door.

**Detect:** grep `service_account`, `api_key`, `client_secret` inventories, orphaned-credential reports, workload-identity configs.

**References:** NIST SP 800-63B, CIS Control 6, OWASP Non-Human Identities Top 10, CSA NHI guidance

---

**Part of:** [authentication](../categories/authentication.md) · [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# OAuth 2.0

**MUST** validate the `state` parameter on every authorization callback and use PKCE for public clients.

**Why:** Missing state/PKCE enables CSRF and authorization-code interception, letting an attacker bind a victim's code to their own session.

**Detect:** grep callback handlers for absent `state` checks, `response_type=token` in public clients, missing `code_verifier`/`code_challenge` in auth URL construction.

**References:** OWASP A01:2021, CWE-352, RFC 6749 §10.12, OAuth Security BCP §7

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# OAuth Third-Party Scope Minimization

**MUST** request the minimum OAuth scopes from identity providers and audit granted-scope drift for third-party app integrations.

**Why:** Over-scoped integrations (`offline_access`, full mailbox, full repo) turn a third-party breach into your breach; scopes granted years ago silently persist.

**Detect:** review OAuth app registrations for scopes beyond current feature needs; grep client code for scope strings vs actual API calls used; check admin consent logs for over-granted apps.

**References:** OAuth 2.0 BCP scope guidance, OWASP API Security (insufficient scope), Microsoft/Google admin consent audit docs

---

**Part of:** [authentication](../categories/authentication.md) · [third-party-integrations](../categories/third-party-integrations.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# OpenID Connect

**MUST** validate the ID token's signature, `iss`, `aud`, and `nonce` before trusting any identity claim.

**Why:** Skipping ID token validation lets an attacker replay a token from another client or provider and be accepted as a different user.

**Detect:** grep for `id_token` usage without `verify`/`validate` calls, missing `nonce` in auth request, `aud` not checked against client ID.

**References:** OIDC Core §3.1.3.7, CWE-347, OWASP A02:2021, NIST SP 800-63B

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Password Reset Flow Security

**MUST** issue single-use, high-entropy reset tokens with short expiry (≤15 min) over HTTPS, invalidated on use or password change.

**Why:** Reusable or long-lived reset tokens let an attacker who intercepts one take over an account at leisure, bypassing the password entirely.

**Detect:** grep reset handlers for tokens without `exp`/`used` flags, tokens in URL query strings logged by proxies, `md5(email)` as token, no rate limit on `/forgot-password`.

**References:** OWASP A07:2021, CWE-640, CWE-639, NIST SP 800-63B §5.1.1.2

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Push-Token Binding & Rotation

**MUST** bind APNs/FCM device tokens to the authenticated user+device and invalidate on logout/account change; never accept a token from an unauthenticated registration.

**Why:** Unbound push tokens let an attacker register their device against someone's account (token swap) and receive their notifications — 2FA codes, account alerts, private messages.

**Detect:** grep push registration endpoints for auth requirement and user+device binding; check logout path unregisters tokens; flag token storage without account association or per-install rotation.

**References:** OWASP MASVS-AUTH, APNs/FCM security guidance, push-token hijacking CVEs

---

**Part of:** [authentication](../categories/authentication.md) · [mobile](../categories/mobile.md) · [backend](../domains/backend.md) · [mobile](../domains/mobile.md) · [SKILL.md](../SKILL.md)

# Refresh Tokens

**SHOULD** store refresh tokens server-side with rotation on every use, invalidating the previous token after exchange.

**Why:** A static, non-rotating refresh token lets an attacker who steals one mint fresh access tokens forever, even after the user logs in again.

**Detect:** grep refresh endpoints for missing rotation (`old token reused`), refresh tokens kept in localStorage, no `revoked`/`rotated_at` column in token store.

**References:** OWASP A02:2021, CWE-523, RFC 6749 §6, OAuth Security BCP §4.13

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# SAML assertion validation and XML signature wrapping

**MUST** validate the SAML assertion's signature against a pinned IdP certificate and verify the signed element is the one consumed, rejecting wrapping attacks.

**Why:** XML signature wrapping lets an attacker embed a validly-signed assertion inside a malicious one, tricking the SP into trusting attacker-controlled attributes.

**Detect:** grep SAML consumer for missing `signature` validation, no certificate pinning, parsing `Assertion` without checking `Signature` reference URI, `xmldsig` verification skipped.

**References:** CWE-347, OWASP A02:2021, CVE-2017-11427, SAML Security BCP §4.1.5

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Session Fixation

**MUST** regenerate the session identifier immediately after any successful authentication or privilege change.

**Why:** If the session ID survives login, an attacker who planted one earlier rides the victim's now-authenticated session undetected.

**Detect:** grep login handlers for missing `session.regenerate`, `session_id` unchanged post-auth, `secure`/`httpOnly` cookie flags absent on session cookies.

**References:** OWASP A07:2021, CWE-384, NIST SP 800-53 SC-25, OWASP Session Management Cheat Sheet

---

**Part of:** [authentication](../categories/authentication.md) · [web-client-security](../categories/web-client-security.md) · [backend](../domains/backend.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)

# Session invalidation on credential change and logout

**MUST** invalidate all existing sessions and tokens when a user changes their password, email, or MFA settings.

**Why:** If old sessions survive a credential change, an attacker's stolen session stays alive after the victim rotates their password in response to a breach.

**Detect:** grep password/email-change handlers for missing `invalidate_all_sessions`, `revoke_tokens`, or session-store purge; old JWTs still accepted post-change.

**References:** NIST SP 800-63B §5.1.1.2, OWASP A07:2021, CWE-613, RFC 7009

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Social Login Account-Linking Takeover

**SHOULD NOT** auto-link a social identity (Google/GitHub) to an existing local account by matching email alone without verifying the user controls that account.

**Why:** An attacker registers a social account using the victim's email, then logs in and gets auto-linked to the victim's existing profile with full access.

**Detect:** grep OAuth callback for auto-link on `email` match without prior password/MFA confirmation, missing `account_linking` verification step, `findOrCreate` by email.

**References:** OWASP A07:2021, CWE-287, CWE-346, Auth0 Account Linking Vulnerability advisory

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Timing Attacks

**MUST** compare secrets (password hashes, tokens, API keys) using constant-time comparison functions.

**Why:** Early-exit string comparison leaks byte-by-byte match timing, letting a remote attacker reconstruct valid secrets through repeated requests.

**Detect:** grep for `==` or `===` comparing hashes/tokens instead of `hmac.compare_digest`, `crypto.timingSafeEqual`, or `MessageDigest.isEqual`.

**References:** CWE-208, CWE-203, OWASP A02:2021, NIST SP 800-53 SC-8

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Token Revocation & Logout Invalidation

**MAY** rely on short expiry alone for stateless tokens, but MUST provide a revocation list or denylist for high-value sessions where immediate logout is required.

**Why:** A pure stateless JWT cannot be logged out; a stolen token keeps working until expiry even after the user hits logout.

**Detect:** grep logout handler for missing token blacklist/`jti` denylist, no `/revoke` endpoint, Redis denylist absent, logout only clears client cookie.

**References:** RFC 7009, RFC 8725 §4.1, OWASP A02:2021, NIST SP 800-53 SC-23

---

**Part of:** [api-design](../categories/api-design.md) · [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

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

**References:** CWE-287, OWASP ASVS 3.5, AWS IRSA trust policy docs, SPIFFE/SPIFFI threat model

---

**Part of:** [authentication](../categories/authentication.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

