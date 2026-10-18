# cicd-pipeline-security — full checklist (23 items)

CI/CD system as an attack surface.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Branch Protection

**MUST** require reviewed, status-passing pull requests before merging into protected branches, with force-push and branch deletion disabled.

**Why:** Unprotected main branches let anyone push unreviewed or malicious code straight into production builds.

**Detect:** GitHub settings API `branches/*/protection`; grep repo scripts for `push --force` to main; missing `.github/settings.yml` `protected_branches`.

**References:** OWASP CI Security CS1, CWE-284, NIST SP 800-218 PW.7, GitHub branch protection docs

# Secrets in CI Logs

**MUST NOT** echo, print, or interpolate secrets into CI output; mask values via CI secret masking and avoid commands that dump environment variables.

**Why:** Build logs are widely readable — teammates, forked PRs, and third-party integrations can harvest tokens from a single verbose step.

**Detect:** `echo $SECRET`, `set -x` in steps handling credentials, `env`/`printenv` in pipelines, `export` of tokens without `::add-mask::`.

**References:** OWASP ASVS V2.10.3, CWE-532, CWE-214

# CI Runner Isolation

**MUST** run untrusted build jobs on ephemeral, per-job isolated runners with no shared workspace, persistent credentials, or network access to production networks.

**Why:** Reused or shared runners let one malicious job harvest secrets and artifacts left behind by previous builds.

**Detect:** Self-hosted runner labels in workflow `runs-on`; persistent `/var/run/docker.sock` mounts; runner config `ephemeral=false`; shared cache dirs across jobs.

**References:** OWASP CI Security CS3, CWE-419, NIST SP 800-218 PW.5, GitHub Actions security hardening guide

# CI Action Pinning (SHA not tag)

**MUST** reference third-party actions by full commit SHA rather than a mutable tag or branch name.

**Why:** A retagged or hijacked tag silently swaps in attacker-controlled code that runs with your workflow's permissions.

**Detect:** Grep `.github/workflows/*.yml` for `uses:` lines matching `@v[0-9]` or `@main` instead of 40-hex SHAs; actionlint `pin-versions` rule.

**References:** OWASP CI Security CS2, CWE-829, NIST SP 800-218 PO.3, GitHub Actions security hardening guide

# CI Deploy-Credential Scoping

**MUST NOT** grant deploy credentials to every workflow; scope each secret and token to the single job and target environment that needs it.

**Why:** Broadly shared deploy keys mean any compromised workflow can push to every environment, including production.

**Detect:** Repo-level `secrets.*` used in many workflows instead of environment-scoped ones; cloud IAM policies with `*` resources attached to CI roles; missing `environment:` stanzas.

**References:** OWASP CI Security CS4, CWE-250, NIST SP 800-218 PS.2, GitHub environments and OIDC deploy docs

# CI Artifact Integrity Handoff

**MUST** sign built artifacts and verify signatures and checksums before downstream deployment consumes them.

**Why:** Unsigned artifacts can be swapped or tampered with between build and deploy with no way to detect the substitution.

**Detect:** Missing `cosign sign`/`sigstore`/`gpg --sign` steps; deploy jobs pulling images by mutable tag without digest pinning; no `.sha256` or provenance attestations in artifact stores.

**References:** OWASP CI Security CS5, CWE-345, NIST SP 800-218 PW.6, SLSA provenance levels, sigstore/cosign docs

# Benchmark Scanning in CI (kube-bench, Lynis, Trivy misconfig)

**SHOULD** run kube-bench, Lynis, or Trivy misconfig scans in CI on every image and host config change, failing the pipeline on high-severity findings.

**Why:** Hardening drifts silently after deploy; without automated benchmark gates, regressions ship unnoticed until an attacker exploits them.

**Detect:** Check `.github/workflows/*` or Jenkinsfile for `kube-bench`, `lynis audit`, `trivy config`, `trivy image --security-check misconfig` steps and severity gates.

**References:** CIS Benchmarks, NIST SP 800-53 CM-6, DevSecOps, CWE-1188

# Code Review Practice

**MUST** require at least one independent reviewer for every change touching authentication, cryptography, or input handling, with a documented security checklist and a response SLA.

**Why:** Single-author security code ships logic errors and backdoors that a second pair of eyes reliably catches.

**Detect:** CODEOWNERS covering auth/crypto paths, PR templates with security checklist items, branch protection requiring ≥1 approval; self-merged security PRs in git log.

**References:** OWASP ASVS V1.1.4, NIST SP 800-218 PS.1 (code review), OWASP Code Review Guide v2, CWE-1068 (design/practice inconsistency)

# Linting & Static Analysis Enforced in CI (linter, type checker, SAST)

**MUST** fail the pipeline when linters, type checkers, or SAST scans report findings, not merely log them as warnings.

**Why:** Advisory-only scans are ignored at scale; vulnerable code merges unchecked because nothing blocks it.

**Detect:** Workflow steps without `--exit-code`/`fail-on-error`; `continue-on-error: true` on scan jobs; SAST action with `level: warning`; missing ruff/mypy/semgrep/codeql steps entirely.

**References:** OWASP CI Security CS2, CWE-1156, NIST SP 800-218 PW.7, GitHub Code Scanning (CodeQL) docs

# CI Workflow Injection via Untrusted PR Content (pull_request_target)

**MUST NOT** check out or execute pull request code inside a `pull_request_target` or other privileged-trigger job that holds write tokens or secrets.

**Why:** Attacker-controlled PR text interpolated into shell steps runs arbitrary commands with full repo and secret access.

**Detect:** Grep workflows for `pull_request_target` combined with `secrets.`, `${{ github.event.* }}` in `run:` blocks, or `checkout` of `github.event.pull_request.head.sha`.

**References:** OWASP CI Security CS2, CWE-94, NIST SP 800-218 PW.8, GitHub Actions security hardening guide

# Dockerfile Secret Leakage via COPY, Build Args, and Cache Layers

**MUST NOT** bake secrets into images via `COPY` of credential files or plain `ARG`/`ENV` values; use BuildKit `--mount=type=secret` instead.

**Why:** Copied files and build args persist in layer history and are recoverable from any pushed image with `docker history`.

**Detect:** Grep Dockerfiles for `COPY .npmrc`, `COPY *credentials*`, `ARG API_KEY`, `ENV SECRET`, or `RUN ... $ARG` patterns; inspect `docker history` for leaked values.

**References:** OWASP Docker DS02, CWE-540, NIST SP 800-218 PS.1, BuildKit secret mounting docs, hadolint DL3025/DL3009

# Docker-in-Docker / Privileged Build Steps in CI

**SHOULD** replace privileged Docker-in-Docker with rootless or daemonless builders (BuildKit, Kaniko, Buildah) since `privileged: true` grants the container host-level control.

**Why:** A privileged build container can escape to the runner host and capture every credential and workload on it.

**Detect:** Grep workflows for `privileged: true`, `docker:dind` images, or volume mounts of `/var/run/docker.sock` into build jobs.

**References:** OWASP Docker DS01, CWE-250, NIST SP 800-218 PW.5, Kaniko and BuildKit rootless docs, GitLab CI best practices

# GitOps Repo Write Access Equals Cluster Write Access

**MUST** treat write access to a GitOps repo as production cluster admin and restrict it accordingly with review, CODEOWNERS, and separation of duties.

**Why:** Anyone who can commit manifests can create privileged workloads or read cluster secrets without ever touching the cluster API.

**Detect:** Repo without CODEOWNERS on `manifests/` or `apps/`; ArgoCD/Flux repo write granted to broad teams; no admission policy blocking high-privilege kinds from Git.

**References:** OWASP GitOps Security, CWE-269, NIST SP 800-218 PO.3, ArgoCD RBAC best practices, Flux multi-tenancy guide

# IaC Plan/Apply Triggered from Untrusted Pull Requests

**MUST NOT** run `terraform apply` (or equivalent) directly from fork or untrusted PR content; apply only from a reviewed, trusted branch after human approval.

**Why:** Malicious HCL in a PR can exfiltrate state, open security-group holes, or destroy resources the moment CI auto-applies it.

**Detect:** CI configs auto-applying on `pull_request` events; plan jobs echoing full state containing secrets; missing manual approval gate before apply stage.

**References:** OWASP IaC Security, CWE-913, NIST SP 800-218 PW.8, Terraform Cloud PR workflow docs, Checkov tfsec guidance

# AI-generated code review gate before merge

**SHOULD** require human security review of AI-generated code before merge; Copilot-style output is not self-certifying.

**Why:** Models reproduce vulnerable patterns and plausible-but-broken crypto from training data at high volume and speed.

**Detect:** PRs with AI-assist labels merged without security-review approval; CI lacks a gate matching ai-generated/copilot review policy.

**References:** OWASP LLM03:2025, NIST SSDF PW.4, CWE-1157

# Patch management SLAs (MTTR targets by severity, exception tracking)

**MUST** define mean-time-to-remediate targets per severity (critical 7d, high 30d, medium 90d) and log every exception with owner and expiry date.

**Why:** Undated exceptions silently become permanent debt; SLA clocks make drift visible and auditable.

**Detect:** `sla` / `mttr` keys in policy docs, `waiver` / `exception` tracker files with `expires` fields

**References:** NIST SP 800-40 Rev.4, CIS Control 7, PCI DSS 6.3.3

# Push Protection (block secrets at commit/push time)

**MUST** scan every commit and push for credentials and reject those containing live secrets before they enter history.

**Why:** A secret once committed stays in git history forever; rotation is the only true fix and is often missed.

**Detect:** Missing pre-commit/gitleaks/trufflehog hooks; no GitHub push protection or secret-scanning alerts enabled; `.git/hooks/pre-commit` absent from repo tooling.

**References:** CWE-798, NIST SP 800-218 PS.1, GitHub push protection docs, gitleaks / trufflehog / detect-secrets

# SARIF-Standardized Scan Results (unified alert pipeline)

**SHOULD** emit all scanner findings in SARIF and ingest them into one dashboard, because scattered formats hide coverage gaps and duplicate triage.

**Why:** Findings in per-tool logs go unseen; a unified pipeline makes severity trends and deduplication auditable.

**Detect:** Scanners run without `--format sarif` / `output: sarif`; no upload step to code-scanning API; each tool reporting to a separate ad-hoc log file.

**References:** OWASP CI Security CS2, CWE-1053, NIST SP 800-218 PW.7, SARIF spec (OASIS), GitHub code scanning SARIF upload docs

# Shift-Left Security (security earliest in the lifecycle)

**MUST** run SAST, dependency, and secret scanning in CI on every pull request, failing the build on high-severity findings rather than deferring them to pre-release.

**Why:** Defects caught in production cost orders of magnitude more than at commit time; late gates train teams to bypass them.

**Detect:** `.github/workflows` with `sast`/`semgrep`/`gitleaks` steps, `fail-on: high` in scanner config, pre-commit hooks

**References:** OWASP SAMM Security Testing, MS SDL, OWASP DevSecOps Maturity Model

# Hermetic Builds (no undeclared network/env deps during build)

**SHOULD NOT** let builds reach undeclared network or environment inputs; every dependency must be declared and cached.

**Why:** Non-hermetic builds silently pull mutated packages mid-build, leaving artifacts unreproducible and quietly tamperable.

**Detect:** grep CI for `--network=none`, unguarded `curl`/`pip install` outside lockfiles, ambient `export` in build scripts.

**References:** SLSA build isolation, NIST SP 800-218 PW.4, Reproducible Builds project, CWE-494

# Branch Protection & Required Reviews (no direct pushes, enforced approval)

**MUST** block direct pushes to protected branches and require reviewed, up-to-date approvals before merge.

**Why:** Unprotected main branches let one bad or malicious commit ship straight to production, bypassing every downstream control.

**Detect:** grep `enforce_admins`, `required_pull_request_reviews`, `required_status_checks` in repo settings-as-code; CODEOWNERS files.

**References:** OWASP SAMM Code Reviews, NIST SP 800-218 PW.7, CWE-1104, GitHub branch protection docs

# Pinned CI Actions & Third-Party Pinned Dependencies (SHA-pinned, not floating tags)

**MUST** reference third-party CI actions by immutable commit SHA, never mutable tags like `@v1`.

**Why:** A floating tag can be retagged overnight to attacker code running with your CI's tokens — the tj-actions incident proved it.

**Detect:** grep workflow YAML for `uses: owner/repo@v` vs `@<40-hex-sha>`; renovate `pin` configs, dependabot pin settings.

**References:** OWASP CI/CD Top 10 CICD-SEC-4, GitHub Actions hardening, SLSA provenance, CWE-829

# Policy-as-Code Enforcement (OPA/Sentinel/CEP gates in CI and admission)

**SHOULD** express security requirements as executable policies (OPA/Rego, Sentinel, Cloud Custodian) enforced in CI and at admission, not in wikis.

**Why:** Documented policies rot and get ignored; code-enforced gates make non-compliant infrastructure physically unable to deploy.

**Detect:** grep for `policy.rego`, `opa check`, `sentinel`, `conftest`, Gatekeeper `ConstraintTemplate`, admission webhook policy configs.

**References:** NIST SP 800-53 CM-6, OPA/Gatekeeper docs, CIS Kubernetes Benchmark 5.2, Policy-as-Code patterns

