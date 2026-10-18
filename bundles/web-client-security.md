# web-client-security — full checklist (22 items)

Browser-side attack surface and defenses.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# XSS

**MUST NOT** Emit user-controlled data into HTML without context-aware escaping or raw/filter bypasses.

**Why:** Injected scripts run in victims' sessions, stealing cookies and acting as them.

**Detect:** `innerHTML`, `dangerouslySetInnerHTML`, `|safe`, `Markup(` fed by request data.

**References:** OWASP A03:2021, CWE-79, OWASP XSS Prevention Cheat Sheet

# CSRF

**MUST** Require a per-session token or origin check on every state-changing request.

**Why:** Without it, an attacker's page forges authenticated requests that change user state.

**Detect:** POST/PUT/DELETE routes lacking `csrf_protect`, `X-CSRF-Token`, `SameSite`; `csrf_exempt=True`.

**References:** OWASP A01:2021, CWE-352, OWASP CSRF Prevention Cheat Sheet

# CORS

**MUST NOT** Pair wildcard or reflected `Access-Control-Allow-Origin` with `Allow-Credentials: true`; whitelist trusted origins.

**Why:** Wildcard-plus-credentials lets any site read authenticated responses cross-origin.

**Detect:** `Allow-Origin: *`, `allow_origins=['*']`, `@CrossOrigin` with credentials, origin reflection.

**References:** OWASP A05:2021, CWE-942, MDN CORS credentials

# Clickjacking

**MUST** Send `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'` on authenticated pages.

**Why:** Invisible iframes overlay trusted buttons onto attacker pages for unintended clicks.

**Detect:** Missing `X-Frame-Options`/`frame-ancestors` in headers or middleware; `ALLOWALL` frame options.

**References:** OWASP A05:2021, CWE-1021, OWASP Clickjacking Defense Cheat Sheet

# Content Security Policy

**SHOULD** Deliver CSP with nonce/hash-based `script-src`; avoid `unsafe-inline` and `unsafe-eval`.

**Why:** A weak CSP removes the last defense once an injection flaw exists.

**Detect:** `unsafe-inline`, `unsafe-eval`, `script-src *` in CSP config; no `Content-Security-Policy` header.

**References:** OWASP A05:2021, CWE-1021, Google CSP Evaluator

# Security Headers

**MUST** Set HSTS, `X-Content-Type-Options: nosniff`, CSP, `Referrer-Policy`, and frame protection on every response.

**Why:** Missing headers leave transport, sniffing, and framing attacks unmitigated.

**Detect:** Config lacking `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`; nginx/ingress snippets absent.

**References:** OWASP A05:2021, CWE-693, securityheaders.com checklist

# Session Fixation

**MUST** regenerate the session identifier immediately after any successful authentication or privilege change.

**Why:** If the session ID survives login, an attacker who planted one earlier rides the victim's now-authenticated session undetected.

**Detect:** grep login handlers for missing `session.regenerate`, `session_id` unchanged post-auth, `secure`/`httpOnly` cookie flags absent on session cookies.

**References:** OWASP A07:2021, CWE-384, NIST SP 800-53 SC-25, OWASP Session Management Cheat Sheet

# Cache-Control Headers

**MUST** set explicit `Cache-Control` on every HTTP response; responses carrying auth tokens, PII, or CSRF values require `no-store`, never a bare default.

**Why:** Missing directives let browsers and proxies cache sensitive pages, exposing them via back-button or shared caches.

**Detect:** Responses lacking `Cache-Control`; `no-store` absent on login, account, admin routes; `public, max-age` on authenticated endpoints.

**References:** OWASP A04:2021, CWE-525, RFC 7234, NIST SP 800-63B 2.4.1.1

# Cookie Consent

**SHOULD** block non-essential cookies until explicit user consent is obtained, with granular category controls.

**Why:** Setting tracking cookies before consent violates ePrivacy Directive and GDPR, exposing sites to regulatory fines and user distrust.

**Detect:** grep for analytics/advertising cookie initialization before consent check; inspect `CookieConsent`, `googleAnalytics`, `fbq` calls preceding consent gate.

**References:** ePrivacy Directive Art. 5(3), GDPR Recital 30, IAB TCF 2.0

# Prototype Pollution

**MUST** validate and reject `__proto__`, `constructor`, and `prototype` keys before recursive merge or deep-set operations on untrusted input.

**Why:** Polluted `Object.prototype` leaks attacker-controlled properties app-wide, enabling XSS, auth bypass, and RCE in Node.

**Detect:** grep `__proto__`, `merge(`, `deepSet`, `set(obj, key` in utils; check lodash versions <4.17.21 and JSON.parse-then-merge flows.

**References:** CWE-1321, OWASP A08:2021, OWASP Prototype Pollution Prevention Cheat Sheet

# SSR Hydration XSS

**MUST NOT** interpolate user-controlled data into server-rendered HTML without context-aware escaping, especially inside script, attribute, or URL contexts.

**Why:** Unescaped state serialized into `__NEXT_DATA__` or inline scripts executes on every page load before hydration, bypassing CSP unsafe-inline allowances.

**Detect:** grep `dangerouslySetInnerHTML`, `innerHTML`, `JSON.stringify` inside `<script>`, `window.__INITIAL_STATE__`, unescaped `{{ }}` templates.

**References:** CWE-79, OWASP XSS Prevention Cheat Sheet, OWASP A03:2021

# CRLF / HTTP Header Injection & Response Splitting

**SHOULD NOT** Put user input into headers or redirect targets without rejecting CR/LF and `%0d%0a`.

**Why:** Injected line breaks forge headers or a whole second response, poisoning caches and sessions.

**Detect:** `set_header(..., user_value)`, `Location:`/`Set-Cookie` built from params without CRLF filtering.

**References:** CWE-113, CWE-93, PortSwigger HTTP Response Splitting

# Cookie Flags: Secure, HttpOnly, SameSite

**MUST** set `Secure`, `HttpOnly`, and `SameSite=Lax` (or `Strict`) on every session cookie issued by the application.

**Why:** Missing flags let cookies leak over HTTP, be read by injected scripts, or ride cross-site requests, enabling session hijacking and CSRF.

**Detect:** grep `Set-Cookie`, `res.cookie(`, `document.cookie=`; inspect ingress/Envoy/nginx cookie-rewrite annotations for stripped flags.

**References:** RFC 6265bis, OWASP Session Management Cheat Sheet, CWE-1004, CWE-1275

# Web Cache Poisoning & Cache Deception

**SHOULD NOT** cache responses that vary on unkeyed inputs like headers, query params, or cookies without declaring `Vary` or normalizing them.

**Why:** An attacker can get a poisoned response stored in CDN/proxy cache and served to every subsequent visitor of that URL.

**Detect:** grep `Vary:`, `cache-control: public`, unkeyed `X-Forwarded-*`/`Accept-Encoding` handling; CDN cache-key config ignoring query params.

**References:** CWE-421, PortSwigger Web Cache Poisoning research, OWASP A04:2021

# DNS Rebinding Against Internal Services

**SHOULD** validate `Host`/`Origin` headers and pin DNS resolution at connect time, so a fetch cannot be re-pointed from a public name to a private IP between lookups.

**Why:** A short-TTL record that flips from the attacker's server to `127.0.0.1` smuggles client requests past filters that only checked the name once — a classic route to admin panels and metadata services.

**Detect:** Handlers trusting `Host` for routing; SSRF allowlists validating DNS once instead of at connect; missing `Origin` checks on state-changing endpoints reachable from browsers. Test with a rebinding service like `rbndr.us`.

**Bad:**
```python
if urlparse(url).hostname.endswith(".example.com"):
    fetch(url)   # second lookup may now return 127.0.0.1
```

**Good:**
```python
ip = ipaddress.ip_address(socket.gethostbyname(host))
if not (ip.is_private or ip.is_loopback or ip.is_link_local):
    fetch(pinned_ip_url)   # connect vetted IP, keep SNI/Host pinned
```

**References:** CWE-350, OWASP SSRF Prevention Cheat Sheet, OWASP A10:2021

# Cross-Site WebSocket Hijacking (CSWSH)

**MUST** validate the `Origin` header on the WebSocket upgrade handshake against an explicit allowlist.

**Why:** WebSockets ignore CORS; any malicious site can open a socket using the victim's cookies and act as them in real time.

**Detect:** grep `ws://`, `wss://`, `upgrade` handlers, `onConnection` without origin checks; nginx `proxy_set_header Origin` passthrough config.

**References:** CWE-1385, OWASP A01:2021, RFC 6455 section 10.2

# window.postMessage Origin Validation

**MUST** verify `event.origin` against an expected allowlist and use a target-origin argument on every `postMessage` call.

**Why:** Skipping checks lets any embedded frame or opened window read sensitive messages or inject forged ones into the app.

**Detect:** grep `addEventListener('message'`, `postMessage(` with `'*'` target, handlers lacking `event.origin` comparison or `event.source` checks.

**References:** CWE-346, OWASP A01:2021, MDN postMessage security considerations

# Sensitive Data in Browser Storage (localStorage/sessionStorage)

**MUST NOT** store session tokens, refresh tokens, PII, or cryptographic keys in localStorage or sessionStorage.

**Why:** Web storage has no expiry or HttpOnly protection, so any XSS exfiltrates it persistently and it survives browser restarts and shared machines.

**Detect:** grep `localStorage.setItem`, `sessionStorage.setItem` for `token`, `jwt`, `password`, `secret`, `ssn`; review auth libraries' persistence config.

**References:** CWE-922, OWASP A02:2021, OWASP Authentication Cheat Sheet (token storage)

# Unvalidated Redirects & Forwards (open redirect in routing/SSO returns)

**MUST NOT** route users via unvalidated `redirect`/`returnUrl` parameters; destinations must pass an allow-list check.

**Why:** Open redirects turn your trusted domain into a phishing launchpad and can leak SSO tokens or OAuth codes externally.

**Detect:** grep `?redirect=`, `next=`, `returnUrl`, `rd=` reaching `redirect()` or `Location:` without allow-list validation.

**References:** OWASP Top 10 A01:2021, CWE-601, OWASP Redirects Cheat Sheet, RFC 6819

# Exposed Debug & Actuator Endpoints

**MUST NOT** expose framework debug or management endpoints (Spring Actuator `/env` `/heapdump`, Django `DEBUG=True`, `/phpinfo`, Rails `/debug`, pprof, adminer) on production interfaces.

**Why:** These endpoints dump env vars, heap memory, config, and internals — a single unauthenticated `/env` request can leak every secret in the service.

**Detect:** grep routes/config for `actuator`, `DEBUG`, `phpinfo`, `pprof`, `django-debug`; DAST-scan prod for `/env`, `/heapdump`, `/debug`, `/server-status`.

**References:** OWASP WSTG-CONF-04, CWE-489, CWE-200

# Forced Browsing & Unprotected Admin Panels

**MUST** authenticate and network-restrict every admin panel, dashboard, and management UI (Kibana, Adminer, /admin, wp-admin, portainer, argocd guest access).

**Why:** Scanners (Nuclei, ffuf) find default-open admin UIs constantly; "security by obscure path" fails against wordlist enumeration.

**Detect:** fuzz paths `/admin`, `/console`, `/kibana`, `/portainer`, `/adminer`; check Nginx/ingress auth annotations and network policies for management routes.

**References:** OWASP WSTG-ATHZ-02, MITRE ATT&CK T1595.001, Nuclei admin-panel templates

# Broken Link & Dependency Hijacking

**SHOULD** remove or pin dead external references (deleted CDN packages, lapsed domains, 404'd script/CSS links) that attackers can register and serve malicious content through.

**Why:** A dangling `<script src>` to an unregistered domain is a supply-chain foothold the browser trusts implicitly — recon tools flag these by checking DNS on referenced hosts.

**Detect:** crawl pages and check HTTP status + DNS registration of every external script/CSS/frame host; grep templates for known-dead CDNs (bower, rawgit, shutdown libraries).

**References:** OWASP WSTG-BUSLOGIC broken-link hijacking, CWE-427, npm/CDN takeover incidents

