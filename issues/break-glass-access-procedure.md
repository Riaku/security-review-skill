# Break-Glass Access Procedure

**SHOULD** define a monitored break-glass path for emergency privileged access: pre-authorized, logged, alerting on use, and reviewed within 24h.

**Why:** Without a sanctioned emergency path, responders improvise with standing admin access — which is either absent in the outage or abused permanently after it.

**Detect:** look for break-glass accounts/policies (AWS IAM break-glass role, Azure PIM emergency access) with alert-on-use and review SLA; check that emergency creds are escrowed (sealed envelope) not casually held.

**References:** Microsoft emergency access accounts, AWS break-glass role patterns, NIST 800-53 AC-2(2)
