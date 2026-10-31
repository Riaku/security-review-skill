# web-api-security

Server-side API and web application attack surface.

## What this category covers

This category exists for attacks that arrive over the network at a server-side HTTP surface: injection into queries, commands, templates, and deserializers; request-framing and header abuse; broken object- and function-level enforcement at the endpoint; and the browser-facing responses that confine what a compromised page can do. The items span input validation and injection sinks (SQL, NoSQL, LDAP, OS command, template, XML, and native deserialization), file and path handling, request smuggling and cache poisoning, server-side request forgery into cloud metadata, and the security headers, content security policy, strict transport security, cross-origin resource sharing, cross-site request forgery, and frame-embedding controls that shape the response. They also cover exposure of admin and debug surfaces, rate limiting, bot defenses, and third-party webhook trust. Expect findings that are concrete at the request boundary: a handler that concatenates input into a query, a response missing a security header, or a route that never reaches an authentication check.

- Injection and input validation sinks across query languages, shell commands, template engines, XML parsers, and deserializers.
- Request framing and header abuse: request smuggling, CRLF injection, cache poisoning, and cache deception.
- Browser-facing response controls: security headers, content security policy, strict transport security, cross-origin resource sharing, cross-site request forgery, frame embedding, and cross-site scripting.
- Broken object-level and function-level enforcement at the endpoint, including mass assignment and routes outside the default-deny allowlist.
- Server-side request forgery, cloud metadata access, open redirect, and path traversal.
- Abuse controls: rate limiting, bot challenges, and inbound webhook signature and replay handling.

## What it does not cover

- [authentication](../categories/authentication.md) — credential verification, login flows, and session or token lifecycle belong there, even when they terminate at the same endpoints.
- [authorization-access-control](../categories/authorization-access-control.md) — role and policy models, least privilege, and privilege-escalation paths belong there; this category holds the per-endpoint enforcement gap.
- [web-client-security](../categories/web-client-security.md) — browser-side rendering, DOM sinks, and client storage controls belong there rather than at the server response.
- [api-design](../categories/api-design.md) — versioning, status-code contracts, and transport selection belong there rather than the attack surface they expose.

## What a finding here looks like

- A request parameter concatenated into a SQL or LDAP query string, letting a caller return rows or entries the query never intended.
- An authenticated response that ships without frame protection, strict transport security, or content-type sniffing protection.
- A route reachable without authentication because it was never added to the default-deny allowlist.
- A user-supplied URL fetched server-side without blocking internal ranges after name resolution.
- A signed webhook accepted repeatedly because no timestamp window or nonce check rejects replays.
- A sink cleared because the value reached it through a helper or wrapper class rather than a request accessor.
