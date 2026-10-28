# web-client-security

Browser-side attack surface and defenses.

## What this category covers

This category covers the part of the attack surface that runs in the browser and the platform features it exposes to attackers: markup injection, response headers, cross-origin requests, and the storage and transport of client-side state. Its member items span XSS in both client-rendered and SSR-hydrated markup, CSP and security headers, cookie flags and session fixation, CSRF, CORS, clickjacking, postMessage and WebSocket origin checks, cache poisoning and cache-control directives, browser storage of sensitive data, header injection, DNS rebinding, and third-party script loading. A reviewer here should follow untrusted data from where the browser receives it to where it is parsed, rendered, or cached. The recurring failure is a place where the browser treats attacker-controlled data as trusted: a missing origin check, an unescaped interpolation, or a session token readable by script.

- Markup injection: XSS across client render, SSR/hydration, and script/attribute/URL contexts.
- Response headers: CSP, HSTS, nosniff, Referrer-Policy, frame protection, Cache-Control.
- Cross-origin defenses: CSRF, CORS, WebSocket origin checks, postMessage validation.
- Session and cookie state: Secure/HttpOnly/SameSite flags, fixation, sensitive data in browser storage.
- Client-side secrets: values inlined into the bundle or exposed through public build-time environment variables.
- Client-side cache and runtime integrity: cache poisoning/deception, prototype pollution, DNS rebinding.
- Third-party client embeds: hot-linked CDN subresources and session-replay SDKs that disclose visitor data or capture input without consent.

## What it does not cover

- [web-api-security](../categories/web-api-security.md) — server-side authentication, authorization, and input handling for API endpoints belong there; this category is what the browser enforces and exposes.
- [authentication](../categories/authentication.md) — how identities are proven and sessions are issued and revoked server-side belongs there; cookie flags and fixation on the client side belong here.
- [caching](../categories/caching.md) — cache keying, eviction, and consistency inside your own cache layer belong there; HTTP caching directives and shared-proxy cache attacks belong here.
- [secrets-crypto](../categories/secrets-crypto.md) — where secrets are stored and how cryptographic primitives are used belong there; keeping them out of localStorage/sessionStorage is a boundary here.

## What a finding here looks like

- user input interpolated into an HTML attribute or a `<script>` block without context-aware escaping.
- `dangerouslySetInnerHTML` (or `|safe`, `Markup(`) fed a request-controlled value.
- `Access-Control-Allow-Origin` reflected back alongside `Allow-Credentials: true`.
- a session cookie missing `HttpOnly`, so any XSS can read it.
- `postMessage` handlers acting on `event.data` without checking `event.origin`.
- a `VITE_`/`NEXT_PUBLIC_` variable holding a service-role key, shipped to every visitor in the bundle.
- a replay SDK (`rrweb`, FullStory, Hotjar) initializing without a consent gate or block/mask selectors.
- a stylesheet pulling `fonts.googleapis.com` instead of a self-hosted or same-origin proxy copy.
