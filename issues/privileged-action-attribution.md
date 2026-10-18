# Privileged-Action Attribution

**MUST** ensure every privileged action is attributable to a named individual — no shared admin accounts, no service-account interactive use.

**Why:** Shared root/admin credentials destroy non-repudiation; when an incident happens, "admin did it" is not an answer.

**Detect:** grep for shared `admin`/`root` logins in auth logs config, team password vaults for infra creds, kubectl exec under shared identities; check SSO with per-user identity to admin planes.

**References:** NIST 800-53 AC-6/IA-2, SOX ITGC segregation of duties, CIS 1.5 no shared accounts
