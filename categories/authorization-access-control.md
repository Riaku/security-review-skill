# authorization-access-control

Who may do what: RBAC, RLS, least privilege.

## What this category covers

This category covers the policy layer that decides what an already-identified principal may do: the role model, the grant, the scope, and the review that keeps them honest. The items span application role-based access control and least privilege, database row-level security for tenant-scoped data, cloud IAM (wildcard actions, PassRole chains, cross-account roles without a caller-specific ExternalId), and Kubernetes role bindings (impersonate, bind, and escalate verbs; exec and attach treated as root-in-pod). They also cover manifest-repo privilege mapping, where write access to a manifest repo becomes cluster write access, and the human processes that grant and revoke access: joiners, movers, and leavers, least-used-permission review, just-in-time and break-glass privileged access, and segregation of duties. Expect findings about a grant broader than the workload needs, a path that lets a principal widen its own access, or access that outlives the reason it was granted.

- Application role-based access control: roles bound to users, function-level checks, and vertical privilege escalation.
- Least privilege and entitlement review: observed-use verification, unused-permission pruning, and non-human identity scoping.
- Cloud IAM: wildcard policies, privilege-escalation edges, and cross-account confused-deputy trust.
- Kubernetes and manifest-repo authorization: role escalation verbs, exec and attach, controller scope, and repo-to-cluster privilege mapping.
- Human access lifecycle: revocation on termination or transfer, just-in-time and break-glass access, and segregation of duties.
- Data-layer enforcement: row-level security and tenant scoping in the database rather than only in application queries.

## What it does not cover

- [authentication](../categories/authentication.md) — proving identity and issuing the credential belong there.
- [multi-tenancy](../categories/multi-tenancy.md) — cross-tenant isolation across caches, queues, and offboarding belongs there, beyond the database policy itself.
- [secrets-crypto](../categories/secrets-crypto.md) — the key material and credential storage behind an identity belong there.
- [security-practices](../categories/security-practices.md) — organization-level process such as threat modeling, disclosure, and patch timelines belongs there.

## What a finding here looks like

- A role granted wildcard actions or resources, so one leaked credential reaches everything the account can touch.
- A cross-account role whose trust policy accepts any caller because it has no ExternalId or source condition.
- A Kubernetes subject holding bind or impersonate, letting it attach admin to itself.
- An entitlement still active long after the employee transferred or left.
- A query path reading another tenant's rows because authorization lives only in application WHERE clauses.
