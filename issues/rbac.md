# RBAC

**SHOULD NOT** grant permissions directly to individual users; assign roles and bind users to roles only.

**Why:** Direct grants become invisible during audits and are routinely missed at offboarding, leaving orphaned access nobody owns.

**Detect:** grep for user-level GRANT statements (`GRANT ... TO <user>` not `TO ROLE`), IAM policies attached to usernames, `subjects: [User/...]` in K8s RoleBindings.

**References:** OWASP A01:2021, CWE-266 Incorrect Privilege Assignment, NIST SP 800-53 AC-2, RBAC NIST SP 800-162

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
