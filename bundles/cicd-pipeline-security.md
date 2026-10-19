# cicd-pipeline-security — full checklist (25 items)

CI/CD system as an attack surface.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/cicd-pipeline-security.md](../categories/cicd-pipeline-security.md) · Index: [SKILL.md](../SKILL.md)

# Advisory-vs-Enforced Agent Checks

**MUST** implement every must-happen-every-time agent rule as a deterministic hook (pre-commit, post-edit lint, blocked paths, secret-scan-before-write) — not as instruction text the model may skip.

**Why:** The whole ecosystem converged on this distinction: "hooks are deterministic; CLAUDE.md is advisory" (Anthropic). Policy claimed in instruction files with no hook behind it is unenforced policy wearing a costume.

**Detect:** security rules present only in instruction-file text with no corresponding hook/CI enforcement; hook config (e.g. .claude/settings.json) empty while policy claims enforcement.

**References:** Anthropic hooks-vs-instructions guidance, Copilot CLI hooks, Cursor hooks, Codex hooks

# AI-generated code review gate before merge

**SHOULD** require human security review of AI-generated code before merge; Copilot-style output is not self-certifying.

**Why:** Models reproduce vulnerable patterns and plausible-but-broken crypto from training data at high volume and speed.

**Detect:** PRs with AI-assist labels merged without security-review approval; CI lacks a gate matching ai-generated/copilot review policy.

**References:** OWASP LLM05:2025, NIST SSDF PW.7

# Default admin password, signing key and webhook auth on control planes

**MUST** replace a product's shipped default administrative password, set a unique token-signing key, and authenticate every webhook receiver before exposing a self-hosted control plane; ArgoCD's `admin` password and auto-generated `server.secretkey` are the canonical example (CWE-1188).

**Why:** ArgoCD ships with a known default admin and auto-generated signing key; an attacker who reaches the UI or webhook endpoint gains cluster-wide deploy control.

**Detect:** check `argocd-secret` for unchanged `admin.password`, default `server.secretkey`, webhook receivers without `secret`/HMAC verification, `admin.enabled: true` in values.

**References:** ArgoCD Security Guide, CWE-1188, OWASP A05:2021

# Benchmark Scanning in CI (kube-bench, Lynis, Trivy misconfig)

**SHOULD** run kube-bench, Lynis, or Trivy misconfig scans in CI on every image and host config change, failing the pipeline on high-severity findings.

**Why:** Hardening drifts silently after deploy; without automated benchmark gates, regressions ship unnoticed until an attacker exploits them.

**Detect:** Check `.github/workflows/*` or Jenkinsfile for `kube-bench`, `lynis audit`, `trivy config`, `trivy image --scanners misconfig` steps and severity gates.

**References:** CIS Benchmarks, NIST SP 800-53 CM-6, DevSecOps, CWE-1188

# Branch Protection

**MUST** require reviewed, status-passing pull requests before merging into protected branches, with force-push and branch deletion disabled.

**Why:** Unprotected main branches let anyone push unreviewed or malicious code straight into production builds, bypassing every downstream control.

**Detect:** GitHub settings API `branches/*/protection` — check `enforce_admins`, `required_pull_request_reviews`, `required_status_checks`; grep repo scripts for `push --force` to main; missing `.github/settings.yml` `protected_branches`; CODEOWNERS files.

**References:** OWASP CI/CD Top 10 CICD-SEC-1, CWE-284, NIST SP 800-218 (SSDF), GitHub branch protection docs

# Breaking-Change Linting in CI

**SHOULD** lint API changes against the previous published version for breaking changes (removed fields, changed types, new required params) before merge.

**Why:** Hand-review misses subtle contract breaks; automated diffing (oasdiff/buf breaking) catches them at the PR that introduces them, before consumers discover at runtime.

**Detect:** check CI for `oasdiff breaking`, `buf breaking`, `protolint`, or equivalent on API definition files; verify the comparison baseline is the last released version, not main.

**References:** oasdiff, buf breaking-change detection, Google AIP-180 backwards compatibility

# CI Action Pinning (SHA not tag)

**MUST** reference third-party actions by full commit SHA rather than a mutable tag or branch name.

**Why:** A retagged or hijacked tag silently swaps in attacker-controlled code that runs with your workflow's permissions, as the tj-actions incident proved; the same trust-in-mutable-references lesson applies to every unpinned build input — compromised build systems and hijacked packages (SolarWinds, event-stream) show what runs with your pipeline's privileges when an upstream reference is subverted.

**Detect:** Grep `.github/workflows/*.yml` for `uses:` lines matching `@v[0-9]` or `@main` instead of 40-hex SHAs; check for unpinned `curl | bash` installers in Dockerfiles or CI scripts; verify renovate/dependabot pin settings; actionlint `pin-versions` rule.

**References:** CWE-829, NIST SP 800-218 (SSDF), GitHub Actions security hardening guide, OWASP Top 10 CI/CD Security Risks CICD-SEC-3 (Dependency Chain Abuse), NIST SP 800-161

# CI Artifact Integrity Handoff

**MUST** sign built artifacts and verify signatures and checksums before downstream deployment consumes them.

**Why:** Unsigned artifacts can be swapped or tampered with between build and deploy with no way to detect the substitution.

**Detect:** Missing `cosign sign`/`sigstore`/`gpg --sign` steps; deploy jobs pulling images by mutable tag without digest pinning; no `.sha256` or provenance attestations in artifact stores.

**References:** OWASP CI/CD Top 10 CICD-SEC-9, CWE-345, NIST SP 800-218 (SSDF), SLSA provenance levels, sigstore/cosign docs

# CI Deploy-Credential Scoping

**MUST NOT** grant deploy credentials to every workflow; scope each secret and token to the single job and target environment that needs it.

**Why:** Broadly shared deploy keys mean any compromised workflow can push to every environment, including production.

**Detect:** Repo-level `secrets.*` used in many workflows instead of environment-scoped ones; cloud IAM policies with `*` resources attached to CI roles; missing `environment:` stanzas.

**References:** OWASP CI/CD Top 10 CICD-SEC-6, CWE-250, NIST SP 800-218 (SSDF), GitHub environments and OIDC deploy docs

# CI Runner Isolation

**MUST** run untrusted build jobs on ephemeral, per-job isolated runners with no shared workspace, persistent credentials, or network access to production networks.

**Why:** Reused or shared runners let one malicious job harvest secrets and artifacts left behind by previous builds.

**Detect:** Self-hosted runner labels in workflow `runs-on`; persistent `/var/run/docker.sock` mounts; runner config `ephemeral=false`; shared cache dirs across jobs.

**References:** OWASP CI/CD Top 10 CICD-SEC-7, CWE-419, NIST SP 800-218 (SSDF), GitHub Actions security hardening guide

# CI Workflow Injection via Untrusted PR Content (pull_request_target)

**MUST NOT** check out or execute pull request code inside a `pull_request_target` or other privileged-trigger job that holds write tokens or secrets.

**Why:** Attacker-controlled PR text interpolated into shell steps runs arbitrary commands with full repo and secret access.

**Detect:** Grep workflows for `pull_request_target` combined with `secrets.`, `${{ github.event.* }}` in `run:` blocks, or `checkout` of `github.event.pull_request.head.sha`.

**References:** OWASP CI/CD Top 10 CICD-SEC-4, CWE-94, NIST SP 800-218 (SSDF), GitHub Actions security hardening guide

# Code Review Practice

**MUST** require at least one independent reviewer for every change touching authentication, cryptography, or input handling, with a documented security checklist and a response SLA.

**Why:** Single-author security code ships logic errors and backdoors that a second pair of eyes reliably catches.

**Detect:** CODEOWNERS covering auth/crypto paths, PR templates with security checklist items, branch protection requiring ≥1 approval; self-merged security PRs in git log.

**References:** OWASP ASVS V1.1.7, NIST SP 800-218 (SSDF) (code review), OWASP Code Review Guide v2, CWE-1068 (Inconsistency Between Implementation and Documented Design)

# Docker-in-Docker / Privileged Build Steps in CI

**SHOULD** replace privileged Docker-in-Docker with rootless or daemonless builders (BuildKit, Kaniko, Buildah) since `privileged: true` grants the container host-level control.

**Why:** A privileged build container can escape to the runner host and capture every credential and workload on it.

**Detect:** Grep workflows for `privileged: true`, `docker:dind` images, or volume mounts of `/var/run/docker.sock` into build jobs.

**References:** OWASP Docker Top 10 D01 (Secure User Mapping: never use --privileged), CWE-250, NIST SP 800-218 (SSDF), Kaniko and BuildKit rootless docs, GitLab CI best practices

# Dockerfile Secret Leakage via COPY, Build Args, and Cache Layers

**MUST NOT** bake secrets into images via `COPY` of credential files or plain `ARG`/`ENV` values; use BuildKit `--mount=type=secret` instead.

**Why:** Copied files and build args persist in the final image: copied file contents remain in the saved layers of any pushed image, and ARG/ENV values stay visible in `docker history` and image metadata.

**Detect:** Grep Dockerfiles for `COPY .npmrc`, `COPY *credentials*`, `ARG API_KEY`, `ENV SECRET`, or `RUN ... $ARG` patterns; inspect `docker history` for leaked values.

**References:** OWASP Docker Top 10 D06 (Protect Secrets), CWE-540, NIST SP 800-218 (SSDF), BuildKit secret mounting docs, Trivy secret scanning / Checkov Dockerfile checks

# GitOps Repo Write Access Equals Cluster Write Access

**MUST** treat write access to a GitOps repo as production cluster admin and restrict it accordingly with review, CODEOWNERS, and separation of duties.

**Why:** Anyone who can commit manifests can create privileged workloads or read cluster secrets without ever touching the cluster API.

**Detect:** Repo without CODEOWNERS on `manifests/` or `apps/`; ArgoCD/Flux repo write granted to broad teams; no admission policy blocking high-privilege kinds from Git.

**References:** OWASP GitOps Security, CWE-269, NIST SP 800-218 (SSDF), ArgoCD RBAC best practices, Flux multi-tenancy guide

# Hermetic Builds (no undeclared network/env deps during build)

**SHOULD NOT** let builds reach undeclared network or environment inputs; every dependency must be declared and cached.

**Why:** Non-hermetic builds silently pull mutated packages mid-build, leaving artifacts unreproducible and quietly tamperable.

**Detect:** grep CI for `--network=none`, unguarded `curl`/`pip install` outside lockfiles, ambient `export` in build scripts.

**References:** SLSA build isolation, NIST SP 800-218 (SSDF), Reproducible Builds project, CWE-494

# IaC Plan/Apply Triggered from Untrusted Pull Requests

**MUST NOT** run `terraform apply` (or equivalent) directly from fork or untrusted PR content; apply only from a reviewed, trusted branch after human approval.

**Why:** Malicious HCL in a PR can exfiltrate state, open security-group holes, or destroy resources the moment CI auto-applies it.

**Detect:** CI configs auto-applying on `pull_request` events; plan jobs echoing full state containing secrets; missing manual approval gate before apply stage.

**References:** OWASP IaC Security, CWE-913, NIST SP 800-218 (SSDF), Terraform Cloud PR workflow docs, Checkov tfsec guidance

# Linting & Static Analysis Enforced in CI (linter, type checker, SAST)

**MUST** fail the pipeline when linters, type checkers, or SAST scans report findings, not merely log them as warnings.

**Why:** Advisory-only scans are ignored at scale; vulnerable code merges unchecked because nothing blocks it, and defects caught in production cost orders of magnitude more than at commit time.

**Detect:** Workflow steps without `--exit-code`/`fail-on-error`; `continue-on-error: true` on scan jobs; SAST action with `level: warning`; missing ruff/mypy/semgrep/codeql steps entirely; pre-commit hooks running the same checks earliest in the lifecycle.

**References:** NIST SP 800-218 (SSDF), GitHub Code Scanning (CodeQL) docs, OWASP SAMM Security Testing, OWASP DevSecOps Maturity Model

# Patch management SLAs (MTTR targets by severity, exception tracking)

**MUST** define mean-time-to-remediate targets per severity (critical 24h, high 30d, medium 90d) and log every exception with owner and expiry date.

**Why:** Undated exceptions silently become permanent debt; SLA clocks make drift visible and auditable.

**Detect:** `sla` / `mttr` keys in policy docs, `waiver` / `exception` tracker files with `expires` fields

**References:** NIST SP 800-40 Rev.4, CIS Control 7, PCI DSS 6.3.3

# Policy-as-Code Enforcement (OPA/Sentinel/CEP gates in CI and admission)

**SHOULD** express security requirements as executable policies (OPA/Rego, Sentinel, Cloud Custodian) enforced in CI and admission, not wikis.

**Why:** Documented policies rot and get ignored; code-enforced gates make non-compliant infrastructure physically unable to deploy.

**Detect:** grep `policy.rego`, `opa check`, `sentinel`, `conftest`, Gatekeeper `ConstraintTemplate`, admission webhook policy configs.

**References:** NIST SP 800-53 CM-6, OPA/Gatekeeper docs, CIS Kubernetes Benchmark 5.2

# Review-Bot Neutral-Status Trap

**MUST** verify that AI review gates actually fail on unresolved findings — a required status that reports neutral/success while findings remain open does not block merges.

**Why:** Cursor documents this explicitly (findings default to neutral; you must enable fail-on-unresolved); GitHub Copilot defaults to "Comment" not "Approve" — teams often believe they have an AI gate they don't have.

**Detect:** branch protection requiring a bot check whose conclusion set lacks failure-on-findings; severity thresholds set above real risk; review config where unresolved ≠ failed.

**References:** Cursor Bugbot status semantics, GitHub Copilot review default-Comment behavior, Gemini severity-threshold filtering

# Review-Config Immutable to the Reviewee

**MUST** read review-automation config from the base branch (or otherwise protect it) so a PR cannot change how it is reviewed, and place CODEOWNERS on all review config.

**Why:** Cursor reads bugbot.yaml from the base branch specifically "so a PR cannot change how Bugbot reviews itself" — the general principle: review controls must not be attacker-controlled by the code under review.

**Detect:** review-config files (bot configs, thresholds, CODEOWNERS for review paths) read from PR head instead of base; missing CODEOWNERS on review automation config.

**References:** Cursor Bugbot base-branch config pattern, GitHub "requester cannot approve own agent's PR" rule

# SARIF-Standardized Scan Results (unified alert pipeline)

**SHOULD** emit all scanner findings in SARIF and ingest them into one dashboard, because scattered formats hide coverage gaps and duplicate triage.

**Why:** Findings in per-tool logs go unseen; a unified pipeline makes severity trends and deduplication auditable.

**Detect:** Scanners run without `--format sarif` / `output: sarif`; no upload step to code-scanning API; each tool reporting to a separate ad-hoc log file.

**References:** NIST SP 800-218 (SSDF), SARIF spec (OASIS), GitHub code scanning SARIF upload docs

# Secrets in CI Logs

**MUST NOT** echo, print, or interpolate secrets into CI output; mask values via CI secret masking and avoid commands that dump environment variables.

**Why:** Build logs are widely readable — teammates, forked PRs, and third-party integrations can harvest tokens from a single verbose step.

**Detect:** `echo $SECRET`, `set -x` in steps handling credentials, `env`/`printenv` in pipelines, `export` of tokens without `::add-mask::`.

**References:** OWASP ASVS V7.1.1, CWE-532, CWE-214

# Unattended-Agent Automation Governance

**MUST** govern scheduled/event-triggered agents (cron, webhook) with: attribution to the automation creator, minimal tool surface per automation, trigger trust controls (signed webhooks, ignore non-trusted events), and preserved downstream human approval.

**Why:** Unattended agents run with no human per task, so every capability they hold is reachable from whatever triggers them; an automation must not inherit outbound authority from an inbound webhook or schedule it does not control.

**Detect:** automations with broad tool grants or opt-in to untrusted-user events; webhook endpoints accepting unsigned payloads; no owner attribution per automation; agent can merge/approve its own output.

**References:** GitHub Copilot coding agent risks and mitigations, OWASP LLM06:2025 Excessive Agency, NIST SP 800-53 AC-6

