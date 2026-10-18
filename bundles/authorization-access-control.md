# authorization-access-control — full checklist (18 items)

Who may do what: RBAC, RLS, least privilege.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [authorization-access-control](../categories/authorization-access-control.md) · index: [SKILL.md](../SKILL.md)

# Human-in-the-loop approval for destructive agent tool calls

**MUST** require explicit human confirmation before an autonomous agent executes destructive actions (deletes, payments, sends, deploys).

**Why:** A hijacked or hallucinating agent with unguarded write access can cause irreversible damage in a single automated chain.

**Detect:** agent tool registry lacks confirm/approval flags on destructive verbs; auto-execute=true on write-capable tools.

**References:** OWASP LLM06:2025, NIST AI RMF GOVERN 3, CWE-807

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Cloud IAM Privilege Escalation Paths

**MUST** trace every newly granted cloud permission for escalation edges before merge: actions that let a principal widen its own access.

**Why:** One overlooked `PassRole` or `AttachPolicy` grant turns a low-privilege service account into an administrator-in-waiting — the most common path from foothold to full account takeover. Escalation rarely arrives as one obvious admin grant; it hides in combinations (PassRole plus a role that trusts you, or a wildcard that later resolves to a new powerful action), so the diff must be judged against what the principal already holds.

**Detect:** In IAM JSON and IaC, look for `iam:PassRole`, `iam:AttachUserPolicy`, `iam:CreateAccessKey`, `iam:UpdateLoginProfile`, GCP `setIamPolicy`, and bindings referencing wildcards; check whether managed-policy attachments or GCP folder/organization inheritance silently widen the effective set, and whether any `NotAction` or `Resource: "*"` will be inherited by future service launches. Tools: Cloudsplaining, PMapper, IAM Access Analyzer — diff the reachable-permissions graph before/after the change.

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

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Cloud Privilege-Escalation Paths (cross-role/cross-account escalation graph reviewed)

**SHOULD** periodically compute the role-to-role and cross-account escalation graph, pruning every path from low privilege to admin.

**Why:** Individually reasonable grants compose into escalation ladders (create-role, assume-role, modify-trust) no single-policy review catches.

**Detect:** run pmapper `analyze`, cloudsplaining cross-account reports; grep trust policies for `"AWS": "*"`.

**References:** AWS IAM Access Analyzer, NIST SP 800-53 AC-3/AC-6, CWE-269, Cloudsplaining, Azure AD escalation analysis

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

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

**References:** AWS Confused Deputy Prevention Guide, CWE-915, AWS Security Best Practices SEC3-BP05

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Dangerous IAM Policies (admin/*, *:*, PassRole chains flagged by policy linting)

**MUST NOT** grant wildcard actions/resources (`*:*`, `admin/*`) or unscoped PassRole; linters must fail CI on them.

**Why:** Over-broad grants turn one leaked credential into full account takeover; IaC makes the blast radius reproducible across every environment the module touches, and PassRole hides escalation inside "read-only" roles.

**Detect:** Grep IAM JSON for `"Action": "*"`, `"Resource": "*"`, bare `iam:PassRole`, `AdministratorAccess`. Lint Terraform `aws_iam_policy`/`google_service_account_iam_*`, CloudFormation `AWS::IAM::Policy`, and Pulumi policy docs for wildcards and modules that accept `policy_json` verbatim; run Cloudsplaining or `tfsec`/`checkov` IAM rules in CI and flag any policy the analyzer reports as admin-equivalent.

**References:** AWS IAM best practices, CWE-269, NIST SP 800-53 AC-6, Cloudsplaining, GCP Policy Intelligence, CIS AWS 5.28–5.36

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# GitOps Controller Running as cluster-admin

**SHOULD** scope GitOps controllers (Flux, ArgoCD) to least-privilege per-namespace roles instead of the blanket `cluster-admin` ClusterRoleBinding.

**Why:** A compromised repo, PR, or controller CVE becomes instant full-cluster takeover when the sync engine holds cluster-admin.

**Detect:** grep deploy manifests for `cluster-admin` bound to `system:serviceaccount:flux-system` / `argocd`; check ClusterRoleBinding subjects and reconciliation scopes.

**References:** OWASP A05 Security Misconfiguration, CWE-250 Execution with Unnecessary Privileges, ArgoCD security docs, NIST SP 800-190

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [containers-k8s](../categories/containers-k8s.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# GitOps Repo Write Access Equals Cluster Write Access

**MUST** treat write access to a GitOps repo as production cluster admin and restrict it accordingly with review, CODEOWNERS, and separation of duties.

**Why:** Anyone who can commit manifests can create privileged workloads or read cluster secrets without ever touching the cluster API.

**Detect:** Repo without CODEOWNERS on `manifests/` or `apps/`; ArgoCD/Flux repo write granted to broad teams; no admission policy blocking high-privilege kinds from Git.

**References:** OWASP GitOps Security, CWE-269, NIST SP 800-218 PO.3, ArgoCD RBAC best practices, Flux multi-tenancy guide

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Joiner-mover-leaver access revocation (offboarding and role change hygiene)

**MUST** revoke all access within a defined SLA (24h) on termination, and re-evaluate entitlements on every internal transfer — movers are as risky as leavers.

**Why:** Stale accounts are the top initial-access vector in breaches; role changes silently accumulate permissions nobody removes.

**Detect:** audit exports comparing HR roster to IdP groups; grep for active accounts with no recent login, local admin accounts outside SSO, orphaned SSH keys and API tokens.

**References:** NIST SP 800-53 AC-2(j) account monitoring, CWE-288, OWASP A07:2021, Cloud Security Alliance JML guidance

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [compliance-privacy](../categories/compliance-privacy.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# exec/attach/debug RBAC Verbs Are Root-in-Pod Equivalent

**MUST NOT** grant `pods/exec`, `pods/attach`, or `pods/debug` broadly; restrict them to named break-glass groups with audit.

**Why:** exec into a pod bypasses every app-layer control — anyone with the verb reads secrets, env vars, and tokens as the workload's user.

**Detect:** grep ClusterRole/Role YAML for `exec`, `attach`, `debug` verbs on `pods`/`pods/exec`; check who can `kubectl exec` via `kubectl auth can-i create pods/exec --as=...`.

**References:** Kubernetes RBAC docs, CWE-269, MITRE ATT&CK T1611 Escape to Host, NIST SP 800-190

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [containers-k8s](../categories/containers-k8s.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# K8s RBAC Escalation via impersonate/bind/escalate Verbs

**MUST NOT** grant `impersonate`, `bind`, or `escalate` verbs to non-admin subjects; each is a direct path to cluster-admin.

**Why:** `bind` lets a user attach cluster-admin to themselves, `impersonate` borrows any identity, `escalate` upgrades any role — self-grant with no audit trail of intent.

**Detect:** `kubectl auth can-i --list` and grep ClusterRole YAML for `impersonate`, `bind`, `escalate` in verbs; flag RoleBindings to ClusterRole admin.

**References:** RBAC: The Bad Parts (Kubernetes blog), CWE-269, MITRE ATT&CK T1098.001, NIST SP 800-190

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [containers-k8s](../categories/containers-k8s.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Least Privilege

**MUST** grant every service account, role, and credential only the permissions its workload actually uses, verified against observed access rather than assumed needs.

**Why:** Over-broad credentials turn any single compromise into a cluster-wide or account-wide breach.

**Detect:** `cluster-admin`, `roleRef`, `rbac.authorization.k8s.io/v1`, `aws:iam::*:*admin*`, wildcard `"*"` in policy Action/Resource fields.

**References:** OWASP ASVS V1.4.3, CWE-269, NIST SP 800-53 AC-6

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Least-Frequently-Used Permission Review (periodic entitlement pruning)

**SHOULD** periodically revoke entitlements unused over a defined window (e.g. 90 days), starting with the broadest grants.

**Why:** Unused permissions are pure attack surface: they never help legitimate work yet sit ready for any compromised account.

**Detect:** grep access-review exports for `unused_permissions`, `last_used_timestamp`, IAM Access Advisor reports.

**References:** NIST SP 800-53 AC-2(3), CIS Control 5, AWS IAM Access Advisor

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Non-Human Identity Governance (service accounts, machine creds inventoried and scoped)

**MUST** inventory every service account, API key, and machine credential with an owner, least-privilege scope, and expiry.

**Why:** Machine identities outnumber humans 50:1 and are rarely reviewed; orphaned service accounts become attackers' favorite door.

**Detect:** grep `service_account`, `api_key`, `client_secret` inventories, orphaned-credential reports, workload-identity configs.

**References:** NIST SP 800-63B, CIS Control 6, OWASP Non-Human Identities Top 10, CSA NHI guidance

---

**Part of:** [authentication](../categories/authentication.md) · [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Privileged access management: JIT access, break-glass, session recording

**SHOULD** issue privileged access just-in-time with expiry and approval, and record break-glass sessions for review.

**Why:** Standing admin credentials are always in an attacker's blast radius; JIT shrinks the window and recordings make misuse provable.

**Detect:** grep for long-lived admin API keys, shared root SSH access, `sudo` without logging; check PAM tool coverage, session-recording config, break-glass runbook existence.

**References:** NIST SP 800-53 AC-6(1)(2)(9) least privilege + JIT, CWE-250, OWASP A07:2021 Identification and Authentication Failures

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [compliance-privacy](../categories/compliance-privacy.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# RBAC

**SHOULD NOT** grant permissions directly to individual users; assign roles and bind users to roles only.

**Why:** Direct grants become invisible during audits and are routinely missed at offboarding, leaving orphaned access nobody owns.

**Detect:** grep for user-level GRANT statements (`GRANT ... TO <user>` not `TO ROLE`), IAM policies attached to usernames, `subjects: [User/...]` in K8s RoleBindings.

**References:** OWASP A01:2021, CWE-266 Incorrect Privilege Assignment, NIST SP 800-53 AC-2, RBAC NIST SP 800-162

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Row-Level Security

**MUST** enforce row-level security (RLS) or equivalent tenant scoping in the database layer for every multi-tenant table, not only in application queries.

**Why:** A single missed WHERE clause in one code path leaks every tenant's rows; database-enforced policies fail closed instead.

**Detect:** grep for `ENABLE ROW LEVEL SECURITY`, `CREATE POLICY`, tenant_id filters in ORM raw queries; flag tables lacking policies.

**References:** OWASP A01:2021 Broken Access Control, CWE-285, PostgreSQL RLS docs, NIST SP 800-53 AC-3

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Segregation of duties in deploy and production operations

**MAY** allow self-merge of production deploys only where compensating controls (automated policy checks, mandatory review bots) exist; otherwise require an independent approver.

**Why:** A single engineer pushing unreviewed changes to production removes the last human check before a mistake or malicious change ships.

**Detect:** check branch protection: `required_approving_review_count`, CODEOWNERS on deploy manifests, whether the same identity authors and approves releases or holds both write and deploy roles.

**References:** NIST SP 800-53 AC-5 Separation of Duties, CWE-265 Privilege Roles Conflict, OWASP ASVS V1.4, SLSA provenance requirements

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Vertical Privilege Escalation / Function-Level Authorization

**MUST** check authorization on every admin or elevated endpoint server-side; never rely on hiding buttons or menus in the UI.

**Why:** Attackers call hidden endpoints directly (IDOR-style), and client-side gating stops no one with curl or a proxy.

**Detect:** grep admin routes (`/admin`, `/settings`, `is_admin`, `@require_staff`) for missing auth decorators/middleware; compare UI-hidden actions to unprotected API paths.

**References:** OWASP A01:2021, CWE-269 Improper Privilege Management, CWE-862 Missing Authorization, OWASP ASVS V4.2

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

