---
categories: [api-design]
domains: [backend, infrastructure]
---

# Bounding Protocol Element Lengths

**MUST** cap the length of every parsed protocol element — method, header name and value, status phrase, numeric field, chunk size — not only the body.

**Why:** Unbounded element parsing is the substrate for arithmetic and buffer overflows, and the spec's own limits are minima rather than safe defaults.

**Detect:** grep edge and server config for header limits (`large_client_header_buffers`, `max-http-header-size`, `LimitRequestFields`) and flag services that limit bodies but not headers.

**References:** RFC 9110 HTTP Semantics, https://httpwg.org/specs/rfc9110.html
