---
categories: [web-api-security]
domains: [backend]
---

# Fetch Metadata Request Policy

**SHOULD** reject state-changing requests whose Fetch Metadata headers declare a cross-site initiator, unless the route is explicitly public.

**Why:** Session cookies travel on cross-site requests, so admission must consult what the browser says about the initiator rather than the token alone.

**Detect:** grep Sec-Fetch-Site in request middleware; no reference means no request-admission policy is enforced

**References:** web.dev Fetch Metadata, https://web.dev/articles/fetch-metadata
