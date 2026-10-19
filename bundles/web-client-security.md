# web-client-security — full checklist (39 items)

Browser-side attack surface and defenses.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/web-client-security.md](../categories/web-client-security.md) · Index: [SKILL.md](../SKILL.md)

# Active Markup Format Rendering

**MUST** sanitize or disable user-controlled Markdown, CSS, XSL, and BBCode processing, because each is rendered by an expression engine, not as text.

**Why:** Markdown with raw-HTML passthrough, CSS expressions, and XSL scripts each reach an interpreter, so escaping for HTML alone leaves an execution path.

**Detect:** grep renderers for `markdown` with raw HTML enabled, `style=` interpolation, and XSL/`transform` calls on uploaded documents.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md

# Broken Link & Dependency Hijacking

**SHOULD** remove or pin dead external references (deleted CDN packages, lapsed domains, 404'd script/CSS links) that attackers can register and serve malicious content through.

**Why:** A dangling `<script src>` to an unregistered domain is a supply-chain foothold the browser trusts implicitly — recon tools flag these by checking DNS on referenced hosts.

**Detect:** crawl pages and check HTTP status + DNS registration of every external script/CSS/frame host; grep templates for known-dead CDNs (bower, rawgit, shutdown libraries).

**References:** OWASP WSTG-BUSL, CWE-427, npm/CDN takeover incidents

# Sensitive Data in Browser Storage (localStorage/sessionStorage)

**MUST NOT** store session tokens, refresh tokens, PII, or cryptographic keys in localStorage or sessionStorage.

**Why:** Web storage has no expiry or HttpOnly protection, so any XSS exfiltrates it persistently and it survives browser restarts and shared machines.

**Detect:** grep `localStorage.setItem`, `sessionStorage.setItem` for `token`, `jwt`, `password`, `secret`, `ssn`; review auth libraries' persistence config.

**References:** CWE-922, OWASP A02:2021, OWASP Authentication Cheat Sheet (token storage)

# Cache-Control Headers

**MUST** set explicit `Cache-Control` on every HTTP response; responses carrying auth tokens, PII, or CSRF values require `no-store`, never a bare default.

**Why:** Missing directives let browsers and proxies cache sensitive pages, exposing them via back-button or shared caches.

**Detect:** Responses lacking `Cache-Control`; `no-store` absent on login, account, admin routes; `public, max-age` on authenticated endpoints.

**References:** OWASP A04:2021, CWE-525, RFC 9111 §5.2.2.5 (no-store)

# CDNs

**MUST NOT** allow CDNs to cache authenticated or per-user responses unless the origin marks them `private` and cache rules exclude them.

**Why:** A CDN caching a personalized response serves one user's data — tokens, PII, balances — to others sharing the URL.

**Detect:** CDN config caching paths like `/account`, `/api/me`; missing `Cache-Control: private` on authenticated responses at edge rules.

**References:** OWASP A01:2021, CWE-525, RFC 9111 section 3.5, Cloudflare cache rules docs

# Clickjacking

**MUST** Send `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'` on authenticated pages.

**Why:** Invisible iframes overlay trusted buttons onto attacker pages for unintended clicks.

**Detect:** Missing `X-Frame-Options`/`frame-ancestors` in headers or middleware; `ALLOWALL` frame options.

**References:** OWASP A05:2021, CWE-1021, OWASP Clickjacking Defense Cheat Sheet

# Clipboard Data Exposure

**MUST** suppress copy, cut, and drag for displayed secrets and personal data, and prefer in-app transfer paths over shared OS buffers.

**Why:** Clipboard, drag-drop, and share buffers are readable by every process on the machine and can persist after the user leaves the screen.

**Detect:** grep navigator.clipboard.writeText, ClipboardManager, UIPasteboard.general, NSPasteboard near token, password, or PII handlers

**References:** Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en_20250827.pdf

# Content Security Policy

**SHOULD** Deliver CSP with nonce/hash-based `script-src`; avoid `unsafe-inline` and `unsafe-eval`.

**Why:** A weak CSP removes the last defense once an injection flaw exists.

**Detect:** `unsafe-inline`, `unsafe-eval`, `script-src *` in CSP config; no `Content-Security-Policy` header.

**References:** OWASP A05:2021, CWE-693, Google CSP Evaluator

# Cookie Consent

**SHOULD** block non-essential cookies until explicit user consent is obtained, with granular category controls.

**Why:** Setting tracking cookies before consent violates ePrivacy Directive and GDPR, exposing sites to regulatory fines and user distrust.

**Detect:** grep for analytics/advertising cookie initialization before consent check; inspect `CookieConsent`, `googleAnalytics`, `fbq` calls preceding consent gate.

**References:** ePrivacy Directive Art. 5(3), GDPR Recital 30, IAB TCF v2.3

# Cookie Flags: Secure, HttpOnly, SameSite

**MUST** set `Secure`, `HttpOnly`, and `SameSite=Lax` (or `Strict`) on every session cookie issued by the application.

**Why:** Missing flags let cookies leak over HTTP, be read by injected scripts, or ride cross-site requests, enabling session hijacking and CSRF.

**Detect:** grep `Set-Cookie`, `res.cookie(`, `document.cookie=`; inspect ingress/Envoy/nginx cookie-rewrite annotations for stripped flags.

**References:** RFC 6265, draft-ietf-httpbis-rfc6265bis §4.1.2.7 (SameSite), OWASP Session Management Cheat Sheet, CWE-1004, CWE-1275

# Cookie Name Prefixes

**MUST** use the `__Host-` prefix on session cookies that are not explicitly meant to be shared across hosts.

**Why:** Without `__Host-`, a sibling subdomain can set a cookie of the same name with `Domain=example.com`, and the server cannot tell it from its own.

**Detect:** grep `Set-Cookie` for session and auth cookies whose names lack `__Host-` or that carry a `Domain` attribute.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, RFC 6265bis (cookie prefixes)

# Cookie Size Limits

**MUST** keep each cookie's name and value under 4096 bytes combined.

**Why:** Browsers drop an oversized cookie without an error, so a session or CSRF cookie simply stops existing and the control it carried disappears.

**Detect:** grep for cookie assembly that concatenates unbounded values, and count `Set-Cookie` headers per response.

**References:** RFC 6265, https://www.rfc-editor.org/rfc/rfc6265.html, OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md

# CORS

**MUST NOT** Pair wildcard or reflected `Access-Control-Allow-Origin` with `Allow-Credentials: true`; whitelist trusted origins.

**Why:** Wildcard-plus-credentials lets any site read authenticated responses cross-origin.

**Detect:** `Allow-Origin: *`, `allow_origins=['*']`, `@CrossOrigin` with credentials, origin reflection.

**References:** OWASP A05:2021, CWE-942, MDN CORS credentials

# CRLF / HTTP Header Injection & Response Splitting

**SHOULD NOT** Put user input into headers or redirect targets without rejecting CR/LF and `%0d%0a`.

**Why:** Injected line breaks forge headers or a whole second response, poisoning caches and sessions.

**Detect:** `set_header(..., user_value)`, `Location:`/`Set-Cookie` built from params without CRLF filtering.

**References:** CWE-113, CWE-93, PortSwigger HTTP Response Splitting

# WebSockets: Upgrade Authentication & Origin Validation (CSWSH)

**MUST** authenticate the upgrade handshake and validate the `Origin` header against an explicit allowlist on every WebSocket connection.

**Why:** WebSockets ignore CORS, so any malicious site can open a socket using the victim's cookies and act as them in real time, streaming private data to the attacker's page.

**Detect:** grep `ws://`, `wss://`, `Upgrade: websocket` upgrade handlers, `onConnection` without origin checks (missing `checkOrigin`/`Origin` validation) or with auth deferred to post-open messages; nginx `proxy_set_header Origin` passthrough config.

**References:** CWE-1385, CWE-346, OWASP A01:2021, OWASP API 2023, RFC 6455 section 10.2

# Fresh CSP Nonce Per Response

**MUST** generate a fresh CSP nonce for every response and verify no cache layer serves a nonce minted for another request.

**Why:** A reused nonce becomes a static allowlist token, so an attacker who sees one value can inject script the policy admits.

**Detect:** command `curl -sI` the same page repeatedly through the CDN and diff the `content-security-policy` nonce; grep cache config for how CSP is cached or shared.

**References:** CSP nonce reuse measurement, https://arxiv.org/abs/2309.07782

# CSRF

**MUST** Require a per-session token or origin check on every state-changing request.

**Why:** Without it, an attacker's page forges authenticated requests that change user state.

**Detect:** POST/PUT/DELETE routes lacking `csrf_protect`, `X-CSRF-Token`, `SameSite`; `csrf_exempt=True`.

**References:** OWASP A01:2021, CWE-352, OWASP CSRF Prevention Cheat Sheet

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

# DOM Clobbering Defenses

**MUST NOT** depend on global names, implicit element identifiers, or untyped DOM property access; declare variables explicitly and read values through typed accessors.

**Why:** Markup injection can shadow a global the script trusts, so a config object becomes an attacker-chosen element and a check silently reads the wrong value.

**Detect:** grep for bare global reads (`if (config)`, `window.<id>`), `document.forms[name]` lookups, and `id`/`name` attributes that collide with script globals.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, OWASP WSTG: Testing for DOM Clobbering

# Encode at the Sink

**MUST** encode untrusted data for the consuming interpreter at the last step before it is interpreted, never when it is stored.

**Why:** A value encoded early is decoded or re-interpreted by the layers in between, so the protection is gone exactly where it was needed.

**Detect:** grep for escaping applied on write (`html.EscapeString`, `escapeHtml`, `htmlspecialchars`) in model setters or INSERT paths instead of in the view/template layer.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md

# Maintained HTML Sanitizer

**MUST** sanitize untrusted rich-text HTML with a maintained allow-list sanitizer library, never a hand-written filter.

**Why:** Mutation-XSS bypasses any regex or tag-stripping filter you write; sanitizer maintainers absorb a parser-differential treadmill you cannot.

**Detect:** grep for bespoke sanitizers (`re.sub` on `<script`, `strip_tags`, custom `sanitize_html` helpers) and confirm an allow-list library (DOMPurify, bleach, sanitize-html, OWASP Java HTML Sanitizer) is the only path.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md

# JSONP and XSSI Defense

**MUST NOT** expose authorized data through script-inclusion formats, or return JSON that another origin can read through a script tag.

**Why:** A callback-wrapped or bare JSON response is readable by any page that includes it, so authenticated data leaks without an XSS bug.

**Detect:** grep for `callback=`, `jsonp`, `jsoncallback` handlers and for JSON endpoints missing an anti-XSSI prefix or `Content-Type` enforcement.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, CWE-200

# No Remote Code In Plugins

**MUST NOT** load executable code from remote origins into a privileged extension, plugin, or widget context; remote content is data only.

**Why:** Remote script inclusion hands code execution to whoever controls that path, inside a context that already holds elevated permissions.

**Detect:** grep extension manifests, plugin loaders, and CSP for remote script URLs (`<script src="https://`, `import("http`, `eval(fetch(`) and remote `script-src` allowances.

**References:** Remote JavaScript inclusion in browser extensions, https://arxiv.org/abs/2505.19456

# Origin Isolation

**MUST** host separate applications on separate hostnames so the same-origin policy keeps one from scripting or reading the other.

**Why:** Two apps on one origin share cookies, storage, and script context, so a flaw in the weaker one is an authenticated foothold in the stronger.

**Detect:** grep ingress and router config for several apps mounted under one host or path prefix, and list the cookies and storage keys they share.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, CWE-346

# Permissions Policy Declaration

**SHOULD** send a Permissions-Policy header that disables powerful browser capabilities the application never uses.

**Why:** A compromised third-party script inherits access to camera, microphone, geolocation, and payment interfaces by default. Declaring the unused set removes the capability instead of trusting the script.

**Detect:** grep response header configuration for `Permissions-Policy` or `Feature-Policy`; compare the declared capabilities against the features the application actually calls.

**References:** OWASP Proactive Controls C8, https://github.com/OWASP/www-project-proactive-controls, W3C Permissions Policy

# Policy Intersection Composition

**MUST** compose overlapping policy layers by intersection, so the effective policy allows only what every layer allows.

**Why:** Ad-hoc layering produces union-shaped surprises where the looser layer wins silently and reviewers believe the strictest layer applied.

**Detect:** grep policy composition for `extend(`, `append(`, `add(` or `+` applied to source or allow lists where an intersection is intended.

**References:** W3C CSP Level 3, https://w3c.github.io/webappsec-csp/

# window.postMessage Origin Validation

**MUST** verify `event.origin` against an expected allowlist and use a target-origin argument on every `postMessage` call.

**Why:** Skipping checks lets any embedded frame or opened window read sensitive messages or inject forged ones into the app.

**Detect:** grep `addEventListener('message'`, `postMessage(` with `'*'` target, handlers lacking `event.origin` comparison or `event.source` checks.

**References:** CWE-346, OWASP A01:2021, MDN postMessage security considerations

# Unsafe Merge Into Shared Runtime State

**MUST** allow-list keys before recursive merge or deep-set of untrusted input into shared, inherited, or prototype-level objects/registries.

**Why:** Poisoning shared state (JS `Object.prototype` via `__proto__` is the classic case; unsafe map/dict merge into shared config or caches is the same class) leaks attacker-controlled values to every later consumer — enabling XSS, auth bypass, and RCE.

**Detect:** grep merge/deep-set helpers fed request bodies (`merge(`, `deepSet`, `set(obj, key`); check `__proto__`/`constructor`/`prototype` key filtering; audit known-vulnerable library versions (e.g. lodash <4.17.21) and JSON.parse-then-merge flows.

**References:** CWE-1321, OWASP A08:2021, OWASP Prototype Pollution Prevention Cheat Sheet

# Report Payload Minimization

**SHOULD** strip sensitive context from violation and error reports, sending the origin instead of full URLs and referrers.

**Why:** Reporting endpoints exfiltrate exactly the data the application is trying to protect, and they are often third-party. Full URLs carry tokens, search terms and internal paths.

**Detect:** `report-uri`/`report-to` endpoints and error-tracker DSNs receiving full `document.URL`, `Referer`, query strings or headers unscrubbed.

**References:** W3C CSP Level 3, https://w3c.github.io/webappsec-csp/

# Security Headers

**MUST** Set HSTS, `X-Content-Type-Options: nosniff`, CSP, `Referrer-Policy`, and frame protection on every response.

**Why:** Missing headers leave transport, sniffing, and framing attacks unmitigated.

**Detect:** Config lacking `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`; nginx/ingress snippets absent.

**References:** OWASP A05:2021, CWE-693, securityheaders.com checklist

# Session Fixation

**MUST** regenerate the session identifier immediately after any successful authentication or privilege change.

**Why:** If the session ID survives login, an attacker who planted one earlier rides the victim's now-authenticated session undetected.

**Detect:** grep login handlers for missing `session.regenerate`, `session_id` unchanged post-auth, `secure`/`httpOnly` cookie flags absent on session cookies.

**References:** OWASP A07:2021, CWE-384, OWASP Session Management Cheat Sheet

# Sibling Domain Distrust

**MUST** treat every sibling subdomain as potentially hostile: no parent-domain cookies, wildcard CORS, or postMessage trust that assumes the domain family is one zone.

**Why:** An attacker who takes over or registers any sibling domain inherits the trust that cookies, CORS rules, and CSP allowances extend to the whole family.

**Detect:** grep for `Domain=.example.com` cookies, `Access-Control-Allow-Origin` wildcard-subdomain regex, `document.domain`, and `postMessage` targets on `*.example.com`.

**References:** Related-domain attacker framework, https://arxiv.org/abs/2012.01946

# Subresource Integrity

**MUST** require integrity hashes on every externally hosted script or stylesheet, or record an explicit exception with its rationale.

**Why:** A third-party host or CDN that is compromised, or a package that is deleted and re-registered, serves attacker code into the page with full origin privileges.

**Detect:** grep `<script src="http` and `<link href="http` for missing `integrity=` attributes.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, W3C Subresource Integrity

# SVG Active Content

**MUST** strip scripts, event handlers, and `foreignObject` from user-supplied SVG, or serve it as an image rather than inline markup.

**Why:** SVG is an HTML document with an XML syntax; an upload endpoint that renders it inline is a stored-XSS endpoint with an image extension.

**Detect:** grep for `image/svg`, `<svg` injected into templates, and for `.svg` accepted by upload allow-lists with no `foreignObject`/`onload` filtering.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md

# Third-Party Tag & Script Governance

**MUST** inventory, approve, and CSP-restrict every third-party script loaded in the app (analytics, marketing tags, chat widgets).

**Why:** Marketing tags execute with your page's full privileges — a compromised tag is a Magecart-class supply-chain attack on your users' sessions and payment data.

**Detect:** list `<script src>` third-party hosts in templates; check CSP `script-src` uses nonces/hashes not `unsafe-inline`/wildcards; look for tag-manager sprawl without an approval list.

**References:** OWASP Magecart/Client-side supply chain, CSP script-src guidance, W3C CSP Level 3

# Untrusted Text in Admin UI

**MUST** mark user-supplied text wherever it appears in privileged review, approval, or system-message surfaces so it cannot be mistaken for system output.

**Why:** A file named "Payment Approved - Finance System" deceives a human approver with no script execution and no technical exploit at all.

**Detect:** grep admin and approval templates for user-controlled fields (filenames, display names, subjects) rendered in the same style as system labels.

**References:** OWASP WSTG Business Logic Testing, https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing

# Uploaded Content Serving

**MUST** serve user-uploaded content from a separate origin or object store, never execute or render it inline from the application's own origin.

**Why:** An uploaded HTML or SVG file served from your origin runs with your cookies and origin privileges, turning a file upload into stored script execution. Content inspection alone does not survive every parser differential.

**Detect:** grep upload handlers and static routes for upload directories inside the document root, inline `Content-Disposition`, and missing `X-Content-Type-Options: nosniff`; confirm uploads resolve to a distinct hostname or bucket.

**References:** OWASP File Upload Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html, CWE-434 Unrestricted Upload of File with Dangerous Type

# Web Cache Poisoning & Cache Deception

**SHOULD NOT** cache responses that vary on unkeyed inputs like headers, query params, or cookies without declaring `Vary` or normalizing them.

**Why:** An attacker can get a poisoned response stored in CDN/proxy cache and served to every subsequent visitor of that URL.

**Detect:** grep `Vary:`, `cache-control: public`, unkeyed `X-Forwarded-*`/`Accept-Encoding` handling; CDN cache-key config ignoring query params.

**References:** PortSwigger Web Cache Poisoning research, OWASP A04:2021

# XSS

**MUST NOT** emit user-controlled data into HTML without context-aware escaping; raw-output helpers and escaping-filter bypasses (`|safe`, `Markup(`, `dangerouslySetInnerHTML`) MUST NOT receive request-controlled data, and user-controlled data MUST NOT be interpolated into server-rendered HTML (`__NEXT_DATA__`, `window.__INITIAL_STATE__`, inline `<script>` blocks, unescaped `{{ }}` templates) without context-aware escaping for script, attribute, and URL contexts.

**Why:** Injected scripts run in victims' sessions, stealing cookies and acting as them; unescaped state serialized into `__NEXT_DATA__` or inline scripts executes on every page load before hydration, bypassing CSP unsafe-inline allowances.

**Detect:** `innerHTML`, `dangerouslySetInnerHTML`, `|safe`, `Markup(` fed by request data; `JSON.stringify` inside `<script>`, `window.__INITIAL_STATE__`, and unescaped `{{ }}` templates in server-rendered HTML.

**References:** OWASP A03:2021, CWE-79, OWASP XSS Prevention Cheat Sheet

