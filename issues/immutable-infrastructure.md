# Immutable Infrastructure (no SSH-and-patch; replace, don't mutate)

**SHOULD NOT** patch running servers over SSH; rebuild and redeploy images so every host matches a known, auditable template.

**Why:** Hand-mutated snowflake hosts hide drift from hardening baselines and can't be trusted or reproduced during incidents.

**Detect:** grep SSH-to-prod patch runbooks vs image pipelines: Packer bake jobs, launch-template updates, `strategy: Recreate`.

**References:** NIST SP 800-53 CM-2/CM-6, CIS Control 2
