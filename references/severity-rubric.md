# Severity Rubric

Severity is assigned by the reviewer using the criteria below. Apply them
consistently across categories; when two factors disagree, the higher severity
wins. Severity is about the *finding in this codebase*, not the abstract issue.

## Critical
Actively exploitable as written, or guarantees catastrophic loss.
- Unauthenticated remote code execution, auth bypass, or admin takeover
- Live secret exposed in a public repo/artifact (verified reachable)
- Direct money movement or data destruction without authorization
- Payment integrity broken (e.g. client-controlled amounts accepted)
Exploit exists or is trivially buildable from what you read → critical.

## High
Serious exposure that requires some precondition (valid account, user
interaction, internal network position) but has large blast radius.
- SQLi/SSRF/IDOR on authenticated-but-underprotected endpoints
- Privilege escalation between roles/tenants
- Missing authorization on bulk-data or admin routes
- Weak crypto protecting real data (MD5 passwords, ECB, no salt)
Precondition needed + wide impact → high.

## Medium
Real weakness with contained blast radius, or defense-in-depth failure where
another control currently limits impact.
- Missing rate limit on a sensitive-but-narrow endpoint
- CSRF on state-changing forms (same-site cookies partially mitigate)
- Verbose errors leaking internals useful for attack planning
- Missing security headers with a concrete, reachable abuse case
Contained impact or mitigated-by-luck → medium.

## Low
Hygiene and hardening gaps with no direct exploit path identified.
- Missing best-practice config with no demonstrated abuse
- Theoretical timing side channels on non-secret comparisons
- Stale dependencies with no reachable vulnerable code path
No exploit path found, but the gap is real → low.

## Modifiers
- **Keyword level raises, never lowers:** a violated `MUST` floors at high
  unless the concern is contained (then medium). A violated `SHOULD` caps at
  medium unless it independently meets Critical/High criteria.
- **Data sensitivity raises one level** when the affected data is PII,
  credentials, payment, or health data.
- **Exposure raises one level** when the surface is internet-facing vs
  internal-only.
- **Evidence gates severity:** no `file:line` evidence → the finding is
  `needs-human`, not a guess at any severity.
- `not-applicable` and `pass` carry no severity.
