# web-api-security — full checklist (49 items)

Server-side API and web application attack surface.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/web-api-security.md](../categories/web-api-security.md) · Index: [SKILL.md](../SKILL.md)

# Account recovery and password-reset flow security (tokens, helpdesk takeover)

**MUST NOT** allow helpdesk or support staff to reset a user's password without a verified second channel (e.g. confirmed email + MFA challenge) and full audit logging.

**Why:** Social-engineering the helpdesk is the cheapest path to takeover; a single unverified reset request bypasses every other control.

**Detect:** grep support/reset tooling for missing identity-verification step, no `audit_log` on manual resets, reset-by-username-only admin endpoints without MFA gate.

**References:** NIST SP 800-63B §5.1.1.2, CWE-287, OWASP A07:2021, CWE-354

# API Gateway Mapping Template / Proxy Passthrough Injection

**MUST NOT** interpolate raw request data into VTL mapping templates or constructed upstream payloads without escaping and schema validation; treat `$input` and `$context` fields as attacker-controlled strings.

**Why:** Naive `$input.json()` splicing into JSON or header templates lets a crafted body break out of the intended structure — forging identity headers, smuggling backend directives, or corrupting the upstream request that the backend trusts because it "came from the gateway."

**Detect:** Audit `*.vm`/VTL templates for direct `$input.json('...')` or `$context.identity.*` writes into headers and bodies without `escapeJson`/`escapeJava`; look for passthrough mode `WHEN_NO_TEMPLATE` on sensitive integrations, and templates that set `X-User-Id` from the body instead of the verified authorizer context.

**Bad:**
```vtl
{ "user": $input.json('$.user'), "role": $input.json('$.role') }
```

**Good:**
```vtl
#set ($user = $input.json('$.user'))
{ "user": "$util.escapeJson($user)",
  "role": "$context.authorizer.claims.role" }
```

**References:** CWE-74, AWS API Gateway mapping template docs, OWASP Injection cheatsheet

# Bot Protection

**MUST** challenge automated clients on login, signup, password-reset, and other abuse-prone flows with bot detection or a challenge (fingerprinting, proof-of-work, CAPTCHA), on top of whatever rate limiting applies.

**Why:** Credential stuffing and signup abuse are spread across large proxy pools, so per-IP throttling alone does not stop them; a challenge is what separates a script from a user.

**Detect:** grep auth flows for a challenge step (`captcha`, `recaptcha`, `turnstile`, `hcaptcha`, `bot_detection`, `proof_of_work`) or bot-detection middleware; a login route with throttling but no challenge at all.

**References:** OWASP A04:2021, CWE-770, OWASP Credential Stuffing Prevention Cheat Sheet

# Business Logic Workflow Bypass & Abuse

**MUST** enforce step ordering, state transitions, and per-user limits server-side rather than trusting the client's flow.

**Why:** Attackers replay, skip, or race steps to get coupons twice, skip payment, or reach states the design never intended.

**Detect:** State transitions driven by client fields, no server-side state machine, idempotency key absent on money actions, missing per-user rate/limit checks.

**References:** CWE-841, CWE-362, OWASP Business Logic Errors, ASVS 4.x

# Clickjacking

**MUST** Send `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'` on authenticated pages.

**Why:** Invisible iframes overlay trusted buttons onto attacker pages for unintended clicks.

**Detect:** Missing `X-Frame-Options`/`frame-ancestors` in headers or middleware; `ALLOWALL` frame options.

**References:** OWASP A05:2021, CWE-1021, OWASP Clickjacking Defense Cheat Sheet

# Cloud Instance Metadata Endpoint Protection (IMDSv2)

**MUST** require session-token (IMDSv2) mode on every EC2-style instance and container host, with a hop limit of 1–2, so that simple single-request SSRF cannot read credentials.

**Why:** The original v1 metadata service answers any GET from the link-local address; an SSRF in user-facing code can then exfiltrate the instance's IAM role credentials in one request.

**Detect:** Review `aws ec2 modify-instance-metadata-options` settings, launch templates/user-data for `HttpTokens=required` and `HttpPutResponseHopLimit`, EKS nodegroup configs, and any Terraform `metadata_options` blocks left at defaults or `optional`.

**Bad:**
```hcl
metadata_options {
  http_tokens = "optional"   # v1 still reachable by plain GET SSRF
}
```

**Good:**
```hcl
metadata_options {
  http_tokens                 = "required"
  http_put_response_hop_limit = 1
}
```

**References:** AWS IMDSv2 announcement (2019), AWS Well-Architected Security Pillar, CIS AWS 5.6

# Content Security Policy

**SHOULD** Deliver CSP with nonce/hash-based `script-src`; avoid `unsafe-inline` and `unsafe-eval`.

**Why:** A weak CSP removes the last defense once an injection flaw exists.

**Detect:** `unsafe-inline`, `unsafe-eval`, `script-src *` in CSP config; no `Content-Security-Policy` header.

**References:** OWASP A05:2021, CWE-693, Google CSP Evaluator

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

# Cross-Site WebSocket Hijacking (CSWSH)

**MUST** validate the `Origin` header on the WebSocket upgrade handshake against an explicit allowlist.

**Why:** WebSockets ignore CORS; any malicious site can open a socket using the victim's cookies and act as them in real time.

**Detect:** grep `ws://`, `wss://`, `upgrade` handlers, `onConnection` without origin checks; nginx `proxy_set_header Origin` passthrough config.

**References:** CWE-1385, OWASP A01:2021, RFC 6455 section 10.2

# CSRF

**MUST** Require a per-session token or origin check on every state-changing request.

**Why:** Without it, an attacker's page forges authenticated requests that change user state.

**Detect:** POST/PUT/DELETE routes lacking `csrf_protect`, `X-CSRF-Token`, `SameSite`; `csrf_exempt=True`.

**References:** OWASP A01:2021, CWE-352, OWASP CSRF Prevention Cheat Sheet

# Debug/Dev Mode in Production

**MUST NOT** ship production with debug mode, verbose traces, interactive debuggers, or profiling endpoints.

**Why:** Traceback pages leak source and secrets; debug consoles allow code execution.

**Detect:** `DEBUG = True`, `FLASK_DEBUG=1`, `app.run(debug`, exposed `/debug`, Werkzeug console.

**References:** OWASP A05:2021, CWE-489, CWE-215

# Decompression Bombs & XML Entity Expansion

**MUST** Cap compressed size, decompressed output, and entity expansion depth before and during parsing of untrusted input.

**Why:** A kilobyte zip-bomb or "billion laughs" XML expands to gigabytes, exhausting memory in seconds.

**Detect:** `zipfile.extractall`, `zlib.decompress` without size caps; XML parsers without entity-expansion limits.

**References:** CWE-409, CWE-776, CWE-789

# Dynamic Code Evaluation of User Input (eval/exec)

**MUST NOT** pass any externally influenced string to `eval`, `exec`, `Function`, or template code execution.

**Why:** Evaluating attacker-controlled text is remote code execution — full host compromise, no sandbox assumed.

**Detect:** `eval(`, `exec(`, `new Function(`, `compile(`/`__import__` on request data, template rendering of user strings (Jinja `|safe`, `Template(user_str)`), expression evaluators over user input.

**References:** CWE-94, CWE-95, OWASP Injection, OWASP ASVS 5.2

# Email-Template Injection

**MUST** treat user-controlled data interpolated into transactional emails as untrusted: escape HTML, strip/sanitize URLs, and never render user input as links or markup.

**Why:** Usernames or fields containing `<a href="https://phish...">` turn your trusted, DKIM-signed transactional email into a phishing vector your own domain vouches for.

**Detect:** grep mail templates for raw interpolation of user fields (`{{name}}` without escape, `|safe`, `dangerouslySetInnerHTML`); check URL fields are validated against allow-lists before rendering as links.

**References:** CWE-94 code injection in mail templates, OWASP XSS in email clients guidance

# Exposed Debug & Actuator Endpoints

**MUST** disable unused framework debug and management endpoints and restrict the rest to authenticated management access (`management.endpoints.web.exposure.include`, `management.server.port`); `/env`, `/heapdump`, `/phpinfo`, and `pprof` handlers are never reachable unauthenticated.

**Why:** These endpoints dump env vars, heap memory, config, and internals — a single unauthenticated `/env` request can leak every secret in the service.

**Detect:** grep routes/config for `actuator`, `DEBUG`, `phpinfo`, `pprof`, `django-debug`; DAST-scan prod for `/env`, `/heapdump`, `/debug`, `/server-status`.

**References:** OWASP WSTG-CONF-04, CWE-489, CWE-200

# Feature Flags

**MUST NOT** use feature flags as a substitute for access control; authorization checks belong server-side regardless of a flag's state.

**Why:** Toggling a flag off in the UI while the endpoint stays routable exposes unfinished, unauthenticated functionality to anyone who knows the URL.

**Detect:** grep flag SDK calls (`isEnabled(`, `flipper`, `launchdarkly`) wrapped around UI only while routes lack auth middleware; flags defaulting `true` in prod config.

**References:** OWASP ASVS 4.1 access control, CWE-862 missing authorization, Unleash/LaunchDarkly security guidance

# File Upload Validation

**MUST** Check uploads by magic bytes, enforce extension/size limits, store outside the web root with randomized names.

**Why:** Unvalidated uploads accept webshells that execute when fetched from a served directory.

**Detect:** `save(request.files[...])` without type/size checks; uploads under static paths; trusting client `Content-Type`.

**References:** OWASP A03:2021, CWE-434, OWASP File Upload Prevention Cheat Sheet

# Forced Browsing & Unprotected Admin Panels

**MUST** authenticate and network-restrict every admin panel, dashboard, and management UI (Kibana, Adminer, /admin, wp-admin, portainer, argocd guest access).

**Why:** Scanners (Nuclei, ffuf) find default-open admin UIs constantly; "security by obscure path" fails against wordlist enumeration.

**Detect:** fuzz paths `/admin`, `/console`, `/kibana`, `/portainer`, `/adminer`; check Nginx/ingress auth annotations and network policies for management routes.

**References:** OWASP WSTG-ATHZ-02, MITRE ATT&CK T1595.001, Nuclei admin-panel templates

# GraphQL Query Depth & Complexity Limits

**MUST** Cap query depth, node count, and alias size, rejecting over-budget queries before execution.

**Why:** Unbounded nesting multiplies resolver calls into denial-of-service from one request.

**Detect:** Server config without `max_depth`/`max_complexity` validation rules; persisted-query-only mode absent; `graphiql` in prod.

**References:** OWASP A04:2021, CWE-770, OWASP GraphQL Cheat Sheet

# HSTS

**SHOULD** Every HTTPS response carry a `Strict-Transport-Security` header with a max-age of at least one year, plus `includeSubDomains` on apex domains.

**Why:** Without HSTS, a single HTTP request or an SSL-stripping proxy can downgrade a connection; the header pins browsers to TLS so later visits can't be intercepted in plaintext.

**Detect:** Grep server and framework configs for `Strict-Transport-Security` and verify `max-age=31536000` or higher. Watch for nginx `add_header` directives in nested locations silently overriding each other.

**Bad:**
```nginx
server {
    listen 443 ssl;
    # no HSTS header at all
    location / { proxy_pass http://app; }
}
```

**Good:**
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

**References:** RFC 6797, CWE-319, OWASP A02:2021 Cryptographic Failures, WSTG-CONF-07

# HTTP Request Smuggling (CL.TE / TE.CL Desync)

**MUST** Front-end and back-end agree on one framing per request: reject requests carrying both `Content-Length` and `Transfer-Encoding`, and disable lenient chunked parsing downstream.

**Why:** When proxy and server disagree on where a request ends, an attacker smuggles a second request inside the first — hijacking someone else's credentials on the shared connection and poisoning caches with attacker-controlled responses.

**Detect:** Test the full proxy chain with the `http-request-smuggler` tool. Grep for proxies forwarding raw `Transfer-Encoding` to frameworks that also honor `Content-Length`; flag hops running different HTTP parser versions, and keepalive between desync-prone tiers.

**Bad:**
```
POST / HTTP/1.1
Content-Length: 13
Transfer-Encoding: chunked   # front-end trusts TE, back-end trusts CL

0

GET /admin HTTP/1.1         # smuggled request runs on the back-end
```

**Good:**
```nginx
# front-end rejects ambiguous framing before any parser sees it
if ($http_transfer_encoding) { return 400; }
proxy_set_header Transfer-Encoding "";   # normalize, never pass through raw
```

**References:** CWE-444, PortSwigger HTTP desync research, RFC 9112 §6.3 (reject both headers)

# IDOR

**MUST** Verify the authenticated principal may access every object referenced by a request identifier.

**Why:** Trusting client-supplied IDs lets anyone alter a number to read others' records.

**Detect:** `params['id']` in queries with no ownership filter or policy check; `get_object` without permissions.

**References:** OWASP A01:2021, CWE-639, OWASP Testing Guide IDOR

# Ingress Host-Header / vHost Routing Collisions and TLS Passthrough Misrouting

**MUST** define explicit host matching on every Ingress rule and a catch-all default backend that returns 404/421, so an unexpected `Host` header cannot route traffic to the wrong service.

**Why:** When rules overlap or a controller falls back to its default vhost, a request aimed at `admin.example.com` can land on an unrelated backend that processes it as if trusted — and TLS passthrough makes the mismatch invisible because the outer SNI never gets re-checked inside.

**Detect:** Look for Ingress resources with empty `host:` (matches everything), duplicate hosts across namespaces, `nginx.ingress.kubernetes.io/ssl-passthrough` on shared ports without per-SNI routing, and controllers configured with a permissive default backend. Test by sending crafted `Host:` headers to the LB IP and observing which service answers.

**Bad:**
```yaml
- http:
    paths:
      - path: /            # no host: matches ANY hostname
        backend: {serviceName: payments, servicePort: 443}
```

**Good:**
```yaml
- host: payments.example.com
  http:
    paths:
      - path: /
        pathType: Prefix
        backend: {serviceName: payments, servicePort: 443}
```

**References:** CWE-441, RFC 9110 §7.2 (Host), Kubernetes Ingress docs, OWASP A01:2021

# Input Validation

**MUST** Validate all external input against type, length, range, and format allowlists at the trust boundary.

**Why:** Downstream code assumes validated data; one unchecked field becomes the injection vector.

**Detect:** Handlers reading `request.params`/body straight into logic; missing pydantic/Zod/Joi or `@Valid`.

**References:** OWASP A03:2021, CWE-20, OWASP Input Validation Cheat Sheet

# Insecure Deserialization

**MUST NOT** Deserialize untrusted data with pickle, ObjectInputStream, unserialize, or BinaryFormatter; use schema-validated JSON.

**Why:** Native deserializers instantiate arbitrary classes, yielding remote code execution.

**Detect:** `pickle.loads`, `ObjectInputStream`, `unserialize(`, `yaml.load` without SafeLoader on request data.

**References:** OWASP A08:2021, CWE-502, OWASP Deserialization Cheat Sheet

# LDAP Injection

**MUST** Escape `* ( ) \` and NUL in values interpolated into LDAP filters; prefer parameterized libraries or strict allowlists.

**Why:** Unescaped input rewrites filter logic, bypassing authentication or dumping directory entries.

**Detect:** String-built `(&(uid=%s)...)` filters; `search(` with concatenated user values; missing `ldap_escape`.

**References:** CWE-90, OWASP A03:2021, OWASP LDAP Injection Prevention Cheat Sheet

# Mass Assignment

**MUST** Whitelist assignable fields when binding request bodies to models.

**Why:** Attackers add hidden fields like `is_admin` to escalate privileges or bypass rules.

**Detect:** `Model(**request.json)`, `save(params)`, `bindAll`; no allowed/forbidden lists in serializers.

**References:** OWASP A08:2021, CWE-915, Rails mass-assignment guide

# Missing Authentication Middleware / Default-Deny Routing

**MUST** default-deny: every route requires authentication unless explicitly marked public via an allowlist.

**Why:** Route-by-route opt-in means any forgotten or newly added endpoint ships unauthenticated, exposing internal APIs to the internet.

**Detect:** grep router config for missing global auth middleware, routes without `@authenticated`/`requireAuth`, `public: true` as default, admin endpoints outside auth filter chain.

**References:** OWASP A01:2021, CWE-306, NIST SP 800-53 AC-3, CIS Control 6.7 (Centralize Access Control)

# NoSQL Query Injection

**MUST NOT** build queries by merging raw user input into query objects; validate types and use explicit field-level operators instead of user-controlled dicts or `$where` clauses.

**Why:** MongoDB-style engines interpret operator keys inside user JSON: `{"pass": {"$ne": ""}}` submitted into a naive `find(body)` authenticates without a password. `$where` with string concatenation goes further, executing arbitrary JavaScript server-side.

**Detect:** Grep for `find(req.body)`, `$where`, `mapReduce` with interpolation, and PyMongo/Mongoose filters whose dict originates from request payloads. Check for missing schema validation (Mongoose strict mode, JSON Schema) on inbound documents.

**Bad:**
```javascript
db.users.find({
  user: req.body.user,
  pass: req.body.pass   // {"$ne":""} bypasses auth
});
```

**Good:**
```javascript
const u = String(req.body.user), p = String(req.body.pass);
db.users.findOne({ user: u, pass: await verify(p) });
```

**References:** CWE-943 NoSQL injection, OWASP NoSQL Injection Prevention Cheat Sheet, MongoDB $where security notes

# Open Directory Listing

**SHOULD NOT** enable directory indexes on web servers or object storage where file enumeration reveals backups, configs, or internal artifacts.

**Why:** `Autoindex on` / bucket list permission turns one known filename pattern into a full inventory of everything ever placed there.

**Detect:** grep server configs for `autoindex on`, `Options +Indexes`, bucket `ListBucket` grants; probe for `Index of /` responses.

**References:** OWASP WSTG-CONF-02, CWE-548, AWS S3 ACL best practices

# Open Redirect

**SHOULD NOT** Redirect from query params (`next`, `returnTo`) without an allowlist or relative-path restriction.

**Why:** "login?next=evil.com" links land victims on phishing pages via your trusted domain, and open redirects can also leak SSO tokens or OAuth codes to external destinations.

**Detect:** `redirect(request.args['next'])`, `location=` from params without allowlist or leading-slash enforcement; grep `?redirect=`, `next=`, `returnUrl`, `rd=` reaching `redirect()` or `Location:` headers.

**References:** OWASP A01:2021, CWE-601, OWASP Unvalidated Redirects guide

# OS Command Injection (CWE-78)

**MUST NOT** Pass user input into shell commands; invoke programs with argument arrays, no shell interpolation.

**Why:** `;`, `|`, and backticks turn an argument into arbitrary command execution.

**Detect:** `os.system`, `subprocess` with `shell=True`, `Runtime.exec`, `$()`/backticks in built command strings.

**References:** CWE-78, OWASP A03:2021, OWASP Command Injection guidance

# Path Traversal

**MUST NOT** Use user input directly in file paths; resolve and confirm the result stays inside the base directory.

**Why:** `../` sequences escape the sandbox to read configs, keys, and source off the host.

**Detect:** `open(` / `send_file` with request params; `os.path.join(base, user_input)` without post-resolve prefix check.

**References:** OWASP A03:2021, CWE-22, OWASP Path Traversal guide

# Rate Limiting / Throttling

**SHOULD** Throttle auth, reset, and expensive endpoints per identity and IP, returning 429 with `Retry-After`.

**Why:** Unlimited endpoints enable credential stuffing, brute force, and cost amplification.

**Detect:** Login/reset routes with no `ratelimit`, `throttle`, `limit=` decorator or gateway policy.

**References:** OWASP A04:2021, CWE-770, OWASP Rate Limiting Cheat Sheet, NIST SP 800-63B

# Regular Expression DoS (ReDoS)

**MUST NOT** run user-supplied or unbounded text against regexes containing nested quantifiers or ambiguous alternation.

**Why:** Catastrophic backtracking turns a short malicious string into exponential CPU time, freezing the request thread or worker.

**Detect:** `(a+)+`, `(a|a)*`, `(.*)*` patterns, `re.match`/`RegExp.test` on raw input, no timeout or RE2/DFA engine configured.

**References:** CWE-1333, CWE-400, OWASP ReDoS, RE2 docs

# SaaS Webhook Consumer Trust

**MUST** verify signature, origin, and replay-protection on every inbound webhook from third-party SaaS — and treat payload contents as untrusted input.

**Why:** Unverified webhook endpoints accept forged events ("payment captured", "user verified") from anyone who finds the URL; SaaS signing secrets also rotate, which unverified integrations hide until they break.

**Detect:** grep webhook handlers for signature verification (HMAC compare, provider SDK `constructEvent`), timestamp tolerance checks, idempotency-key dedupe; flag handlers that trust payload identity fields blindly.

**References:** OWASP Webhook Security practices, Stripe/GitHub webhook verification docs, CWE-345 insufficient verification of data authenticity

# Security Headers

**MUST** Set HSTS, `X-Content-Type-Options: nosniff`, CSP, `Referrer-Policy`, and frame protection on every response.

**Why:** Missing headers leave transport, sniffing, and framing attacks unmitigated.

**Detect:** Config lacking `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`; nginx/ingress snippets absent.

**References:** OWASP A05:2021, CWE-693, securityheaders.com checklist

# Sensitive endpoint exposure (actuator, /admin, .git, .env, debug routes, dashboards)

**MUST NOT** Expose admin panels, actuator endpoints, `.git`/`.env` files, or dashboards publicly; gate them behind auth.

**Why:** Leaked `.env` and `.git` hand attackers credentials and full source directly.

**Detect:** Reachable `/actuator`, `/admin`, `/.git/HEAD`, `/.env`, `/server-status`, `/metrics` without auth.

**References:** OWASP A05:2021, CWE-538, CWE-200, OWASP WSTG-CONF-05

# Server-Side Authorization

**MUST NOT** Trust the client for any authorization decision: hidden UI, client route guards, and client-supplied role or permission values are all forgeable, so permissions are re-derived server-side from the authenticated session on every request.

**Why:** Hidden buttons and guarded routes are bypassed by calling the API directly.

**Detect:** handlers reading role or permission from a request body, header, or unverified token claim; permission flags echoed to the client and trusted back; destructive actions gated only in the frontend router.

**References:** OWASP A01:2021, CWE-862, OWASP Authorization Cheat Sheet

# Server-Side Template Injection (SSTI)

**MUST NOT** Render user input as a template; pass it only as context variables, never into dynamic template compilation.

**Why:** Expressions like `{{config}}` evaluate server-side, escalating to remote code execution.

**Detect:** `render_template_string(user_input)`, `Template(request...)`, `format_map` with user strings.

**References:** CWE-1336, OWASP A03:2021, PortSwigger SSTI research

# SQL Injection

**MUST** Use parameterized queries or bound variables; never concatenate user input into SQL.

**Why:** Concatenated input lets attackers rewrite query logic to dump or destroy data.

**Detect:** `execute(` with f-strings, `%` formatting, or `+`/`||` concatenation of request values.

**References:** OWASP A03:2021, CWE-89, OWASP SQL Injection Prevention Cheat Sheet

# SSRF

**MUST** Restrict user-supplied URLs to an allowlist of hosts/schemes, blocking internal ranges after DNS resolution.

**Why:** Crafted URLs reach internal services and cloud metadata endpoints to steal credentials.

**Detect:** `requests.get(user_url)`, `urlopen`, `fetch(` on request-derived URLs without IP-blocklist checks.

**References:** OWASP A10:2021, CWE-918, SSRF-Defense list

# Tenant-ID Spoofing at API Boundary

**MUST** derive the tenant from the authenticated session/token on every request — never from a client-supplied tenant_id parameter or header.

**Why:** The classic cross-tenant breach: API trusts `?tenant_id=` from the caller, letting one tenant read or mutate another's data with a valid session.

**Detect:** grep handlers for `tenant_id`/`org_id` read from query params, headers, or request bodies rather than from auth context; check middleware sets tenant once and handlers cannot override.

**References:** OWASP API1:2023 broken object level authorization, OWASP Multi-Tenant Security Cheat Sheet

# Web Cache Poisoning & Cache Deception

**SHOULD NOT** cache responses that vary on unkeyed inputs like headers, query params, or cookies without declaring `Vary` or normalizing them.

**Why:** An attacker can get a poisoned response stored in CDN/proxy cache and served to every subsequent visitor of that URL.

**Detect:** grep `Vary:`, `cache-control: public`, unkeyed `X-Forwarded-*`/`Accept-Encoding` handling; CDN cache-key config ignoring query params.

**References:** PortSwigger Web Cache Poisoning research, OWASP A04:2021

# Webhook Replay Protection

**MUST NOT** rely on signatures alone for webhook authenticity; add timestamp windows and nonce deduplication to block valid-signature replays.

**Why:** A captured signed webhook stays replayable forever without expiry — an attacker resends a legitimate payment event days later undetected.

**Detect:** grep webhook receivers for missing `timestamp` validation, absent `nonce`/`event_id` dedup store, signature checks with no freshness window.

**References:** OWASP Webhook Security Best Practices, CWE-294, Stripe/GitHub webhook verification docs

# Webhook Signature Verification

**MUST** verify the provider HMAC over the raw body with constant-time comparison before acting on any webhook.

**Why:** Unsigned endpoints accept forged events — fake payments, refunds, account changes.

**Detect:** Handlers with no signature check; `hmac.compare_digest` absent; verification skipped in dev branches.

**References:** CWE-347, CWE-208, Stripe/GitHub webhook signing docs

# XSS

**MUST NOT** emit user-controlled data into HTML without context-aware escaping; raw-output helpers and escaping-filter bypasses (`|safe`, `Markup(`, `dangerouslySetInnerHTML`) MUST NOT receive request-controlled data.

**Why:** Injected scripts run in victims' sessions, stealing cookies and acting as them.

**Detect:** `innerHTML`, `dangerouslySetInnerHTML`, `|safe`, `Markup(` fed by request data.

**References:** OWASP A03:2021, CWE-79, OWASP XSS Prevention Cheat Sheet

# XML External Entity (XXE) Injection

**MUST** Disable external entities and DTD processing in every XML parser (`resolve_entities=False`, secure processing features).

**Why:** Enabled external entities let crafted XML read local files and hit internal networks.

**Detect:** `lxml.etree.parse`, `DocumentBuilderFactory`, `XmlReader` without hardening flags; `DOCTYPE` accepted in inbound XML/SOAP/SVG.

**References:** CWE-611, OWASP A03:2021, OWASP XXE Prevention Cheat Sheet

