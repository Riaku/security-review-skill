# Immutable Infrastructure (no SSH-and-patch; replace, don't mutate)

**SHOULD NOT** patch running servers over SSH; rebuild and redeploy images instead, so every host matches a known, auditable template.

**Why:** Snowflake hosts mutated by hand hide rootkits, drift from hardening baselines, and cannot be trusted or reliably reproduced during an incident.

**Detect:** grep for SSH-to-prod runbooks, `apt upgrade` on live hosts vs image pipelines: Packer, AMI bake jobs, `deployment strategy: Recreate`, Auto Scaling group launch templates.

**References:** NIST SP 800-53 CM-2/CM-6, CIS Control 2, Chromebook/immutable-infra pattern, AWS Well-Architected operational excellence
