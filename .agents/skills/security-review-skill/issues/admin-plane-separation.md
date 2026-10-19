---
categories: [authorization-access-control]
domains: [backend]
---

# Admin Plane Separation

**SHOULD** run administrative interfaces on a separate plane from user traffic, with their own authentication, network reachability, and audit stream.

**Why:** Admin surfaces are the highest-value target, and sharing the user plane means one user-plane bug, session, or WAF bypass reaches them.

**Detect:** grep route/host definitions and ingress rules — whether `/admin`, actuator, and management ports share the user-facing host, auth middleware, and log stream.

**References:** OWASP Access Control Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html
