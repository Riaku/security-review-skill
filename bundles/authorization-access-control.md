# authorization-access-control — full checklist (40 items)

Who may do what: RBAC, RLS, least privilege.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/authorization-access-control.md](../categories/authorization-access-control.md) · Index: [SKILL.md](../SKILL.md)

# Account Graph Blast Radius

**MUST** authorize every feature that links accounts, because one compromised account inherits access through those edges.

**Why:** Family graphs, shared workspaces and org directories turn a single account takeover into access to everyone adjacent to it. The edge is an authorization decision.

**Detect:** Inspect linking features (invites, shared folders, org membership): each edge is authorized on both sides and revocable.

**References:** arXiv:2502.04303, https://arxiv.org/abs/2502.04303

# Admin Plane Separation

**SHOULD** run administrative interfaces on a separate plane from user traffic, with their own authentication, network reachability, and audit stream.

**Why:** Admin surfaces are the highest-value target, and sharing the user plane means one user-plane bug, session, or WAF bypass reaches them.

**Detect:** grep route/host definitions and ingress rules — whether `/admin`, actuator, and management ports share the user-facing host, auth middleware, and log stream.

**References:** OWASP Access Control Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html

# Admin Reset Blindness

**MUST** let administrators trigger a password reset without ever setting, viewing, or learning the user's password.

**Why:** An admin who knows the user's password destroys non-repudiation: every later action by that account is plausibly the administrator's.

**Detect:** grep admin endpoints for a `new_password` or generated-password field targeting another user id.

**References:** OWASP ASVS v5.0 V6.4.6, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md

# Agent Tool Authorization

**MUST** enforce authorization for agent tool execution outside the agent's own decision context, never from a flag the agent sets for itself.

**Why:** Anything inside the model's context is attacker-influenceable through prompt injection, including an 'approved' flag. Enforcement must live in the component that actually executes the call.

**Detect:** grep tool-execution code for approval checks that read agent-supplied arguments, prompt state, or model output instead of a server-side authorization decision.

**References:** OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html, OWASP Top 10 for LLM Applications (LLM06 excessive agency)

# Authorization Default Deny

**MUST** deny by default: an unmatched rule, missing role, or empty policy resolves to refusal, never to allow.

**Why:** Default-allow turns every forgotten rule into an open door, and an unloaded or empty permission set is the most common way that happens.

**Detect:** grep policy functions whose fall-through returns `True`/`allow`, `if not denied` guards, and permission lookups where `None` or `[]` is treated as unrestricted.

**References:** OWASP Access Control Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html, OWASP Zero Trust Architecture Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Zero_Trust_Architecture_Cheat_Sheet.html

# Authorization Service Degraded Mode

**MUST** design the central authorization service for failure with replication and a documented degraded mode stating what remains allowed and for how long.

**Why:** A security component on every request path without an availability story converts its own outage into a total outage, or into an undocumented allow-all.

**Detect:** read the runbook section for the authorization service and check it states replica count, failure detection, and the exact behaviour (allow, deny, cache) during an outage.

**References:** NIST SP 800-207 §5.2, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 CP-2

# Cloud IAM Privilege Escalation Paths

**MUST** trace every newly granted cloud permission for escalation edges before merge: actions that let a principal widen its own access.

**Why:** One overlooked `PassRole` or `AttachPolicy` grant turns a low-privilege service account into an administrator-in-waiting — the most common path from foothold to full account takeover. Escalation rarely arrives as one obvious admin grant; it hides in combinations (PassRole plus a role that trusts you, or a wildcard that later resolves to a new powerful action), so the diff must be judged against what the principal already holds.

**Detect:** In IAM JSON and IaC, look for `iam:PassRole`, `iam:AttachUserPolicy`, `iam:CreateAccessKey`, `iam:UpdateLoginProfile`, GCP `setIamPolicy`, and bindings referencing wildcards; check whether managed-policy attachments or GCP folder/organization inheritance silently widen the effective set, and whether any `NotAction` or `Resource: "*"` will be inherited by future service launches. Tools: Cloudsplaining, PMapper, IAM Access Analyzer — diff the reachable-permissions graph before/after the change. Periodically recompute the full role-to-role and cross-account escalation graph and prune every path from low privilege to admin.

**Bad:**
```json
{"Effect": "Allow", "Action": ["iam:AttachRolePolicy", "iam:PassRole"], "Resource": "*"}
```

**Good:**
```json
{"Effect": "Allow", "Action": "iam:PassRole",
 "Resource": "arn:aws:iam::111122223333:role/deploy-app",
 "Condition": {"StringEquals": {"iam:PassedToService": "lambda.amazonaws.com"}}}
```

**References:** CWE-269, MITRE ATT&CK T1548.005, Cloudsplaining, AWS IAM Security Best Practices, GCP Policy Analyzer

# Complete Mediation at a Chokepoint

**MUST** route every access to every resource through one enforcement point that no request path can bypass.

**Why:** An attacker simply takes the unchecked path, so a control enforced on most routes is equivalent to no control at all.

**Detect:** grep handlers that fetch a record (`findById(`, `get_object_or_404(`, raw `SELECT`) with no `authorize(`, `can(`, or policy call in the same function.

**References:** OWASP Access Control Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html, Saltzer & Schroeder, The Protection of Information in Computer Systems (1975), https://web.archive.org/web/2023/https://dl.acm.org/doi/10.1145/359545.359563

# Composite Privilege from Innocuous Operations

**MUST** review and audit the low-privilege operations around a protected asset in combination, because individually harmless edits compose into privilege the operator does not otherwise hold.

**Why:** Address change, card issue, and address revert are each harmless alone and amount to account takeover in sequence, and audits covering only sensitive-sounding operations miss it.

**Detect:** judgment: the admin operation inventory, enumerated as sequences that reach a sensitive outcome

**References:** Anderson, Security Engineering 3rd ed., ch.12, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch12.pdf

# Confused Deputy: Cross-Account Roles Without ExternalId or Source Conditions

**MUST** require a caller-specific `sts:ExternalId` (or equivalent source-account/source-ARN conditions) in the trust policy of every cross-account role, so third parties cannot trick the role into acting on another customer's behalf.

**Why:** Without an ExternalId, any account that learns the role's ARN can ask the STS to assume it — the "deputy" cannot tell which client actually requested the action, letting one tenant read or modify another's resources.

**Detect:** Review trust policies (`assume_role_policy` in Terraform, `AssumeRolePolicyDocument` in CloudFormation) for cross-account principals lacking a `Condition` block on `sts:ExternalId`, `aws:SourceArn`, or `aws:SourceAccount`. Check partner-integration docs and IaC modules that accept a bare `principal_arn` parameter with no external-id input.

**Bad:**
```json
"Principal": {"AWS": "arn:aws:iam::999988887777:root"}
```

**Good:**
```json
"Principal": {"AWS": "arn:aws:iam::999988887777:root"},
"Condition": {"StringEquals": {
  "sts:ExternalId": "acme-tenant-42",
  "aws:SourceArn": "arn:aws:events:us-east-1:999988887777:rule/nightly-sync"}}
```

**References:** AWS Confused Deputy Prevention Guide, CWE-441, AWS Security Best Practices SEC3-BP05

# Dangerous IAM Policies (admin/*, *:*, PassRole chains flagged by policy linting)

**MUST NOT** grant wildcard actions/resources (`*:*`, `admin/*`) or unscoped PassRole; linters must fail CI on them.

**Why:** Over-broad grants turn one leaked credential into full account takeover; IaC makes the blast radius reproducible across every environment the module touches, and PassRole hides escalation inside "read-only" roles.

**Detect:** Grep IAM JSON for `"Action": "*"`, `"Resource": "*"`, bare `iam:PassRole`, `AdministratorAccess`. Lint Terraform `aws_iam_policy`/`google_service_account_iam_*`, CloudFormation `AWS::IAM::Policy`, and Pulumi policy docs for wildcards and modules that accept `policy_json` verbatim; run Cloudsplaining or `tfsec`/`checkov` IAM rules in CI and flag any policy the analyzer reports as admin-equivalent.

**References:** AWS IAM best practices, CWE-269, NIST SP 800-53 AC-6, Cloudsplaining, GCP Policy Intelligence, CIS AWS 1.16

# Permissions From Declared Operation

**MUST** derive the runtime permission of a tool invocation from the operation it declares, not from the ambient rights of the approving process.

**Why:** Approving a narrow action while handing the executor broad host access creates a laundering channel where steered arguments reach files outside the declared scope.

**Detect:** grep tool and plugin host config for ambient grants applied to per-call execution (`privileged: true`, `--mount`, `cap_add`, `seccomp=unconfined`) where the declared operation needs none.

**References:** My Credentials, Please: tool approval scope laundering, https://arxiv.org/abs/2610.22301

# Dual Approval Irreversible

**MUST** require two independent approvers for high-value, irreversible actions such as large transfers, contract approvals, or safety overrides.

**Why:** A single actor who can both initiate and release an irreversible action is indistinguishable from an attacker holding that account.

**Detect:** trace the approval workflow and confirm no single identity can complete both the request and the release step.

**References:** OWASP ASVS v5.0 V2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x11-V2-Validation-and-Business-Logic.md, NIST SP 800-53 AC-5

# Dual Control High-Impact Ops

**MUST** require two independently authenticated approvals for high-impact operations so no single credential can complete them alone.

**Why:** One compromised or malicious credential should never be enough to delete data, move money or ship a release. Independent conditions bound what one identity can do.

**Detect:** List destructive operations (data deletion, payouts, production deploy, key rotation) and check each demands a second approver distinct from the requester.

**References:** OWASP Developer Guide: Security Principles, https://github.com/OWASP/DevGuide/blob/main/docs/en/02-foundations/03-security-principles.md

# Exact-Match Authorization Strings

**MUST** compare roles, scopes, token claims, and paths by exact equality; never decide authorization with prefix, suffix, or substring matching.

**Why:** A startsWith("admin") check accepts administrator-disabled, and case folding silently widens the accepted set beyond the intended value.

**Detect:** grep startsWith(, endsWith(, includes(, HasPrefix, Contains( on role, claim, or path variables next to authorization code

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook

# Feature-Level Authorization

**MUST** check authorization against a named permission for the specific action, never a bare role string such as `role == "admin"`.

**Why:** `is_admin`-style checks re-hardcode the permission map into code, so every new feature silently inherits whatever the role string allows.

**Detect:** grep for role-string comparisons in handlers (`role == "admin"`, `isAdmin`, `user.role in (`) guarding feature or record-level operations.

**References:** OWASP ASVS v5.0 V8.2.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md

# Field-Level Authorization

**MUST** enforce read and write authorization per field, including rules that depend on the object's current state.

**Why:** Object-level checks let a caller who may read a record also read or write the fields reserved for another role or for a later stage.

**Detect:** grep serializers and update handlers for object-level-only checks and for a per-field policy map keyed by state.

**References:** OWASP ASVS v5.0 V8, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md, CWE-863

# GitOps Controller Running as cluster-admin

**SHOULD** scope GitOps controllers (Flux, ArgoCD) to least-privilege per-namespace roles instead of the blanket `cluster-admin` ClusterRoleBinding.

**Why:** A compromised repo, PR, or controller CVE becomes instant full-cluster takeover when the sync engine holds cluster-admin.

**Detect:** grep deploy manifests for `cluster-admin` bound to `system:serviceaccount:flux-system` / `argocd`; check ClusterRoleBinding subjects and reconciliation scopes.

**References:** OWASP A05 Security Misconfiguration, CWE-250 Execution with Unnecessary Privileges, ArgoCD security docs, NIST SP 800-190

# GitOps Repo Write Access Equals Cluster Write Access

**MUST** treat write access to a GitOps repo as production cluster admin and restrict it accordingly with review, CODEOWNERS, and separation of duties.

**Why:** Anyone who can commit manifests can create privileged workloads or read cluster secrets without ever touching the cluster API.

**Detect:** Repo without CODEOWNERS on `manifests/` or `apps/`; ArgoCD/Flux repo write granted to broad teams; no admission policy blocking high-privilege kinds from Git.

**References:** OWASP GitOps Security, CWE-269, NIST SP 800-218 (SSDF), ArgoCD RBAC best practices, Flux multi-tenancy guide

# Independent Conditions for Irreversible Actions

**MUST** require irreversible high-consequence actions to satisfy independent authorization, environment, and intent conditions drawn from different trust domains before executing.

**Why:** A single compromised credential or channel then cannot trigger the action alone, however privileged that compromise is.

**Detect:** judgment: the authorization flow for the destructive action — count the independent conditions and their sources

**References:** Anderson, Security Engineering 3rd ed., ch.15, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch15.pdf

# Joiner-mover-leaver access revocation (offboarding and role change hygiene)

**MUST** revoke all access within a defined SLA (24h) on termination, and re-evaluate entitlements on every internal transfer — movers are as risky as leavers.

**Why:** Stale accounts are the top initial-access vector in breaches; role changes silently accumulate permissions nobody removes.

**Detect:** audit exports comparing HR roster to IdP groups; grep for active accounts with no recent login, local admin accounts outside SSO, orphaned SSH keys and API tokens.

**References:** NIST SP 800-53 AC-2(j) account monitoring, CWE-287, OWASP A07:2021, Cloud Security Alliance JML guidance

# exec/attach/debug RBAC Verbs Are Root-in-Pod Equivalent

**MUST NOT** grant `pods/exec`, `pods/attach`, or `pods/debug` broadly; restrict them to named break-glass groups with audit.

**Why:** exec into a pod bypasses every app-layer control — anyone with the verb reads secrets, env vars, and tokens as the workload's user.

**Detect:** grep ClusterRole/Role YAML for `exec`, `attach`, `debug` verbs on `pods`/`pods/exec`; check who can `kubectl exec` via `kubectl auth can-i create pods/exec --as=...`.

**References:** Kubernetes RBAC docs, CWE-269, MITRE ATT&CK T1609 Container Administration Command, NIST SP 800-190

# K8s RBAC Escalation via impersonate/bind/escalate Verbs

**MUST NOT** grant `impersonate`, `bind`, or `escalate` verbs to non-admin subjects; each is a direct path to cluster-admin.

**Why:** `bind` lets a user attach cluster-admin to themselves, `impersonate` borrows any identity, `escalate` upgrades any role — self-grant with no audit trail of intent.

**Detect:** `kubectl auth can-i --list` and grep ClusterRole YAML for `impersonate`, `bind`, `escalate` in verbs; flag RoleBindings to ClusterRole admin.

**References:** RBAC: The Bad Parts (Kubernetes blog), CWE-269, MITRE ATT&CK T1098.006, NIST SP 800-190

# Kubernetes RBAC & NetworkPolicies

**MUST** bind least-privilege RBAC roles and enforce default-deny NetworkPolicies per namespace instead of flat open cluster networking.

**Why:** Cluster-admin bindings and absent network segmentation let any compromised pod read secrets or laterally reach every service.

**Detect:** `ClusterRoleBinding` to `cluster-admin` for app serviceaccounts; no `NetworkPolicy` with `podSelector` matching all ingress in namespace.

**References:** CIS K8s 5.1, RBAC Least Privilege, CWE-284, OWASP Kubernetes Top 10 K03/K07

# Least Privilege

**MUST** grant every service account, role, and credential only the permissions its workload actually uses, verified against observed access rather than assumed needs.

**Why:** Over-broad credentials turn any single compromise into a cluster-wide or account-wide breach.

**Detect:** `cluster-admin`, `roleRef`, `rbac.authorization.k8s.io/v1`, `aws:iam::*:*admin*`, wildcard `"*"` in policy Action/Resource fields.

**References:** OWASP ASVS V1.4.1, CWE-269, NIST SP 800-53 AC-6

# Least-Frequently-Used Permission Review (periodic entitlement pruning)

**SHOULD** periodically revoke entitlements unused over a defined window (e.g. 90 days), starting with the broadest grants.

**Why:** Unused permissions are pure attack surface: they never help legitimate work yet sit ready for any compromised account.

**Detect:** grep access-review exports for `unused_permissions`, `last_used_timestamp`, IAM Access Advisor reports.

**References:** NIST SP 800-53 AC-2(3), CIS Control 5, AWS IAM Access Advisor

# Minimize the Privileged Window

**MUST** acquire elevated privilege as late as possible and drop it immediately after the operation that needs it completes.

**Why:** Every instruction executed while privileged is attack surface for that privilege, so a long window turns a small bug into a privileged one.

**Detect:** grep setuid/seteuid/setresuid sequences and privilege-drop calls, checking that privilege is released before the main loop

**References:** OWASP Go Secure Coding Practices, https://github.com/OWASP/Go-SCP

# No Support Bypass Paths

**MUST NOT** let support, impersonation, or convenience features skip authorization, MFA, or audit logging; treat every such path as privileged.

**Why:** A support backdoor is a documented attack primitive, and 'temporary' bypasses outlive the incident that justified them.

**Detect:** grep `impersonat`, `login_as`, `sudo`, `skip_auth`, `as_user`, and support-role branches that sit above the policy check.

**References:** Saltzer & Schroeder, The Protection of Information in Computer Systems, https://web.mit.edu/Saltzer/www/publications/protection/

# Non-Human Identity Governance (service accounts, machine creds inventoried and scoped)

**MUST** inventory every service account, API key, and machine credential with an owner, least-privilege scope, and expiry.

**Why:** Machine identities outnumber humans 50:1 and are rarely reviewed; orphaned service accounts become attackers' favorite door.

**Detect:** grep `service_account`, `api_key`, `client_secret` inventories, orphaned-credential reports, workload-identity configs.

**References:** NIST SP 800-63B, CIS Control 6, OWASP Non-Human Identities Top 10, CSA NHI guidance

# Object Authorization Beyond Spec

**MUST** treat an API specification's security schemes as evidence of authentication only, and verify object-level authorization separately in code and tests.

**Why:** Schema languages describe shape and transport authentication only, so a spec that looks covered ships endpoints with no per-object ownership check at all.

**Detect:** list endpoints declared in the spec, then grep their handlers for an ownership or policy check on the referenced object.

**References:** Object authorization in web API specifications (arXiv 2212.06606), https://arxiv.org/abs/2212.06606

# Pending Dual-Approval State

**MUST** persist partially approved transactions in a store protected like the action itself, with expiry, cancellation rules, and visibility limited to the approvers.

**Why:** Dual control is not atomic: between the two sign-offs the half-approved request is state an attacker can replay, cancel, or complete.

**Detect:** judgment: the approval workflow's pending table and who may read, cancel, or extend its entries

**References:** Anderson, Security Engineering 3rd ed., ch.12, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch12.pdf

# Policy Store Change Control

**MUST** restrict writes to the authorization policy store to dedicated administrators and log every policy change for review.

**Why:** Whoever can edit the policy decides every access decision, so an unreviewed policy edit is a silent grant of everything the policy covers.

**Detect:** kubectl auth can-i update on the policy custom resource for each subject; audit-log query for writes to policy objects.

**References:** NIST SP 800-207 §5.1, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 AU-9

# Privileged access management: JIT access, break-glass, session recording

**SHOULD** issue privileged access just-in-time with expiry and approval, and record break-glass sessions for review.

**Why:** Standing admin credentials are always in an attacker's blast radius; JIT shrinks the window and recordings make misuse provable.

**Detect:** grep for long-lived admin API keys, shared root SSH access, `sudo` without logging; check PAM tool coverage, session-recording config, break-glass runbook existence.

**References:** NIST SP 800-53 AC-6(1)(2)(9) least privilege + JIT, CWE-250, OWASP A07:2021 Identification and Authentication Failures

# RBAC

**SHOULD NOT** grant permissions directly to individual users; assign roles and bind users to roles only.

**Why:** Direct grants become invisible during audits and are routinely missed at offboarding, leaving orphaned access nobody owns.

**Detect:** grep for user-level GRANT statements (`GRANT ... TO <user>` not `TO ROLE`), IAM policies attached to usernames, `subjects: [User/...]` in K8s RoleBindings.

**References:** OWASP A01:2021, CWE-266 Incorrect Privilege Assignment, NIST SP 800-53 AC-2, RBAC NIST SP 800-162

# Row-Level Security

**MUST** enforce row-level security (RLS) or equivalent tenant scoping in the database layer for every multi-tenant table, not only in application queries.

**Why:** A single missed WHERE clause in one code path leaks every tenant's rows; database-enforced policies fail closed instead.

**Detect:** grep for `ENABLE ROW LEVEL SECURITY`, `CREATE POLICY`, tenant_id filters in ORM raw queries; flag tables lacking policies.

**References:** OWASP A01:2021 Broken Access Control, CWE-285, PostgreSQL RLS docs, NIST SP 800-53 AC-3

# Segregation of duties in deploy and production operations

**MAY** allow self-merge of production deploys only where compensating controls (automated policy checks, mandatory review bots) exist; otherwise require an independent approver.

**Why:** A single engineer pushing unreviewed changes to production removes the last human check before a mistake or malicious change ships.

**Detect:** check branch protection: `required_approving_review_count`, CODEOWNERS on deploy manifests, whether the same identity authors and approves releases or holds both write and deploy roles.

**References:** NIST SP 800-53 AC-5 Separation of Duties, CWE-268 Privilege Chaining, OWASP ASVS V1.4, SLSA provenance requirements

# Separation of Privilege

**MUST** require two independent conditions, such as a permission plus a second approval or factor, before any destructive or high-value operation.

**Why:** A single check that is buggy, phished, or over-granted hands over the whole operation; independent conditions fail independently.

**Detect:** grep destructive handlers (`delete`, `transfer`, `refund`, `role`, `key`) guarded only by one `is_admin`/`has_role` call, with no approval or step-up call nearby.

**References:** Saltzer & Schroeder, The Protection of Information in Computer Systems (1975), https://web.archive.org/web/2023/https://dl.acm.org/doi/10.1145/359545.359563

# Server-Side Authorization

**MUST** check authorization on every admin or elevated endpoint server-side and **MUST NOT** trust the client for any authorization decision: hidden UI, client route guards, and client-supplied role or permission values are all forgeable, so permissions are re-derived from the authenticated session on every request.

**Why:** Hidden buttons and guarded routes are bypassed by calling the API directly: attackers hit hidden admin endpoints with curl or a proxy, and client-side gating stops no one.

**Detect:** handlers reading role or permission from a request body, header, or unverified token claim; permission flags echoed to the client and trusted back; destructive actions gated only in the frontend router; grep admin routes (`/admin`, `/settings`, `is_admin`, `@require_staff`) for missing auth decorators or middleware and compare UI-hidden actions to unprotected API paths.

**References:** OWASP A01:2021, CWE-862, CWE-269 Improper Privilege Management, OWASP Authorization Cheat Sheet, OWASP ASVS V4.2

# Spec-Derived Authorization Tests

**MUST** generate object-level authorization tests from the API specification, crossing each identity with every object identifier it must not reach.

**Why:** Reviewers cannot reliably remember which endpoints own objects, so unscoped lookups pass review and surface only when one customer reads another's record.

**Detect:** command generate cases from the OpenAPI spec (`schemathesis`) pairing token A with object IDs owned by B, and fail on any 2xx.

**References:** Spec-driven IDOR/BOLA test generation, https://arxiv.org/abs/2201.10833, CWE-639 (Authorization Bypass Through User-Controlled Key)

# Subject Authority Propagation

**MUST** carry the originating subject's authority through service chains, so downstream decisions use that subject's permissions rather than the intermediary's.

**Why:** When a middle service calls downstream with its own machine credentials, every downstream check authorizes the service and the user's limits vanish.

**Detect:** grep downstream clients for machine-credential auth (`client_credentials`, `service_account`, `AssumeRole`) on calls that act for an end user.

**References:** OWASP ASVS v5.0 V8, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md, CWE-441

