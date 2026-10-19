# deployment-release — full checklist (29 items)

Release engineering: strategies, environments, versioning.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/deployment-release.md](../categories/deployment-release.md) · Index: [SKILL.md](../SKILL.md)

# Default admin password, signing key and webhook auth on control planes

**MUST** replace a product's shipped default administrative password, set a unique token-signing key, and authenticate every webhook receiver before exposing a self-hosted control plane; ArgoCD's `admin` password and auto-generated `server.secretkey` are the canonical example (CWE-1188).

**Why:** ArgoCD ships with a known default admin and auto-generated signing key; an attacker who reaches the UI or webhook endpoint gains cluster-wide deploy control.

**Detect:** check `argocd-secret` for unchanged `admin.password`, default `server.secretkey`, webhook receivers without `secret`/HMAC verification, `admin.enabled: true` in values.

**References:** ArgoCD Security Guide, CWE-1188, OWASP A05:2021

# Artifact Signing & Verification at Deploy (cosign/sigstore verify before run)

**MUST** verify cosign/sigstore signatures on images and release artifacts at deploy time, rejecting unsigned or mismatched ones.

**Why:** An unsigned image pulled into production may be a tampered one; the deploy boundary is the last honest checkpoint.

**Detect:** grep `cosign verify`, `sigstore`, Kyverno `verifyImages`, `signature_verification: true` in deploy pipelines.

**References:** SLSA Build Level 3, sigstore/cosign docs, NIST SP 800-218 (SSDF), CWE-347

# Blue-Green Deployments

**SHOULD** keep the idle environment patched and drained of live secrets, with automated cutover health gates before traffic shifts.

**Why:** A stale standby environment becomes an unmonitored foothold, and a premature cutover routes users onto unverified code mid-incident.

**Detect:** grep switch scripts for missing health-check gates before service/ingress selector flips; compare standby image tags against the live CVE-patched baseline.

**References:** NIST SP 800-190, AWS Blue/Green deployment guidance, CWE-1188 Initialization of a Resource with an Insecure Default

# Strict Build / Release / Run Separation

**MUST NOT** rebuild per environment: build once, compose config into a versioned release, and promote the identical digest-pinned artifact from staging to production.

**Why:** A per-environment rebuild means the binary that passed staging review is not the binary running in production, silently breaking the review-to-deployment trust chain. Non-promoted builds also make rollbacks unreliable and provenance unverifiable.

**Detect:** CI jobs that build separately per environment; `:latest` tags used across environments; config compiled at build time instead of injected at release time; production digests that cannot be traced to the reviewed staging digest.

**References:** 12factor.net/build-release-run, SLSA Build L2+ provenance, OpenSSF artifact promotion guidance

# Canary Releases

**SHOULD** gate canary traffic expansion on error-rate and latency SLOs with automatic rollback, never on a fixed timer alone.

**Why:** A timer-driven rollout spreads a defect to the whole fleet before anyone notices, turning a small blast radius into a full outage.

**Detect:** grep Argo Rollouts configs for `canary.steps` without an `analysis` step/`analysisTemplates` and for `trafficRouting` without metric-based abort; grep Flagger for `analysis.maxWeight`/`stepWeight` without `threshold` and without `metrics[].thresholdRange`.

**References:** Google SRE Book canarying, NIST SP 800-190, AWS CodeDeploy canary guards, CWE-1095 lifecycle defect

# Code rollback without data rollback causes schema mismatch

**MUST NOT** roll application code back past a schema migration unless that migration is backward-compatible with the old code or a tested compensating migration exists.

**Why:** Migrations move the schema forward while old code expects the old shape: a dropped column or NOT NULL addition makes the rolled-back binary error out or silently write wrong data.

**Detect:** Review migrations paired with the deploy plan: flag destructive changes (`DROP COLUMN`, rename, narrowing types) in the same release; check the scheme is expand-contract — additive first, cleanup after old code is gone.

**Bad:**
```sql
-- release 41: destructive rename (and an index/query that still says `total`)
ALTER TABLE orders RENAME COLUMN total TO amount_cents;
-- rollback to 40: old code queries `total`, which no longer exists
```

**Good:**
```sql
-- expand: add nullable, backfill; contract in a later release
ALTER TABLE orders ADD COLUMN amount_cents bigint;
```

**References:** Fowler Evolutionary Database Design (expand/contract), Marten migration docs, DORA rollback practices

# Debug/Dev Mode in Production

**MUST NOT** ship production with debug mode, verbose traces, interactive debuggers, or profiling endpoints.

**Why:** Traceback pages leak source and secrets; debug consoles allow code execution.

**Detect:** `DEBUG = True`, `FLASK_DEBUG=1`, `app.run(debug`, exposed `/debug`, Werkzeug console.

**References:** OWASP A05:2021, CWE-489, CWE-215

# Deploy Markers on Metrics

**MUST** annotate dashboards and traces with deploy events (version, timestamp, actor) so regressions and incidents can be correlated to releases.

**Why:** Without deploy markers, every incident starts with "what changed?" guessed from memory; attackers exploiting a fresh vulnerable deploy hide behind that ambiguity.

**Detect:** grep CI/CD for annotations pushed to metrics (`deploy_event`, Grafana annotations API, `release` label on series); check dashboards show deploy lines.

**References:** Google SRE Workbook, DORA deploy frequency practices, Grafana annotations docs

# Dual-write plus backfill migration cutover rehearsed

**SHOULD** rehearse the full dual-write → backfill → verify → cutover sequence on a staging copy of production data before running it live, with tested rollback at each phase.

**Why:** These migrations have four independent failure modes — dual-write drift, backfill gaps, verifier blind spots, cutover races — and each discovered in production means reconciling divergent datasets by hand under an outage clock.

**Detect:** Require a runbook with phase gates and a rehearsal log. The verifier must compare full datasets with counts plus checksums, not spot checks; cutover and rollback need dry-run evidence.

**Bad:**
```text
runbook: "write to both DBs, backfill, switch reads"
rehearsal: none — the first live run is the test
```

**Good:**
```text
staging: dual-write 48h → backfill → checksum diff = 0
→ cutover drill → rollback drill, each timed and logged
```

**References:** AWS DMS dual-run/verification guidance, expand-migrate-contract migration pattern docs, NIST SP 800-34 rehearsal requirements

# Environment Parity

**SHOULD** keep dev, staging, and production identical in runtime versions, TLS termination, and network policy so defects surface before prod.

**Why:** Bugs that only exist under production's real configuration — stricter TLS, real auth, actual latency — ship invisible and get discovered by customers.

**Detect:** diff `helm values-*.yaml` across environments for divergent image tags, ingress TLS settings, networkPolicy presence, and connection-pool sizes.

**References:** 12-Factor process parity, NIST SP 800-53 CM-6 configuration settings, Etsy continuous deployment lessons

# Feature Flags

**MUST NOT** use feature flags as a substitute for access control; authorization checks belong server-side regardless of a flag's state.

**Why:** Toggling a flag off in the UI while the endpoint stays routable exposes unfinished, unauthenticated functionality to anyone who knows the URL.

**Detect:** grep flag SDK calls (`isEnabled(`, `flipper`, `launchdarkly`) wrapped around UI only while routes lack auth middleware; flags defaulting `true` in prod config.

**References:** OWASP ASVS 4.1 access control, CWE-862 missing authorization, Unleash/LaunchDarkly security guidance

# GitOps

**MUST** make Git the single source of truth for cluster state, with sync controllers denying out-of-band mutation and requiring signed commits for merge.

**Why:** Unsigned or bypassed changes let an attacker persist malicious workloads that survive incidents and appear legitimate during audits.

**Detect:** check Flux `GitRepository` secretRef/gpgGCM, ArgoCD `signedCrds`/commit verification, and RBAC blocking `kubectl apply` outside the controller service account.

**References:** OWASP Kubernetes Top 10 K04 (centralized policy enforcement), NIST SP 800-190, Sigstore/cosign, Git signed commits

# Manual kubectl apply Drift Not Detected Against Git

**SHOULD** run periodic drift detection (Flux `diff`/`check`, ArgoCD health) that alerts when live cluster state diverges from the reconciled Git revision.

**Why:** A hand-applied manifest silently overrides GitOps intent, so the next sync either reverts an emergency fix or entrenches an unauthorized change unnoticed.

**Detect:** check Flux `Kustomization` for `interval`/`retryInterval` with drift alerts, ArgoCD `syncPolicy.automated` plus `selfHeal: true`; grep for out-of-band `kubectl apply` in audit logs.

**References:** Flux drift detection docs, ArgoCD selfHeal, OWASP K8s misconfiguration, NIST SP 800-190 integrity monitoring

# Release hook ordering and failed-hook release blocking

**MUST** order schema-migration hooks ahead of the workload rollout and treat a failed hook as a release blocker rather than a warning; Helm's `hook-weight` and `hook-delete-policy` annotations are one way to express that ordering.

**Why:** If a DB migration hook fails but the release proceeds, new pods start against an unmigrated schema and corrupt or reject data immediately.

**Detect:** grep chart `helm.sh/hook` annotations for missing `hook-weight` ordering, absent `hook-delete-policy`, and `--no-hooks` flags in CI deploy steps.

**References:** Helm hooks docs, CWE-664 Improper Control of a Resource Through its Lifetime, NIST SP 800-190 change control

# Plaintext Secrets in Helm values Files and Rendered Manifests

**MUST NOT** commit plaintext secrets in `values.yaml` or render them into manifests; reference ExternalSecret/SealedSecret objects or inject at deploy time instead.

**Why:** Values files and `helm get values` output are readable by anyone with repo or release access, leaking credentials through charts and CI artifacts.

**Detect:** `password:`, `apiKey:`, `token:` literals in `values*.yaml`, `helm get values` output containing credentials, missing `existingSecret` references.

**References:** OWASP ASVS V6.4.1, CWE-312, Helm security best practices, Bitnami `existingSecret` pattern

# Immutable Infrastructure (no SSH-and-patch; replace, don't mutate)

**SHOULD NOT** patch running servers over SSH; rebuild and redeploy images so every host matches a known, auditable template.

**Why:** Hand-mutated snowflake hosts hide drift from hardening baselines and can't be trusted or reproduced during incidents.

**Detect:** grep SSH-to-prod patch runbooks vs image pipelines: Packer bake jobs, launch-template updates, `strategy: Recreate`.

**References:** NIST SP 800-53 CM-2/CM-6, CIS Control 2

# Infrastructure as Code

**MUST** define all cloud and cluster resources in version-controlled IaC templates reviewed through pull requests, never via console clicks.

**Why:** Manually created resources drift from policy, escape security review, and cannot be audited or reproducibly rebuilt after compromise.

**Detect:** grep for open security group ingress (`cidr_blocks = ["0.0.0.0/0"]`), unencrypted storage flags, and console-created resources flagged by drift detection.

**References:** AWS Config drift detection, CIS AWS 5.4, IaC Scanning OWASP, Checkov/tfsec baselines

# Infrastructure Drift Detection (live state vs IaC diffed and alerted)

**MUST** continuously diff live infrastructure against IaC definitions and alert on unauthorized manual changes.

**Why:** Console-clicked changes bypass review and become invisible holes — an undocumented open security group never gets fixed.

**Detect:** grep `terraform plan -detailed-exitcode` cron jobs, Driftctl, AWS Config drift rules, `kubectl diff -f`.

**References:** NIST SP 800-53 CM-3/CM-6, CIS Control 2, Terraform drift docs

# Kill-Switch Verification

**SHOULD** test that emergency feature kill-switches actually work (flip in staging, verify behavior) before relying on them in production.

**Why:** An untested kill-switch is a rumor: the flag path may be dead code, the config may not propagate, or the dependency may be the very thing that's failing.

**Detect:** check for scheduled kill-switch drills with recorded results; verify each critical feature has a flag whose off-path is exercised in tests; confirm flag-service outage behavior is a defined, tested state.

**References:** Netflix chaos/kill-switch practice, feature-flag resilience patterns, circuit-breaker companion issue

# Admin Tasks as One-Off Processes from the Release

**SHOULD** run admin and maintenance tasks (migrations, REPLs, one-time scripts) as one-off processes from the same released code, config, and dependency isolation — committed to the repo — rather than ad-hoc scripts executed against production out-of-band.

**Why:** Out-of-band admin access (manual `psql` into prod, hand-copied scripts, SSH one-offs) is unauditable, drifts from the released code's assumptions, and is the classic vector for irreversible mistakes. Running the same image as a scoped one-off Job keeps credentials, code version, and audit trail aligned.

**Detect:** runbooks showing manual DB/console access instead of `kubectl job` or release-hook migrations; admin scripts not present in the repo; production mutations with no corresponding committed task definition.

**References:** 12factor.net/admin-processes, OWASP Logging Cheat Sheet (audit of admin actions), Kubernetes Jobs pattern

# Online schema-change tooling for large tables (gh-ost, pt-osc)

**MUST** use a non-blocking migration strategy for schema changes on tables above a defined size instead of a plain blocking `ALTER TABLE`: gh-ost or `pt-online-schema-change` for MySQL, expand-contract/`pgroll` or concurrent-index patterns for Postgres.

**Why:** A naive `ALTER` on a multi-hundred-gigabyte MySQL table can block writes for the whole copy, freezing writes and cascading timeouts through dependent services — and retrying it mid-outage doubles the damage. (gh-ost/pt-osc are MySQL-only; Postgres 11+ makes `ADD COLUMN` with `DEFAULT` metadata-only, but rewrites still need online treatment.)

**Detect:** Scan migration directories for raw `ALTER TABLE` against known-large tables, missing size thresholds in the runbook, and absence of gh-ost/pt-osc in CI/CD. Migrations should declare expected duration and lock behavior.

**Bad:**
```sql
-- 400 GB table: changing a column's type rebuilds the table and blocks
-- concurrent DML (MySQL 8.0 online DDL: Instant No, Permits Concurrent DML No)
ALTER TABLE orders MODIFY promo_code text;
```

**Good:**
```bash
gh-ost --table=orders --alter="MODIFY promo_code text" \
  --execute   # ghost-table copy, seconds-long cutover
```

**References:** GitHub gh-ost docs (MySQL), Percona pt-online-schema-change docs (MySQL), pgroll docs (Postgres), PostgreSQL CREATE INDEX CONCURRENTLY docs

# Policy-as-Code Enforcement (OPA/Sentinel/CEP gates in CI and admission)

**SHOULD** express security requirements as executable policies (OPA/Rego, Sentinel, Cloud Custodian) enforced in CI and admission, not wikis.

**Why:** Documented policies rot and get ignored; code-enforced gates make non-compliant infrastructure physically unable to deploy.

**Detect:** grep `policy.rego`, `opa check`, `sentinel`, `conftest`, Gatekeeper `ConstraintTemplate`, admission webhook policy configs.

**References:** NIST SP 800-53 CM-6, OPA/Gatekeeper docs, CIS Kubernetes Benchmark 5.2

# Rollbacks

**MUST** be rehearsed, one-command operations whose database migrations are backward-compatible or paired with tested down-migrations.

**Why:** An irreversible schema change pins a broken release in production because rolling back the app would corrupt data, extending outage duration.

**Detect:** grep migration folders for down scripts missing or marked irreversible; check deploy manifests for `revisionHistoryLimit` and `kubectl rollout undo` runbook presence.

**References:** NIST SP 800-34 contingency planning, Fowler Parallel Change

# Semantic Versioning

**MUST** bump major versions for breaking API changes rather than shipping them under a minor tag that consumers assume is safe to auto-upgrade.

**Why:** Dependabot and floating tags auto-adopt a "minor" release that breaks contracts, silently propagating incompatibility across every dependent service.

**Detect:** grep changelogs/tags for `MAJOR`/`MINOR` bumps against diffed public API signatures; check `package.json`/`Cargo.toml` for `^` ranges crossing breaking releases.

**References:** semver.org spec items 7-9, OWASP dependency management, CWE-1265 incorrect version semantics

# Staging Environments

**MUST NOT** populate staging with production data copies unless they are masked, encrypted, and access-restricted to the same degree as prod.

**Why:** Staging typically has weaker auth, logging, and network controls, so a raw prod snapshot leaks real PII through a far softer target.

**Detect:** grep ETL/sync jobs for unmasked `SELECT *` from prod tables into staging; check staging ingress for absent auth, disabled audit logging, open security groups.

**References:** OWASP Top 10 A02:2021 Cryptographic Failures, GDPR Art. 32, CWE-201

# Stale-Flag Expiry Policy

**SHOULD** give every feature flag an owner and expiry; flags past expiry trigger cleanup tickets, and long-lived flags are treated as config debt.

**Why:** Zombie flags accumulate branches that no one understands, each a latent config-drift and dead-code hazard; flag sprawl measurably degrades codebase health.

**Detect:** grep flag definitions for expiry/owner metadata; count flags older than N months without cleanup; check flag service (LaunchDarkly/Unleash) for stale-flag reports and kill dates.

**References:** Feature-Toggle engineering (Fowler), LaunchDarkly stale-flag governance, Unleash flag lifecycle

# Startup Dependency Ordering

**MUST** have services retry with backoff until backends (DB, cache, queues) are reachable, rather than crash-on-first-failure at boot.

**Why:** A pod that dies because the database was seconds from ready enters CrashLoopBackOff, cascading restarts across the fleet during every rolling deploy.

**Detect:** grep readiness/liveness probes and init containers for backend-wait logic; check app boot for missing retry/backoff on connection errors and `initContainers` gating startup.

**References:** Kubernetes init containers & probes docs, AWS retry/backoff patterns, CWE-756 missing custom error handling, resilience4j patterns

# Infrastructure-as-code state kept out of repositories and encrypted at rest

**MUST NOT** commit infrastructure-as-code state to a repository or keep it on an unencrypted disk; use a remote backend with encryption at rest and state locking, and mark secret-bearing variables and outputs `sensitive` so plan output, CI logs, and pull requests cannot echo them. Terraform's `terraform.tfstate` and `terraform output` are the common case; any IaC tool's state artifact is the same class of secret-bearing file.

**Why:** State files and plan artifacts record every resource attribute in plaintext — secrets, resource IDs, network topology — so a leaked backend, backup, or CI log hands over all managed credentials at once.

**Detect:** grep tracked files for `terraform.tfstate`, `*.tfstate.backup`; check the backend block for `backend "s3"` with `encrypt = true` and DynamoDB locking; scan variables and outputs for missing `sensitive = true` and CI steps that print `terraform output`/`terraform plan` unmasked.

**References:** CIS Terraform 1.2/1.3, OWASP Secrets Management, CWE-312, HashiCorp backend security docs

# 12-Factor Apps

**SHOULD** externalize config to the environment and treat processes as stateless, so no secret or session state is baked into images or local disk.

**Why:** Config compiled into images leaks through registry access and forces rebuilds to rotate credentials, slowing response to a compromise.

**Detect:** grep images/repos for hardcoded hosts, ports, and credentials instead of `env`/`ConfigMap`; check for session data written to container filesystem paths.

**References:** 12factor.net config/stateless factors, OWASP Docker Top 10 D06 (Protect Secrets), CWE-798 hardcoded credentials

