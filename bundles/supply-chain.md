# supply-chain — full checklist (26 items)

Dependencies, artifacts, build provenance.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Secret Scanning

**MUST** run automated secret scanning (gitleaks, trufflehog, GitHub push protection) on every commit and full-history scans before publishing any repository.

**Why:** Developers routinely commit live credentials under deadline pressure; without scanning, leaks ship silently to public or shared remotes — and a secret once committed stays in git history forever, so rotation is the only true fix and is often missed.

**Detect:** `.gitleaks.toml`, `.pre-commit-config.yaml` with gitleaks/trufflehog hooks that reject at commit/push time, absent GitHub `secret_scanning`/push-protection settings in org config.

**References:** OWASP ASVS V2.10.2, CWE-540, CWE-319, NIST SP 800-218 PS.1, GitHub push protection docs

# Dependency Vulnerabilities

**MUST** scan third-party libraries against a current advisory database (OSV/GHSA) in CI and fail builds on critical or high findings.

**Why:** Unpatched library CVEs are the most common entry point for remote code execution and data breaches.

**Detect:** `requirements.txt`, `package-lock.json`, `go.mod`; run `pip-audit`, `npm audit`, `govulncheck`; grep `.github/workflows` for `osv-scanner`.

**References:** OWASP A06:2021, CWE-1104, SCB-001

# Image Scanning

**SHOULD** scan every container image for vulnerabilities and malware at build time and again before deployment, blocking on policy violations.

**Why:** Untested images ship known-exploitable OS packages into production, where runtime patching is rarely possible.

**Detect:** CI steps invoking `trivy image`, `grype`, or `docker scout`; absence of any scan stage in pipeline YAML; registry scan config disabled.

**References:** OWASP A06:2021, CIS Docker 4.9, NIST SP 800-190

# Lockfiles

**MUST** commit and honor dependency lockfiles so every install resolves to identical, audited versions.

**Why:** Unpinned resolution lets a transitive dependency change silently between builds, opening the door to typosquat and version-rollback attacks.

**Detect:** Missing `package-lock.json`, `poetry.lock`, `go.sum`; CI flags like `--no-lock`, `npm install` without `ci`; `.gitignore` excluding lockfiles.

**References:** OWASP A06:2021, CWE-829, SCB-002

# Reproducible Builds

**SHOULD** produce bit-for-bit reproducible artifacts by eliminating timestamps, random paths, and nondeterministic ordering from builds.

**Why:** Non-reproducible output makes it impossible to verify that a deployed binary matches its reviewed source, hiding tampered releases.

**Detect:** `SOURCE_DATE_EPOCH` unset; build scripts embedding `date`/`hostname`; `-trimpath` absent in Go builds; unreproducible flag in `reproducible-builds.org` checks.

**References:** CWE-937, reproducible-builds.org, SLSA L3

# Hallucinated Packages

**SHOULD** verify that every package name in generated or AI-assisted code actually exists and matches intent before installing.

**Why:** Attackers pre-register plausible-sounding package names that AI models invent, so blindly installing them pulls malware into the project.

**Detect:** Install logs for names absent from the registry; review AI-generated import lines against PyPI/npm search; grep manifests for near-miss spellings of popular libs.

**References:** CWE-427, Snyk "slopsquatting" research, OWASP LLM03

# Dependency Confusion / Package-Name Squatting

**MUST NOT** resolve internal package names from public registries; private packages must install only from the internal registry via explicit scope or index pinning.

**Why:** Attackers publish an internal-named package with a higher version to npm/PyPI, and the resolver silently prefers it, executing attacker code at install time.

**Detect:** `.npmrc`/`pip.conf` without scoped `@internal:registry=`; `pip install` without `--index-url`; internal names absent from private registry listings.

**References:** CWE-427, OWASP A06:2021, Alex Birsan 2021 disclosure

# Artifact Signing & Provenance (cosign/Sigstore/SBOM)

**MUST** sign released images and attach provenance attestations plus an SBOM generated inside the trusted build pipeline.

**Why:** Unsigned artifacts can be swapped or forged after build with no way to trace who produced what, defeating every downstream integrity check.

**Detect:** `cosign sign --yes` / `cosign attest` in CI; `syft`/`bom` generation steps; registry entries lacking `.sig` bundles or SPDX/CycloneDX files.

**References:** SLSA L3, Sigstore docs, NIST SP 800-161, NTIA SBOM minimum elements

# Model Artifact Integrity (pickle-format models)

**MUST NOT** load pickle-format model artifacts (.pkl, .pt via torch.load default) from untrusted sources; prefer safetensors or verified signed formats.

**Why:** Pickle executes arbitrary code at load time, so a malicious checkpoint is remote code execution before inference starts.

**Detect:** grep torch.load( without weights_only=True, pickle.load on model files, .pkl/.ckpt pulled from Hub without checksum/signature.

**References:** OWASP LLM08:2025, CWE-502, CWE-94

# CI Action Pinning (SHA not tag)

**MUST** reference third-party actions by full commit SHA rather than a mutable tag or branch name.

**Why:** A retagged or hijacked tag silently swaps in attacker-controlled code that runs with your workflow's permissions, as the tj-actions incident proved; upstream tag compromises (SolarWinds, event-stream) extend the same lesson to every unpinned build input.

**Detect:** Grep `.github/workflows/*.yml` for `uses:` lines matching `@v[0-9]` or `@main` instead of 40-hex SHAs; check for unpinned `curl | bash` installers in Dockerfiles or CI scripts; verify renovate/dependabot pin settings; actionlint `pin-versions` rule.

**References:** OWASP CI Security CS2, CWE-829, NIST SP 800-218 PO.3, GitHub Actions security hardening guide, OWASP CI/CD Top 10 CICD-SEC-4, NIST SP 800-161

# CI Artifact Integrity Handoff

**MUST** sign built artifacts and verify signatures and checksums before downstream deployment consumes them.

**Why:** Unsigned artifacts can be swapped or tampered with between build and deploy with no way to detect the substitution.

**Detect:** Missing `cosign sign`/`sigstore`/`gpg --sign` steps; deploy jobs pulling images by mutable tag without digest pinning; no `.sha256` or provenance attestations in artifact stores.

**References:** OWASP CI Security CS5, CWE-345, NIST SP 800-218 PW.6, SLSA provenance levels, sigstore/cosign docs

# Mutable Image Tags (latest) Instead of Digest Pinning

**SHOULD** reference images by immutable digest (`@sha256:`) rather than floating tags like `latest` in production manifests.

**Why:** A retagged or compromised `latest` silently changes what deploys, defeating rollback and supply-chain review.

**Detect:** Image fields ending in `:latest` or bare repo names; absence of `@sha256:` digest in Deployment/Pod specs.

**References:** CIS Docker 4.5, NIST SP 800-190 4.4, OWASP A08 Software Supply Chain, CWE-829

# Admission Enforcement of Signed Images (Verify, Not Just Sign)

**MUST** enforce signature verification at admission so unsigned or wrongly-signed images are rejected before they ever schedule.

**Why:** Signing without enforcement is decoration: an attacker pushes an unsigned image and the cluster runs it happily because nothing checks.

**Detect:** ClusterPolicy `cosigned` / `verify-images` with `match` on all registries; absence of kyverno/admission-controller verify rules; `--image-verification` disabled in k3s config.

**References:** SLSA L4, Sigstore, NSA Kubernetes Hardening Guide, CIS K8s 5.4

# IaC Plan/Apply Triggered from Untrusted Pull Requests

**MUST NOT** run `terraform apply` (or equivalent) directly from fork or untrusted PR content; apply only from a reviewed, trusted branch after human approval.

**Why:** Malicious HCL in a PR can exfiltrate state, open security-group holes, or destroy resources the moment CI auto-applies it.

**Detect:** CI configs auto-applying on `pull_request` events; plan jobs echoing full state containing secrets; missing manual approval gate before apply stage.

**References:** OWASP IaC Security, CWE-913, NIST SP 800-218 PW.8, Terraform Cloud PR workflow docs, Checkov tfsec guidance

# Registry Outage Tolerated via Cached/Pinned Images

**SHOULD** keep images cached on nodes and pinned by digest so a registry outage does not block scheduling or restarts.

**Why:** If a pod must pull during a registry outage, rescheduling and rollouts stall, turning a third-party outage into a cluster outage.

**Detect:** No `imagePullPolicy: IfNotPresent`/`Never` with pre-pulled images; no local registry mirror or pull-through cache configured.

**References:** K8s docs imagePullPolicy, NIST SP 800-190 4.4, Harbor/Docker registry mirror docs, OWASP A08

# EU Cyber Resilience Act (product security lifecycle, SBOM and vulnerability handling duties)

**MUST** ship products with digital elements under a secure development lifecycle, provide an SBOM, and actively handle reported vulnerabilities for the support period.

**Why:** Unpatched connected products become botnet fodder; CRA makes manufacturers legally liable for known vulnerabilities left unfixed.

**Detect:** grep for "SBOM", "CRA", "support period", vulnerability disclosure policy; no CycloneDX/SPDX artifacts, end-of-life products with live CVEs.

**References:** EU CRA 2024/2847, ENISA SBOM guidance, ISO/IEC 30111

# Third-party MCP/plugin trust and malicious tool-description injection

**MUST** vet, pin, and sandbox third-party MCP servers and plugins; treat their tool descriptions and names as untrusted input to the model.

**Why:** A malicious tool description can instruct the agent to exfiltrate data or chain other tools harmfully.

**Detect:** MCP config pulling unpinned packages; no approved-server allowlist; tool descriptions unsanitized at registration.

**References:** OWASP LLM06:2025, MITRE ATLAS T0059, CWE-829

# Vendor/third-party risk management and subprocessor registers

**SHOULD** maintain a current register of every vendor and its subprocessors with review dates, data access scope, and breach-notification terms.

**Why:** Breaches frequently originate downstream; without a register you cannot assess exposure or notify affected parties when a vendor falls.

**Detect:** Missing vendor register doc or spreadsheet; SaaS admin lists without subprocessor pages checked; contracts lacking breach-notification SLA clauses.

**References:** NIST SP 800-161, SOC 2 CC9.2, GDPR Art. 28, ISO 27036

# Malware Alerts on Dependencies (registry-side malware detection)

**MAY** subscribe to registry-side malware signals (npm malware advisories, PyPI malware scanning, Dependabot security alerts) and route them to a responder.

**Why:** Advisory CVE feeds lag behind live malware campaigns; registry detectors catch obfuscated install-script payloads that version scans miss entirely.

**Detect:** Dependabot/Renovate security alerts enabled in repo settings; `npm audit --audit-level=moderate`; subscribed to GitHub security advisories for owned packages.

**References:** OWASP A06:2021, npm malware policy, GitHub Advisory Database, CWE-506

# Cyber Supply Chain Risk Management (supplier vetting and ongoing risk review, NIST SP 800-161)

**MUST** vet critical suppliers at onboarding and re-review their security posture on a fixed cadence.

**Why:** One compromised or negligent vendor becomes your breach; SolarWinds showed a single upstream can poison thousands of downstream users.

**Detect:** grep `vendor_risk`, `supplier_assessment`, `C-SCRM` in third-party inventories, due-diligence records, SBOM ingestion configs.

**References:** NIST SP 800-161, NIST SSDF (SP 800-218), ISO/IEC 27036

# SBOM Generation & Retention (CycloneDX/SPDX per build, kept for incident response)

**MUST** generate a CycloneDX or SPDX SBOM per build and retain it long enough to answer "were we affected?" in incidents.

**Why:** Without per-build inventories, Log4Shell-style emergencies become weeks of guesswork instead of minutes of lookup.

**Detect:** grep `bom-*.json`, `cyclonedx`, `spdx`, `syft`, `cdxgen` in CI pipelines and artifact repos.

**References:** NTIA SBOM minimum elements, NIST SP 800-161, OWASP CycloneDX, CWE-1357

# Build Provenance Attestation (SLSA-style signed provenance for artifacts)

**MUST** attach signed provenance (source, builder, inputs) to every published artifact so consumers can verify its origin.

**Why:** Unsigned artifacts let attackers substitute trojaned builds that look identical to legitimate releases downstream.

**Detect:** grep `slsa`, `provenance`, `cosign attest`, `sigstore`, `in-toto` in CI configs and release steps.

**References:** SLSA v1.0, in-toto attestation framework, NIST SP 800-218 PW.4, CWE-494

# Hermetic Builds (no undeclared network/env deps during build)

**SHOULD NOT** let builds reach undeclared network or environment inputs; every dependency must be declared and cached.

**Why:** Non-hermetic builds silently pull mutated packages mid-build, leaving artifacts unreproducible and quietly tamperable.

**Detect:** grep CI for `--network=none`, unguarded `curl`/`pip install` outside lockfiles, ambient `export` in build scripts.

**References:** SLSA build isolation, NIST SP 800-218 PW.4, Reproducible Builds project, CWE-494

# Artifact Signing & Verification at Deploy (cosign/sigstore verify before run)

**MUST** verify cosign/sigstore signatures on images and release artifacts at deploy time, rejecting unsigned or mismatched ones.

**Why:** An unsigned image pulled into production may be a tampered one; the deploy boundary is the last honest checkpoint.

**Detect:** grep `cosign verify`, `sigstore`, Kyverno `verifyImages`, `signature_verification: true` in deploy pipelines.

**References:** SLSA levels 3-4, sigstore/cosign docs, NIST SP 800-218 PW.6, CWE-347

# Broken Link & Dependency Hijacking

**SHOULD** remove or pin dead external references (deleted CDN packages, lapsed domains, 404'd script/CSS links) that attackers can register and serve malicious content through.

**Why:** A dangling `<script src>` to an unregistered domain is a supply-chain foothold the browser trusts implicitly — recon tools flag these by checking DNS on referenced hosts.

**Detect:** crawl pages and check HTTP status + DNS registration of every external script/CSS/frame host; grep templates for known-dead CDNs (bower, rawgit, shutdown libraries).

**References:** OWASP WSTG-BUSLOGIC broken-link hijacking, CWE-427, npm/CDN takeover incidents

# Firmware Signing & Secure Boot

**MUST** sign firmware images and enforce signature verification at boot (secure boot chain) so unsigned or tampered images cannot run on devices.

**Why:** Unsigned firmware is the ultimate persistence layer — an attacker who flashes once owns the device permanently and it survives every software remediation.

**Detect:** grep build pipeline for signing steps (`osslsigncode`, `imgtool`, HSM calls); check bootloader verify-enforce (not just verify-log) mode; look for dev/test keys shipped in production images.

**References:** NIST SP 800-193 platform firmware resiliency, OWASP IoT Top 10 (IOT ASSET), Arm TrustZone/UEFI Secure Boot docs

