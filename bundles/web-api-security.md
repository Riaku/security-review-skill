# web-api-security — full checklist (91 items)

Server-side API and web application attack surface.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/web-api-security.md](../categories/web-api-security.md) · Index: [SKILL.md](../SKILL.md)

# Abstraction Escape Hatches

**MUST** review the raw and escape-hatch APIs of every ORM, query builder, and template engine for untrusted input, since the abstraction does not sanitize them.

**Why:** Injection reappears wherever input reaches concatenated raw SQL, literal fragments, or template escape-hatch calls, and the layer itself ships its own vulnerabilities.

**Detect:** grep for `raw(`, `Raw(`, `.literal(`, `createQuery(`, `execute(`, `|safe`, `Markup(` receiving request data.

**References:** OWASP WSTG: ORM injection, https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Injection_Testing/, CWE-89 (SQL Injection)

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

# Archive Symlink Rejection

**MUST** reject archive entries that are symbolic or hard links unless explicitly required, and then only to allowlisted targets.

**Why:** A link entry that survives extraction points outside the destination, so the next read or write lands on a file the archive chose.

**Detect:** grep extraction code for link handling (`is_symlink`, `link_target`, `member.issym`, `tarfile` filter) and for a destination containment check.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md, CWE-59

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

# Canonicalize Before Validate

**MUST** decode and canonicalize input to one normal form before validating or comparing it, and reject input that still changes when re-decoded.

**Why:** A validator that sees a different string from the component that later decodes it approves an attack; nested encodings survive single-pass checks.

**Detect:** grep decode/unescape calls placed after the validation or comparison (`urldecode`, `normalize`, `unquote`) and validators that run on the raw parameter.

**References:** OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html, One Byte to Rule Them All (Facebook canonicalization bypass), https://david942j.blogspot.com/2018/10/one-byte-to-rule-them-all-fun-with-fb.html

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

# Content-Type Enforcement

**MUST** reject request bodies whose declared Content-Type is not the one the endpoint expects, before parsing.

**Why:** Parsers disagree about ambiguous bodies, so a form-encoded or text payload can be read as JSON or the reverse. That disagreement turns cross-site protections and validation rules into no-ops.

**Detect:** grep route handlers and framework config for explicit content-type rejection (`415`, `UnsupportedMediaType`, `request.is_json`); flag endpoints that parse whatever arrives.

**References:** OWASP REST Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html, CWE-436 Interpretation Conflict

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

# Cross-Field Validation

**MUST** validate semantic relationships between fields — date orderings, totals, and business bounds — not only each field's type and length.

**Why:** A start date after its end date, or a negative quantity, passes per-field checks and then corrupts scheduling, billing, or inventory. Fields are only meaningful in relation to each other.

**Detect:** grep request validators and schemas for cross-field rules (`start < end`, amount bounds, mutually exclusive flags); schemas with type and length checks only are the finding.

**References:** OWASP Proactive Controls C5 (validate all inputs), https://github.com/OWASP/www-project-proactive-controls, CWE-20 Improper Input Validation

# Cross-Layer Path Normalization

**MUST** verify that every component deciding on a URL path — proxy, router, cache, WAF, application — normalizes it identically before enforcing path-based rules.

**Why:** Syntactically valid but inconsistently normalized paths let one layer allow what another denies, bypassing path-matched controls without any traversal sequence.

**Detect:** grep path-matching rules in each layer (`location ~`, `pathPrefix`, route patterns) and compare their trailing-slash, case, and percent-encoding handling.

**References:** OWASP WSTG Path Confusion, https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management/13-Path_Confusion.md

# WebSockets: Upgrade Authentication & Origin Validation (CSWSH)

**MUST** authenticate the upgrade handshake and validate the `Origin` header against an explicit allowlist on every WebSocket connection.

**Why:** WebSockets ignore CORS, so any malicious site can open a socket using the victim's cookies and act as them in real time, streaming private data to the attacker's page.

**Detect:** grep `ws://`, `wss://`, `Upgrade: websocket` upgrade handlers, `onConnection` without origin checks (missing `checkOrigin`/`Origin` validation) or with auth deferred to post-open messages; nginx `proxy_set_header Origin` passthrough config.

**References:** CWE-1385, CWE-346, OWASP A01:2021, OWASP API 2023, RFC 6455 section 10.2

# CSRF

**MUST** Require a per-session token or origin check on every state-changing request.

**Why:** Without it, an attacker's page forges authenticated requests that change user state.

**Detect:** POST/PUT/DELETE routes lacking `csrf_protect`, `X-CSRF-Token`, `SameSite`; `csrf_exempt=True`.

**References:** OWASP A01:2021, CWE-352, OWASP CSRF Prevention Cheat Sheet

# CSV Formula Injection

**MUST** prefix-escape any exported field whose first character is `=`, `+`, `-`, `@`, tab, or CR, following RFC 4180 quoting.

**Why:** A username beginning with `=` executes as a formula when the export is opened in a spreadsheet, giving code execution on the reviewer's machine.

**Detect:** grep export code (`to_csv`, `csv.writer`, `CsvWriter`) for a field-prefix check (`'=`, `"="`, `startswith` guard) and for raw `join(',')` serialization.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md, RFC 4180 (CSV format)

# Debug/Dev Mode in Production

**MUST NOT** ship production with debug mode, verbose traces, interactive debuggers, or profiling endpoints.

**Why:** Traceback pages leak source and secrets; debug consoles allow code execution.

**Detect:** `DEBUG = True`, `FLASK_DEBUG=1`, `app.run(debug`, exposed `/debug`, Werkzeug console.

**References:** OWASP A05:2021, CWE-489, CWE-215

# Decode Before Validate

**MUST** decode input fully, then canonicalize, then validate, so no later step can reinterpret data an earlier check already approved.

**Why:** Validating before decoding lets an encoded payload pass the check and then decode into a dangerous form downstream. Sanitizing instead of rejecting leaves the same gap.

**Detect:** Trace one tainted parameter from ingress to sink: record where decoding, canonicalization and validation happen and confirm that order.

**References:** SAFECode Fundamental Practices v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf, CWE-180

# Decode Once Before Validation

**MUST** decode and normalize input exactly once, before validation, and never after a check has approved it.

**Why:** Decoding after the check re-injects the characters the check removed, so the sanitized value and the used value differ.

**Detect:** grep for decode or normalize calls after validation (`urldecode`, `decodeURIComponent`, `unquote`, `html.unescape`) on the same value.

**References:** OWASP ASVS v5.0 V1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md, CWE-174

# Decompression Bombs & XML Entity Expansion

**MUST** Cap compressed size, decompressed output, and entity expansion depth before and during parsing of untrusted input.

**Why:** A kilobyte zip-bomb or "billion laughs" XML expands to gigabytes, exhausting memory in seconds.

**Detect:** `zipfile.extractall`, `zlib.decompress` without size caps; XML parsers without entity-expansion limits.

**References:** CWE-409, CWE-776, CWE-789

# Disable Setup Endpoints

**MUST** remove or disable installer, setup, and bootstrap endpoints once provisioning completes, and verify they are unreachable afterwards.

**Why:** Setup paths trust whoever reaches them first, so a forgotten one lets a stranger create an administrator account months after install.

**Detect:** grep routes for `setup`, `install`, `bootstrap`, `first-run`, and `wizard`; then curl each on a provisioned instance and expect 404 or 403.

**References:** NVD CVE-2023-22515, https://nvd.nist.gov/vuln/detail/CVE-2023-22515

# Document Processor Escape Hatches

**MUST** disable file-include, shell-escape, and external-fetch features in document and graphics processors, and allow-list the operations users may invoke.

**Why:** Any renderer that shells out or follows includes turns template injection into command execution; the escape hatch exists for convenience, not for untrusted input.

**Detect:** grep for `--shell-escape`, `--enable-write18`, `\write18`, missing `-dSAFER`, and unfiltered `\input{` passthrough in LaTeX/ImageMagick/LibreOffice invocations.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md

# Duplicate Parameter Policy

**MUST** define one duplicate-parameter policy — reject, first-wins, or last-wins — and apply it identically in the validator, the filter, and the handler.

**Why:** Standards leave repeated-field semantics undefined, so a filter and the application can read different values from the same request, and the filter approves what the handler never sees.

**Detect:** grep parameter accessors that silently collapse duplicates (`req.query.x`, `request.args.get`, `getParameter`) and confirm the framework rejects repeated keys.

**References:** OWASP WSTG: HTTP parameter pollution, https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Injection_Testing/, CWE-235 (Parameter Pollution)

# Dynamic Code Evaluation of User Input (eval/exec)

**MUST NOT** pass any externally influenced string to `eval`, `exec`, `Function`, or template code execution.

**Why:** Evaluating attacker-controlled text is remote code execution — full host compromise, no sandbox assumed.

**Detect:** `eval(`, `exec(`, `new Function(`, `compile(`/`__import__` on request data, template rendering of user strings (Jinja `|safe`, `Template(user_str)`), expression evaluators over user input.

**References:** CWE-94, CWE-95, OWASP Injection, OWASP ASVS 5.2

# Dynamic Dispatch Allowlist

**MUST** allowlist the dispatchable targets of any method-by-name, handler-by-string, or plugin-by-name path that touches request data.

**Why:** Dynamic dispatch promotes any attacker-chosen name into an entry point, including internals never meant to be reachable from the edge.

**Detect:** grep for dispatch on request data: `send(params`, `public_send(`, `getattr(obj, request`, `Class.forName(`, `method_call(user_input)`.

**References:** Brakeman: dangerous send, https://brakemanscanner.org/docs/warning_types/, CWE-470 (Unsafe Reflection)

# Email-Template Injection

**MUST** treat user-controlled data interpolated into transactional emails as untrusted: escape HTML, strip/sanitize URLs, and never render user input as links or markup.

**Why:** Usernames or fields containing `<a href="https://phish...">` turn your trusted, DKIM-signed transactional email into a phishing vector your own domain vouches for.

**Detect:** grep mail templates for raw interpolation of user fields (`{{name}}` without escape, `|safe`, `dangerouslySetInnerHTML`); check URL fields are validated against allow-lists before rendering as links.

**References:** CWE-94 code injection in mail templates, OWASP XSS in email clients guidance

# Feature Flags

**MUST NOT** use feature flags as a substitute for access control; authorization checks belong server-side regardless of a flag's state.

**Why:** Toggling a flag off in the UI while the endpoint stays routable exposes unfinished, unauthenticated functionality to anyone who knows the URL.

**Detect:** grep flag SDK calls (`isEnabled(`, `flipper`, `launchdarkly`) wrapped around UI only while routes lack auth middleware; flags defaulting `true` in prod config.

**References:** OWASP ASVS 4.1 access control, CWE-862 missing authorization, Unleash/LaunchDarkly security guidance

# Fetch Metadata Request Policy

**SHOULD** reject state-changing requests whose Fetch Metadata headers declare a cross-site initiator, unless the route is explicitly public.

**Why:** Session cookies travel on cross-site requests, so admission must consult what the browser says about the initiator rather than the token alone.

**Detect:** grep Sec-Fetch-Site in request middleware; no reference means no request-admission policy is enforced

**References:** web.dev Fetch Metadata, https://web.dev/articles/fetch-metadata

# File Upload Validation

**MUST** Check uploads by magic bytes, enforce extension/size limits, store outside the web root with randomized names.

**Why:** Unvalidated uploads accept webshells that execute when fetched from a served directory.

**Detect:** `save(request.files[...])` without type/size checks; uploads under static paths; trusting client `Content-Type`.

**References:** OWASP A03:2021, CWE-434, OWASP File Upload Prevention Cheat Sheet

# Filename Header Encoding

**MUST** generate the download filename server-side and encode it per RFC 6266 rather than echoing the uploaded name.

**Why:** A user-chosen filename reaches a response header, where a newline or quote breaks out of the header or the disposition entirely.

**Detect:** grep for `Content-Disposition` values built from a request filename parameter.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md, RFC 6266 (Content-Disposition), CWE-113

# Forced Browsing & Unprotected Admin Panels

**MUST** authenticate and network-restrict every admin panel, dashboard, and management UI (Kibana, Adminer, /admin, wp-admin, portainer, argocd guest access).

**Why:** Scanners (Nuclei, ffuf) find default-open admin UIs constantly; "security by obscure path" fails against wordlist enumeration.

**Detect:** fuzz paths `/admin`, `/console`, `/kibana`, `/portainer`, `/adminer`; check Nginx/ingress auth annotations and network policies for management routes.

**References:** OWASP WSTG-ATHZ-02, MITRE ATT&CK T1595.001, Nuclei admin-panel templates

# Format String Injection

**MUST** never let untrusted data become the format string itself; pass it only as an argument to a fixed format.

**Why:** Attacker-controlled format strings read or write memory in native code and silently swallow argument mismatches everywhere else.

**Detect:** grep `printf(user`, `fmt.Sprintf(user`, `.format(request`, `% (request`, and `String.format(` calls whose first argument is a variable.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md

# Generic Error Responses

**MUST** return a generic, user-safe error body to clients and keep stack traces, paths, and query fragments in server-side logs only.

**Why:** Stack traces, internal hostnames, and SQL fragments in a response hand an attacker the map of the system for free.

**Detect:** grep response builders for `str(e)`, `traceback.format_exc`, `err.Error()`, `e.getMessage()` serialized into the body, and default framework debug pages reachable in production.

**References:** OWASP Error Handling Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html

# GraphQL Query Depth & Complexity Limits

**MUST** Cap query depth, node count, and alias size, rejecting over-budget queries before execution.

**Why:** Unbounded nesting multiplies resolver calls into denial-of-service from one request.

**Detect:** Server config without `max_depth`/`max_complexity` validation rules; persisted-query-only mode absent; `graphiql` in prod.

**References:** OWASP A04:2021, CWE-770, OWASP GraphQL Cheat Sheet

# Host Header Injection

**MUST** build URLs, cache keys, and routing decisions from the Host header only after validating it against an allow-list.

**Why:** Password-reset links, canonical URLs, and cache entries inherit whatever host the attacker sent, redirecting victims or poisoning shared caches.

**Detect:** grep for `request.host`, `get_host()`, `X-Forwarded-Host`, and URL builders outside the configured base-URL constant.

**References:** OWASP WSTG checklist, https://github.com/OWASP/wstg/blob/master/checklists/checklist.md

# Host Header Trust

**MUST NOT** derive redirect targets, absolute URLs, cache keys, or access decisions from the client-supplied Host header.

**Why:** The Host header is attacker-controlled, so a trusted-host bug turns password-reset and OAuth flows into token exfiltration and poisons caches with the wrong origin. Configure the canonical host instead.

**Detect:** grep `request.host`, `X-Forwarded-Host`, `SERVER_NAME`, and `Host` reads inside URL builders; each must come from configuration, not the request.

**References:** Semgrep rule: request host used, https://github.com/semgrep/semgrep-rules/blob/develop/generic/nginx/security/request-host-used.yaml, CWE-346 Origin Validation Error

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

# Image Dimension Bounds

**MUST** bound decoded pixel dimensions and total pixel count before decoding an image, not just the file's byte size.

**Why:** A small compressed file can decode to gigapixels, so a size limit on the wire passes an image that exhausts memory in the decoder.

**Detect:** grep image decode paths (`Image.open`, `image.Decode`, `sharp(`) for a pixel or dimension limit and for `MAX_IMAGE_PIXELS`-style guards.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md, CWE-400

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

# Input Entry Point Inventory

**MUST** enumerate every data-entry point — network, IPC, files, deep links, clipboard, background sync — and validate each as an untrusted boundary.

**Why:** Teams validate the HTTP API and forget the deep link, the shared file, or the IPC message, each of which reaches the same privileged code. An unlisted entry point never gets reviewed.

**Detect:** judgment: the data-flow diagram or threat model — every entry point listed with its parser, validation, and trust level, cross-checked against platform entry declarations in the app manifest.

**References:** OWASP MASVS-CODE-4 (input validation), https://github.com/OWASP/masvs/blob/master/controls/MASVS-CODE-4.md, OWASP Threat Modeling

# Input Validation

**MUST** Validate all external input against type, length, range, and format allowlists at the trust boundary.
**MUST** validate every inbound payload against an explicit schema (types, required fields, bounds) before any business logic runs.

**Why:** Downstream code assumes validated data; one unchecked field becomes the injection vector, and unvalidated fields let attackers inject unexpected shapes, extra keys, or oversized values that downstream code mishandles.

**Detect:** Handlers reading `request.params`/body straight into logic; missing pydantic/Zod/Joi or `@Valid`; `request.json[...]` read with no validator or JSON Schema, `additionalProperties: true`, mass-assignment from raw body.

**References:** OWASP A03:2021, CWE-20, OWASP Input Validation Cheat Sheet, CWE-915, CWE-1289, OWASP ASVS V5.1.3/V5.1.4, OWASP API1:2023

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

# Learned Allowlists Poison Easily

**MUST** validate a traffic-learned allowlist against a clean baseline before enforcing it, because small contamination poisons the learned profile.

**Why:** A learned profile degrades at fractions of a percent of poisoned requests and then admits the attacker's payload shape as legitimate.

**Detect:** grep WAF and proxy config for learning or auto-tuning modes enabled against production traffic without a filtered training source.

**References:** WAF allowlist poisoning study, https://arxiv.org/abs/2609.06840

# Malware Scan Untrusted Files

**MUST** scan files received from untrusted sources for malware before storing, serving, or processing them further.

**Why:** The application becomes a distribution channel: it stores the payload, serves it from its own origin, and hands it to internal processors.

**Detect:** clamscan on the upload quarantine path; check the upload pipeline for a scan step before the file is promoted.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md, CWE-509

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

# No Plaintext API Endpoints

**MUST** refuse plaintext HTTP on API endpoints rather than redirect it, and scope any unavoidable cleartext exception to named hosts.

**Why:** A redirect still exposes the first request - headers, tokens, payload - to anyone on the path. Clients that follow redirects then resend credentials to the redirect target.

**Detect:** Listeners on port 80 that only `return 301`, plain `http://` upstreams, and `usesCleartextTraffic`/`cleartextTrafficPermitted="true"` without a per-domain exception.

**References:** Mozilla Web Security Guidelines, https://infosec.mozilla.org/guidelines/web_security, OWASP ASVS Communications chapter

# No Silent TLS Upgrade

**MUST** reject cleartext requests on programmatic endpoints rather than redirecting them, so a misconfigured client fails loudly.

**Why:** A redirect turns a broken client into a working one that still believes it is speaking plaintext, hiding the defect until something else relies on it.

**Detect:** grep for 301/308 redirects on `/api`, `/v1`, or RPC routes, and for TLS enforcement implemented only as a redirect rule.

**References:** OWASP ASVS v5.0 V4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x13-V4-API-and-Web-Service.md, CWE-319

# Non-SQL Protocol Injection

**MUST** escape or reject untrusted values before they reach cache keys and mail command parsers.

**Why:** Every protocol has its own metacharacters; a value that is safe in SQL still injects LDAP filters, cache-key namespaces, or SMTP commands.

**Detect:** grep sinks: `memcache.get/set` and Redis key builders using concatenated request values, `sendmail(`, and `SMTP.send_message` built from request data.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md

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

# Outbound Fetch Policy

**MUST** re-apply the outbound destination policy on every redirect and retry, not only to the initial request URL.

**Why:** An allowlist checked once is defeated by a 302 to an internal address or a retry that resolves a new host; only per-hop enforcement covers the whole chain.

**Detect:** grep HTTP client construction for `follow_redirects=True` with no re-validation hook, and for retry policies that re-resolve the original hostname; a policy check performed once before the first request is the finding.

**References:** OWASP SSRF Prevention Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html, CWE-918 Server-Side Request Forgery

# Parameter Source Separation

**MUST** distinguish query, body, cookie, and header parameters, and reject duplicate names where the framework merges them into one value.

**Why:** When validation reads one copy of a duplicated parameter and business logic reads another, every check can be satisfied while the action runs on different input.

**Detect:** grep for merged parameter maps (`request.values`, `request.params`, `getParameterMap`, `ctx.request.body` merged with query) and missing duplicate-parameter rejection.

**References:** OWASP ASVS v5.0 V15.3.7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md, OWASP WSTG: Testing for HTTP Parameter Pollution, CWE-235

# Parser Resource Limits

**MUST** cap structural parser limits - nesting depth, node or element counts, header counts - inside the parser itself, not only the request body size.

**Why:** A small body can still carry a deeply nested or million-element document, and a parser that allocates first has already lost.

**Detect:** grep parser configuration for `max_depth`, `max_nodes`, `max_header`, `max_element_depth`, `XMLConstants.FEATURE_SECURE_PROCESSING`; a parser relying solely on an edge body-size limit is the finding.

**References:** OWASP Denial of Service Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html, OWASP XXE Prevention Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html

# Partial Data Display

**MUST** return and display only the minimum sensitive value the feature needs, masking all but the last few characters by default.

**Why:** Full values in a response or a screen become full values in a screenshot, a support ticket, and a browser cache, for a user who only needed to recognize them.

**Detect:** grep API serializers and templates for full card, account, or identity numbers where a masked form would serve.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x23-V14-Data-Protection.md, CWE-200

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

# Regex Engine Parity

**MUST** verify each validation pattern's behavior on the engine that runs it in production, not on the dialect it was copied from.

**Why:** Engines differ on anchoring, Unicode classes, backreferences and backtracking limits, so a copied validator can accept inputs its author tested as rejected.

**Detect:** Run the pattern corpus under the production engine (RE2, V8, JVM) and diff the results against the dialect the pattern was written for.

**References:** OpenSSF: Correctly Using Regular Expressions, https://best.openssf.org/Correctly-Using-Regular-Expressions, CWE-625

# Regex Full-Match Validation

**MUST** anchor validator patterns to the whole input, so a substring match cannot pass an allowed-format check.

**Why:** Unanchored patterns accept `valid-prefix<script>` because they match somewhere in the string. Bare alternation makes anchors apply to only one branch.

**Detect:** `re.match(`/`re.search(`/`preg_match(`/`Matcher.find()` used for validation without `^...$` or `fullmatch`; alternation lacking a wrapping group.

**References:** OpenSSF: Correctly Using Regular Expressions, https://best.openssf.org/Correctly-Using-Regular-Expressions, CWE-625

# Regex Metacharacter Escaping

**MUST** escape or reject regex metacharacters in user input that becomes part of a pattern.

**Why:** Unescaped input lets the caller inject alternation and quantifiers, turning a search filter into a match-everything bypass or an exfiltration primitive.

**Detect:** grep `new RegExp(`, `re.compile(` and `Pattern.compile(` calls whose argument interpolates a request value rather than a literal.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md

# Reject, Don't Repair

**SHOULD** reject malformed input outright instead of sanitizing or correcting it toward validity and passing the repaired value on.

**Why:** A sanitizer encodes one component's idea of clean, and attackers live in the gap between what it strips and what the next consumer interprets.

**Detect:** grep `sanitize`, `strip_tags`, `escape`, `clean(`, `replace('<'` applied to request data before validation, and handlers that continue after a repair.

**References:** OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

# Relay Address Filtering

**MUST** block relaying or proxying to loopback, link-local, private, and reserved addresses on every supported address family, not only IPv4.

**Why:** A relay that will forward to an internal address is an open proxy into the private network, and IPv6 special ranges are routinely left unhandled.

**Detect:** grep relay/proxy config for peer or destination filtering (`no-multicast-peers`, denied CIDR lists, `allowed_peers`); check whether IPv6 ranges `::1`, `fc00::/7`, `fe80::/10` appear alongside the IPv4 denials.

**References:** OWASP ASVS v5.0 V17.1.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x26-V17-WebRTC.md, CWE-918

# Security Headers

**MUST** Set HSTS, `X-Content-Type-Options: nosniff`, CSP, `Referrer-Policy`, and frame protection on every response.

**Why:** Missing headers leave transport, sniffing, and framing attacks unmitigated.

**Detect:** Config lacking `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`; nginx/ingress snippets absent.

**References:** OWASP A05:2021, CWE-693, securityheaders.com checklist

# Sensitive endpoint exposure (actuator, /admin, .git, .env, debug routes, dashboards)

**MUST NOT** Expose admin panels, actuator endpoints, `.git`/`.env` files, debug routes, or dashboards publicly; gate them behind auth, and **MUST** disable unused framework debug and management endpoints while restricting the rest to authenticated management access (`management.endpoints.web.exposure.include`, `management.server.port`), so `/env`, `/heapdump`, `/phpinfo`, `pprof`, and `/server-status` are never reachable unauthenticated.

**Why:** Leaked `.env` and `.git` hand attackers credentials and full source directly, and debug or management endpoints dump environment variables, heap memory, and internal configuration — a single unauthenticated `/env` request can leak every secret in the service.

**Detect:** Reachable `/actuator`, `/admin`, `/.git/HEAD`, `/.env`, `/server-status`, `/metrics` without auth; grep routes and config for `actuator`, `DEBUG`, `phpinfo`, `pprof`, `django-debug`, and DAST-scan production for `/env`, `/heapdump`, `/debug`.

**References:** OWASP A05:2021, CWE-538, CWE-200, CWE-489, OWASP WSTG-CONF-04, OWASP WSTG-CONF-05

# Served Extension Allowlist

**MUST** configure the web tier to serve only an allowlist of file extensions, so carelessly placed source or configuration files cannot be downloaded.

**Why:** Uploads, editor backups, and deployment artifacts land in the document root, and a permissive handler serves them as text.

**Detect:** grep web-server config for extension allowlisting (`location ~* \.(css|js|png)$`, `FilesMatch`) and for a catch-all static handler.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x22-V13-Configuration.md, CWE-552

# Server-Side Authorization

**MUST** check authorization on every admin or elevated endpoint server-side and **MUST NOT** trust the client for any authorization decision: hidden UI, client route guards, and client-supplied role or permission values are all forgeable, so permissions are re-derived from the authenticated session on every request.

**Why:** Hidden buttons and guarded routes are bypassed by calling the API directly: attackers hit hidden admin endpoints with curl or a proxy, and client-side gating stops no one.

**Detect:** handlers reading role or permission from a request body, header, or unverified token claim; permission flags echoed to the client and trusted back; destructive actions gated only in the frontend router; grep admin routes (`/admin`, `/settings`, `is_admin`, `@require_staff`) for missing auth decorators or middleware and compare UI-hidden actions to unprotected API paths.

**References:** OWASP A01:2021, CWE-862, CWE-269 Improper Privilege Management, OWASP Authorization Cheat Sheet, OWASP ASVS V4.2

# Server-Side Template Injection (SSTI)

**MUST NOT** Render user input as a template; pass it only as context variables, never into dynamic template compilation.

**Why:** Expressions like `{{config}}` evaluate server-side, escalating to remote code execution.

**Detect:** `render_template_string(user_input)`, `Template(request...)`, `format_map` with user strings.

**References:** CWE-1336, OWASP A03:2021, PortSwigger SSTI research

# Signup Abuse Limits

**SHOULD** bound the resources a self-service account can consume — compute, storage, outbound sends, and spend — before payment or verification.

**Why:** Free tiers are farmed for cryptomining, file hosting, and outbound mail, and the operator pays. Per-account ceilings make bulk abuse unprofitable without blocking legitimate signups.

**Detect:** grep signup and quota code for per-account limits on jobs, storage, egress, and email sends; flag flows where verification happens only after resources are consumed.

**References:** OWASP Abuse Case Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html

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

# Strict Parser Rejection

**MUST** reject malformed, ambiguous, or non-canonical input at security-critical parsers instead of tolerating it for interoperability.

**Why:** Tolerant receivers keep non-conformant implementations alive and turn undefined behaviour into a permanent compatibility constraint that cannot be patched.

**Detect:** grep parsers for lenient switches (`strict=False`, `allow_unknown`, duplicate-header tolerance, trailing-garbage acceptance) and for fallback branches that repair bad input.

**References:** NCSC Protocol Design Principles, https://www.ncsc.gov.uk/sites/default/files/2026-06/Protocol-Design-Principles.pdf

# Strict Parsing, No Coercion

**MUST** parse untrusted structured data with a strict schema that rejects unknown fields, duplicate keys, and type coercion.

**Why:** Lenient parsers silently coerce, and the coerced value differs from what the sender meant and from what the validator checked.

**Detect:** grep `additionalProperties: true`, `ignore_unknown_fields`, `strict=False`, `coerce`, `Extra`-allowing serializers, and schema-less `json.loads` on request bodies.

**References:** OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

# Tenant-ID Spoofing at API Boundary

**MUST** derive the tenant from the authenticated session/token on every request — never from a client-supplied tenant_id parameter or header.

**Why:** The classic cross-tenant breach: API trusts `?tenant_id=` from the caller, letting one tenant read or mutate another's data with a valid session.

**Detect:** grep handlers for `tenant_id`/`org_id` read from query params, headers, or request bodies rather than from auth context; check middleware sets tenant once and handlers cannot override.

**References:** OWASP API1:2023 broken object level authorization, OWASP Multi-Tenant Security Cheat Sheet

# Untrusted Forwarded Headers

**MUST NOT** make security decisions from `X-Forwarded-For`, `Referer`, `User-Agent`, or client timestamps without validating the trusted proxy chain.

**Why:** Every one of those headers is client-writable, so an IP allowlist, CSRF check, or rate limit keyed on them is keyed on attacker input.

**Detect:** grep `X-Forwarded-For`, `X-Real-IP`, `Referer`, and `User-Agent` reads that feed allowlists, rate-limit keys, or audit fields; check the proxy config for trusted-proxy depth.

**References:** OWASP HTTP Headers Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html

# Untrusted Lookup Targets

**MUST NOT** let untrusted input choose a name-resolution, class-loading, or remote-fetch target inside an interpreter or template.

**Why:** Lookup mechanisms turn a data field into code or network reach: a logged string becomes an outbound directory request, a filename becomes a loaded class. The attacker chooses what executes or where the request goes.

**Detect:** grep `InitialContext.lookup`, `Class.forName(`, `importlib.import_module`, dynamic `require(`/`import(` with request-derived arguments, and template calls that accept a variable template name.

**References:** Cloudflare Log4j response, https://blog.cloudflare.com/how-cloudflare-security-responded-to-log4j2-vulnerability/, OWASP Injection Prevention Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html, CWE-470 Use of Externally-Controlled Input to Select Classes or Code

# Uploaded Content Serving

**MUST** serve user-uploaded content from a separate origin or object store, never execute or render it inline from the application's own origin.

**Why:** An uploaded HTML or SVG file served from your origin runs with your cookies and origin privileges, turning a file upload into stored script execution. Content inspection alone does not survive every parser differential.

**Detect:** grep upload handlers and static routes for upload directories inside the document root, inline `Content-Disposition`, and missing `X-Content-Type-Options: nosniff`; confirm uploads resolve to a distinct hostname or bucket.

**References:** OWASP File Upload Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html, CWE-434 Unrestricted Upload of File with Dangerous Type

# WASM Host Boundary

**MUST** restrict the host functions a sandboxed module may import to validated, capability-scoped calls, and assume module memory bugs reach them.

**Why:** The sandbox contains crashes, not bad code: an over-permissive host import turns a contained memory bug into host compromise or cross-tenant state leakage.

**Detect:** Read the module's import table and glue code; every host function needs typed, bounded arguments and no ambient filesystem or network authority.

**References:** OWASP WSTG WebAssembly Testing, https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/13-WebAssembly_Testing/00-WebAssembly_Testing_Overview.md

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

# Webhook Signature & Origin Verification

**MUST** verify the provider HMAC over the raw body with constant-time comparison before acting on any webhook, validate the `Origin` header against an explicit allowlist, and treat payload contents — identity fields included — as untrusted input.

**Why:** Unsigned endpoints accept forged events — fake payments, refunds, account changes — from anyone who finds the URL; a handler that trusts payload identity fields blindly is the same exposure, and SaaS signing secrets rotate, so an unverified integration hides the breakage until it fails.

**Detect:** Handlers with no signature check; `hmac.compare_digest` absent; verification skipped in dev branches; no origin check; no idempotency-key dedupe; provider SDK helpers (`constructEvent`) unused; handlers that trust payload identity fields blindly.

**References:** CWE-347, CWE-345, CWE-208, OWASP Webhook Security practices, Stripe/GitHub webhook signing/verification docs

# XSS

**MUST NOT** emit user-controlled data into HTML without context-aware escaping; raw-output helpers and escaping-filter bypasses (`|safe`, `Markup(`, `dangerouslySetInnerHTML`) MUST NOT receive request-controlled data, and user-controlled data MUST NOT be interpolated into server-rendered HTML (`__NEXT_DATA__`, `window.__INITIAL_STATE__`, inline `<script>` blocks, unescaped `{{ }}` templates) without context-aware escaping for script, attribute, and URL contexts.

**Why:** Injected scripts run in victims' sessions, stealing cookies and acting as them; unescaped state serialized into `__NEXT_DATA__` or inline scripts executes on every page load before hydration, bypassing CSP unsafe-inline allowances.

**Detect:** `innerHTML`, `dangerouslySetInnerHTML`, `|safe`, `Markup(` fed by request data; `JSON.stringify` inside `<script>`, `window.__INITIAL_STATE__`, and unescaped `{{ }}` templates in server-rendered HTML.

**References:** OWASP A03:2021, CWE-79, OWASP XSS Prevention Cheat Sheet

# XML External Entity (XXE) Injection

**MUST** Disable external entities and DTD processing in every XML parser (`resolve_entities=False`, secure processing features).

**Why:** Enabled external entities let crafted XML read local files and hit internal networks.

**Detect:** `lxml.etree.parse`, `DocumentBuilderFactory`, `XmlReader` without hardening flags; `DOCTYPE` accepted in inbound XML/SOAP/SVG.

**References:** CWE-611, OWASP A03:2021, OWASP XXE Prevention Cheat Sheet

# 0-RTT Replay Protection

**MUST NOT** accept state-changing requests carried in TLS 1.3 0-RTT early data.

**Why:** An observer replays the early-data request verbatim, and the server performs the purchase, transfer, or deletion a second time.

**Detect:** grep for `ssl_early_data`, `early_data on`, and `Early-Data` handling, then confirm mutating methods are refused until the handshake completes.

**References:** NGINX Admin Handbook, https://github.com/trimstray/nginx-admins-handbook

