---
categories: [authorization-access-control]
domains: [backend]
---

# No Support Bypass Paths

**MUST NOT** let support, impersonation, or convenience features skip authorization, MFA, or audit logging; treat every such path as privileged.

**Why:** A support backdoor is a documented attack primitive, and 'temporary' bypasses outlive the incident that justified them.

**Detect:** grep `impersonat`, `login_as`, `sudo`, `skip_auth`, `as_user`, and support-role branches that sit above the policy check.

**References:** Saltzer & Schroeder, The Protection of Information in Computer Systems, https://web.mit.edu/Saltzer/www/publications/protection/
