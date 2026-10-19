# supply-chain — full checklist (60 items)

Dependencies, artifacts, build provenance.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/supply-chain.md](../categories/supply-chain.md) · Index: [SKILL.md](../SKILL.md)

# AI Third-Party Components

**MUST** inventory third-party datasets, pre-trained models, plugins, and hosted model APIs, recording their downstream impact and a contingency plan for failure.

**Why:** Errors and compromises in procured models or data propagate silently into every downstream output, and an uninventoried component cannot be rotated or recalled.

**Detect:** grep for unpinned model and dataset loads (`from_pretrained(`, `hf_hub_download`, dataset URLs, plugin registries) and check each appears in the component inventory with a digest.

**References:** NIST AI 600-1 GOVERN 6.1, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# Artifact Integrity Verification

**MUST** verify the checksum or signature of every downloaded artifact before executing it or shipping it onward.

**Why:** Transport security protects the channel, not the bytes: a compromised mirror or tampered upload serves whatever it chooses. Running or redistributing those bytes imports the attacker's code with your privileges.

**Detect:** grep download steps (`curl`, `wget`, `ADD <url>`, package-manager fetch hooks) for an adjacent `sha256sum -c`, `gpg --verify`, or `cosign verify`; flag any `curl ... | sh` and unverified `ADD` URL.

**References:** SLSA v1.0 requirements, https://slsa.dev/spec/v1.0/requirements, Codecov security update, https://about.codecov.io/blog/security-update/, CWE-494 Download of Code Without Integrity Check

# Authorized Supply Channels

**SHOULD** buy security-relevant hardware and software only from the manufacturer or an authorized distributor, never through gray-market resellers.

**Why:** Gray-market channels deliver counterfeit or reflashed components that pass functional tests and fail every integrity expectation later.

**Detect:** the bill of materials vendor list against the manufacturer's published authorized-distributor list

**References:** NIST SP 800-161r1 (C-SCRM, foundational practices)

# Binary Composition Verification

**MUST** inventory third-party components from the shipped binary itself and reconcile that list against the build's declared dependencies.

**Why:** Declared manifests omit statically linked and vendored libraries, so a binary can carry an unpatched component that no SBOM records.

**Detect:** Run `syft <image-or-binary>` and diff its package list against the SBOM generated at build time.

**References:** AutoFirm (arXiv 2406.12947), https://arxiv.org/abs/2406.12947, OWASP CycloneDX specification

# Broken Link & Dependency Hijacking

**SHOULD** remove or pin dead external references (deleted CDN packages, lapsed domains, 404'd script/CSS links) that attackers can register and serve malicious content through.

**Why:** A dangling `<script src>` to an unregistered domain is a supply-chain foothold the browser trusts implicitly — recon tools flag these by checking DNS on referenced hosts.

**Detect:** crawl pages and check HTTP status + DNS registration of every external script/CSS/frame host; grep templates for known-dead CDNs (bower, rawgit, shutdown libraries).

**References:** OWASP WSTG-BUSL, CWE-427, npm/CDN takeover incidents

# Build Provenance Attestation (SLSA-style signed provenance for artifacts)

**MUST** sign released artifacts and attach signed provenance (source, builder, inputs) plus an SBOM generated inside the trusted build pipeline, and **MUST** verify those signatures and checksums at every downstream boundary (before a deployment consumes an artifact, and at cluster admission) so unsigned or mismatched artifacts are rejected rather than merely signed.

**Why:** Unsigned artifacts let attackers substitute trojaned builds that look identical to legitimate releases downstream, and without provenance or an SBOM there is no record of which source and builder produced what.

**Detect:** `cosign sign --yes` / `cosign attest` in CI; `syft`/`bom` generation steps; grep `slsa`, `provenance`, `in-toto` in CI configs and release steps; registry entries lacking `.sig` bundles or SPDX/CycloneDX files; deploy jobs pulling images by mutable tag with no digest or checksum verification; grep `cosign verify`, `sigstore`, Kyverno `verifyImages`, `signature_verification: true`, and admission verify rules.

**References:** SLSA v1.0, Sigstore/cosign docs, in-toto attestation framework, NIST SP 800-218 (SSDF), NIST SP 800-161, NTIA SBOM minimum elements, OWASP CI/CD Top 10 CICD-SEC-9, NSA Kubernetes Hardening Guide, CIS K8s 5.5 (Extensible Admission Control), CWE-494, CWE-345

# C2-Free Propagation Assumption

**SHOULD** design containment and detection assuming compromised code propagates without command-and-control, through local credentials and package registries.

**Why:** A worm that reads its own package and republishes it needs no egress channel, so network blocks and C2 signatures miss it entirely.

**Detect:** the containment runbook: if egress filtering is the only propagation control, the assumption is wrong

**References:** Shai-Hulud 2.0 npm worm analysis (2025)

# CI Action Pinning (SHA not tag)

**MUST** reference third-party actions by full commit SHA rather than a mutable tag or branch name.

**Why:** A retagged or hijacked tag silently swaps in attacker-controlled code that runs with your workflow's permissions, as the tj-actions incident proved; the same trust-in-mutable-references lesson applies to every unpinned build input — compromised build systems and hijacked packages (SolarWinds, event-stream) show what runs with your pipeline's privileges when an upstream reference is subverted.

**Detect:** Grep `.github/workflows/*.yml` for `uses:` lines matching `@v[0-9]` or `@main` instead of 40-hex SHAs; check for unpinned `curl | bash` installers in Dockerfiles or CI scripts; verify renovate/dependabot pin settings; actionlint `pin-versions` rule.

**References:** CWE-829, NIST SP 800-218 (SSDF), GitHub Actions security hardening guide, OWASP Top 10 CI/CD Security Risks CICD-SEC-3 (Dependency Chain Abuse), NIST SP 800-161

# Dependency Confusion / Package-Name Squatting

**MUST NOT** resolve internal package names from public registries; private packages must install only from the internal registry via explicit scope or index pinning.

**Why:** Attackers publish an internal-named package with a higher version to npm/PyPI, and the resolver silently prefers it, executing attacker code at install time.

**Detect:** `.npmrc`/`pip.conf` without scoped `@internal:registry=`; `pip install` without `--index-url`; internal names absent from private registry listings.

**References:** CWE-427, OWASP A08:2021, Alex Birsan 2021 disclosure

# Dependency Delta Gating

**SHOULD** evaluate dependency risk on the packages a change adds or upgrades, and report pre-existing findings separately.

**Why:** Blocking every pull request on the whole historical backlog trains teams to bypass the gate, while delta scoping keeps the check meaningful and actionable.

**Detect:** osv-scanner --lockfile=- <(git diff origin/main -- package-lock.json)  or an equivalent scan of base versus head lockfiles in the PR job

**References:** Dependency Review action, https://github.com/actions/dependency-review-action

# Dependency Install Scripts

**MUST** disable dependency install-time script execution in builds, enabling it only for explicitly reviewed packages that need it.

**Why:** Install hooks execute arbitrary code with the build's credentials before any scanner sees the package. A postinstall script is a complete compromise path that requires no vulnerability.

**Detect:** grep for `ignore-scripts=true` in `.npmrc`, `--ignore-scripts` on install commands, `postinstall`/`preinstall` keys in `package.json`, and `setup.py` execution or `--no-build-isolation` in Python builds.

**References:** OWASP NPM Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html

# Dependency Maintainer Health

**SHOULD** treat maintainer dormancy, ownership transfer, or single-maintainer status in a critical dependency as a security event requiring review.

**Why:** Registry compromises usually arrive through a trusted maintainer account rather than a vulnerability. Abandoned or handed-over projects lose the one person who would have noticed the malicious release.

**Detect:** command: `npm view <pkg> maintainers time.modified`, `pip index versions`, or the registry API for maintainer list and last publish date, compared against the review date in the dependency register.

**References:** xz backdoor announcement (upstream maintainer page), https://tukaani.org/xz-backdoor/, event-stream maintainer handover, https://github.com/dominictarr/event-stream/issues/116

# Cooldown Before Adopting Releases

**SHOULD** delay automated adoption of newly published dependency releases by a configured cooldown, so poisoned releases are caught upstream first.

**Why:** The hours after publication are when malicious or broken releases get reported by others; immediate automation ingests them first.

**Detect:** grep renovate minimumReleaseAge or dependabot cooldown settings in the update configuration

**References:** zizmor, https://github.com/zizmorcore/zizmor

# Dependency Version Cooldown

**SHOULD** delay adopting newly published dependency versions until a short cooldown period passes without incident.

**Why:** Malicious or broken releases are usually reported and yanked within days, while automated update bots consume them within hours. A cooldown converts someone else's incident into a version you never installed.

**Detect:** command: `npm config get minimum-release-age`, Renovate `minimumReleaseAge`, Dependabot `cooldown`, or the update bot's configured soak window in the automation config.

**References:** GitHub: the case for a cooldown before version updates, https://github.blog/security/supply-chain-security/the-case-for-a-cooldown-why-dependabot-now-waits-before-issuing-version-updates/

# Dependency Vulnerabilities

**MUST** scan third-party libraries against a current advisory database (OSV/GHSA) in CI and fail builds on critical or high findings.

**Why:** Unpatched library CVEs are the most common entry point for remote code execution and data breaches.

**Detect:** `requirements.txt`, `package-lock.json`, `go.mod`; run `pip-audit`, `npm audit`, `govulncheck`; grep `.github/workflows` for `osv-scanner`.

**References:** OWASP A06:2021, CWE-1104, OSV.dev

# End-of-Support Components

**MUST NOT** keep components, runtimes, or platforms in production past their vendor support end date without a dated replacement plan.

**Why:** Unsupported software receives no advisories or patches, so vulnerabilities accumulate silently while the component still passes a routine scan.

**Detect:** the dependency and runtime inventory against each vendor's published end-of-support dates

**References:** NIST SP 800-161r1 (C-SCRM, supplier support status)

# EU Cyber Resilience Act (product security lifecycle, SBOM and vulnerability handling duties)

**MUST** ship products with digital elements under a secure development lifecycle, provide an SBOM, and actively handle reported vulnerabilities for the support period.

**Why:** Unpatched connected products become botnet fodder; CRA makes manufacturers legally liable for known vulnerabilities left unfixed.

**Detect:** grep for "SBOM", "CRA", "support period", vulnerability disclosure policy; no CycloneDX/SPDX artifacts, end-of-life products with live CVEs.

**References:** EU CRA 2024/2847, ENISA SBOM guidance, ISO/IEC 30111

# Firmware Signing & Secure Boot

**MUST** sign firmware images and enforce signature verification at boot (secure boot chain) so unsigned or tampered images cannot run on devices.

**Why:** Unsigned firmware is the ultimate persistence layer — an attacker who flashes once owns the device permanently and it survives every software remediation.

**Detect:** grep build pipeline for signing steps (`sbsign`, `imgtool` (MCUboot), `openssl dgst -sign`, HSM calls); check bootloader verify-enforce (not just verify-log) mode; look for dev/test keys shipped in production images.

**References:** NIST SP 800-193 platform firmware resiliency, OWASP IoT Top 10 I4, Arm TrustZone/UEFI Secure Boot docs

# Fork Patch Tracking

**MUST** verify that a forked or renamed dependency tracks upstream security fixes before adopting it, not merely that it resolves and builds.

**Why:** Clones replicate an old snapshot without the upstream's later patches, so importing a plausible lookalike silently forfeits the fix history the original earned.

**Detect:** command compare the fork's commit log and releases against canonical upstream (`git log upstream/main ^fork/main`), recording the last synced release.

**References:** SpellBound typosquatting and code clones, https://arxiv.org/abs/2003.03471

# Hallucinated Packages

**SHOULD** verify that every package name in generated or AI-assisted code actually exists and matches intent before installing.

**Why:** Attackers pre-register plausible-sounding package names that AI models invent, so blindly installing them pulls malware into the project.

**Detect:** Install logs for names absent from the registry; review AI-generated import lines against PyPI/npm search; grep manifests for near-miss spellings of popular libs.

**References:** CWE-427, Snyk "slopsquatting" research, OWASP LLM03

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

# Image Scanning

**SHOULD** scan every container image for vulnerabilities and malware at build time and again before deployment, blocking on policy violations.

**Why:** Untested images ship known-exploitable OS packages into production, where runtime patching is rarely possible.

**Detect:** CI steps invoking `trivy image`, `grype`, or `docker scout`; absence of any scan stage in pipeline YAML; registry scan config disabled.

**References:** OWASP A06:2021, CIS Docker 4.9, NIST SP 800-190

# Commit in Trusted Repository

**MUST** resolve a pinned commit against the trusted repository itself before executing it, not merely accept that the hash is reachable through a fork network.

**Why:** Fork networks let a commit with an identical hash live in an attacker's repository, so a pinned SHA can name code you never reviewed.

**Detect:** gh api repos/OWNER/REPO/commits/SHA and confirm the returned html_url is the trusted repository

**References:** zizmor, https://github.com/zizmorcore/zizmor

# Internal Registry Proxy

**MUST** fetch dependencies through an internal registry or proxy that enforces allowlisting, malware blocking, and quarantine of new versions.

**Why:** Direct public-registry installs give every workstation and build job an unaudited path to arbitrary code. A proxy is the single choke point where policy applies and a bad version can be frozen.

**Detect:** command: `npm config get registry`, `pip config list`, `~/.m2/settings.xml`, and `.npmrc` mirror settings, plus the proxy's allowlist and quarantine policy in the platform repository.

**References:** GitHub: disrupting supply-chain attacks on npm and GitHub Actions, https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/, NIST SP 800-161 supply chain risk management

# Load-Time Integrity Verification

**SHOULD** verify a checksum or signature over interpreted code, plugins, and configuration files at load time against values recorded at deploy time.

**Why:** Deployment-time trust decays; a file modified after release executes with the application's own privileges and no other control notices.

**Detect:** grep plugin, script, and config loaders that read a file with no digest or signature check

**References:** OWASP Go Secure Coding Practices, https://github.com/OWASP/Go-SCP

# Lockfiles

**MUST** commit and honor dependency lockfiles so every install resolves to identical, audited versions.

**Why:** Unpinned resolution lets a transitive dependency change silently between builds, opening the door to typosquat and version-rollback attacks.

**Detect:** Missing `package-lock.json`, `poetry.lock`, `go.sum`; CI flags like `--no-lock`, `npm install` without `ci`; `.gitignore` excluding lockfiles.

**References:** OWASP A06:2021, CWE-829, OSV.dev, SLSA framework

# Lookalike Package Triage

**SHOULD** triage package-name-similarity alerts with registry metadata — age, downloads, maintainer history, release cadence — before treating them as malicious.

**Why:** Edit distance alone flags thousands of benign lookalikes, so teams mute the alert class; metadata turns an unusable similarity score into a triage decision.

**Detect:** `npm view <pkg> time maintainers` (or the registry API) against the canonical package, comparing publish date, maintainers, and downloads before escalating.

**References:** ConfuGuard package-confusion detection, https://arxiv.org/abs/2502.20528

# Malware Alerts on Dependencies (registry-side malware detection)

**MAY** subscribe to registry-side malware signals (npm malware advisories, PyPI malware scanning, Dependabot security alerts) and route them to a responder.

**Why:** Advisory CVE feeds lag behind live malware campaigns; registry detectors catch obfuscated install-script payloads that version scans miss entirely.

**Detect:** Dependabot/Renovate security alerts enabled in repo settings; `npm audit --audit-level=moderate`; subscribed to GitHub security advisories for owned packages.

**References:** OWASP A06:2021, npm malware policy, GitHub Advisory Database, CWE-506

# Third-party MCP/plugin trust and malicious tool-description injection

**MUST** vet, pin, and sandbox third-party MCP servers and plugins; treat their tool descriptions and names as untrusted input to the model.

**Why:** A malicious tool description can instruct the agent to exfiltrate data or chain other tools harmfully.

**Detect:** MCP config pulling unpinned packages; no approved-server allowlist; tool descriptions unsanitized at registration.

**References:** OWASP LLM03:2025, MITRE ATLAS, CWE-829

# Model Artifact Integrity (pickle-format models)

**MUST NOT** load pickle-format model artifacts (.pkl, .pt via torch.load default) from untrusted sources; prefer safetensors or verified signed formats.

**Why:** Pickle executes arbitrary code at load time, so a malicious checkpoint is remote code execution before inference starts.

**Detect:** grep torch.load( without weights_only=True, pickle.load on model files, .pkl/.ckpt pulled from Hub without checksum/signature.

**References:** OWASP LLM03:2025, CWE-502, CWE-94

# Model Version Pinning

**MUST** pin exact model versions or digests rather than floating aliases like gpt-4 or latest in production configs.

**Why:** Silent upstream model swaps change safety behavior and data-handling guarantees without any code review.

**Detect:** grep model: "latest", model: gpt-4 without dated suffix; missing digest/revision fields in inference config.

**References:** OWASP LLM03:2025, CWE-1104, NIST AI RMF MANAGE

# Mutable Image Tags (latest) Instead of Digest Pinning

**SHOULD** reference images by immutable digest (`@sha256:`) rather than floating tags like `latest` in production manifests.

**Why:** A retagged or compromised `latest` silently changes what deploys, defeating rollback and supply-chain review.

**Detect:** Image fields ending in `:latest` or bare repo names; absence of `@sha256:` digest in Deployment/Pod specs.

**References:** CIS Docker 4.5, NIST SP 800-190 §4.2.2 (stale images in registries), OWASP A08 Software Supply Chain, CWE-829

# No Binaries In Version Control

**MUST NOT** commit generated executables or opaque binary artifacts to version control.

**Why:** Binaries cannot be reviewed in a diff, so they hide planted code while adding noise that discourages review of the change.

**Detect:** command `git ls-files | xargs file | grep -Ei 'ELF|Mach-O|PE32|executable'`, and check ignore rules for build output.

**References:** OpenSSF OSPS Baseline: no generated or unreviewable binaries in VCS, https://www.bestpractices.dev/en/criteria

# Obfuscated Code Review Gap

**MUST** require reviewable source for every shipped third-party bundle, and treat a clean scan over obfuscated or minified code as no evidence.

**Why:** An adversary can iterate obfuscation until the scanner reports clean, so the gate is defeated by transformation alone rather than by a novel bug.

**Detect:** grep for vendored `.min.js` bundles and packer output with no matching source-map or upstream source reference in the lockfile.

**References:** Analyzing obfuscation against SAST pipelines (arXiv 2604.01131), https://arxiv.org/abs/2604.01131

# Pin The Expected Signer

**MUST** pin the expected signer identity for artifacts and code, not merely require that a signature validates.

**Why:** Valid code-signing certificates are sold through resellers, so signature validity answers who signed without saying whether that signer is trusted.

**Detect:** grep verification config for identity allowlists (`cosign verify --certificate-identity`, `codesign -R`, publisher rules) instead of a bare signature-valid check.

**References:** Issued for Abuse: purchasable code-signing certificates, https://arxiv.org/abs/1803.02931

# Portability as Security Property

**MUST** prefer open, standard interfaces for policy, identity, and telemetry so a provider compromise or outage does not trap the system.

**Why:** Proprietary formats on the decision path turn a single provider's incident into an un-exitable outage, because migration cost exceeds the risk tolerance.

**Detect:** read the integration ADR for each security-critical dependency and check it names an export or replacement path that has been exercised.

**References:** NIST SP 800-207 §5.6, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-161 (C-SCRM)

# Project Handoff Verification

**MUST** treat any transfer of project control - package, domain, organization or maintainer access - as a security event requiring verification and review.

**Why:** Abandoned projects get acquired and resurrected with new intent while consumers keep trusting the name. A stale domain or org handle is a ready-made supply-chain entry point.

**Detect:** Ownership changes in registry metadata and DNS/WHOIS history against a recorded handoff review.

**References:** Filippo Valsorda: compromise survey, https://words.filippo.io/dispatches/compromise-survey/

# Publishing Credential Protection

**MUST** keep package-publishing tokens and release signing keys in a protected, short-lived publishing environment, never as long-lived repository secrets.

**Why:** An attacker who can publish as you never needs to breach your build: long-lived publish tokens are the usual entry point, and a forged release reaches every consumer through the channel they already trust.

**Detect:** grep CI and repository config for `NPM_TOKEN`, `TWINE_PASSWORD`, `CARGO_REGISTRY_TOKEN`, and long-lived registry tokens; check that publishing runs from a protected environment with short-lived or trusted-publisher credentials.

**References:** SLSA v1.0 requirements, https://slsa.dev/spec/v1.0/requirements, NIST SP 800-218 (SSDF) PS.2

# Reachability-Aware Dependency Alerts

**SHOULD** alert only on vulnerable dependencies whose affected code path is reachable, and verify fixes against current versions.

**Why:** Volume-based update noise trains teams to ignore advisories, including the one that matters. Reachability turns a list of version bumps into a short list of real exposures.

**Detect:** `govulncheck ./...` or `osv-scanner --call-analysis=all` compared against a version-only scan.

**References:** Filippo Valsorda: dependabot, https://words.filippo.io/dispatches/dependabot/

# Registry Compromise Containment

**MUST** maintain a rehearsed procedure to mass-revoke registry and CI tokens and block compromised package versions within hours.

**Why:** Automated worms publish across thousands of packages and consume every token they can reach in minutes. Manual, per-incident rotation cannot keep pace with registry-scale compromise.

**Detect:** judgment: the incident runbook and its last exercise record — token inventory, bulk-revocation path, and a dependency freeze/blocklist mechanism with a measured time-to-contain.

**References:** GitHub: disrupting supply-chain attacks on npm and GitHub Actions, https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/

# Registry Outage Tolerated via Cached/Pinned Images

**SHOULD** keep images cached on nodes and pinned by digest so a registry outage does not block scheduling or restarts.

**Why:** If a pod must pull during a registry outage, rescheduling and rollouts stall, turning a third-party outage into a cluster outage.

**Detect:** No `imagePullPolicy: IfNotPresent`/`Never` with pre-pulled images; no local registry mirror or pull-through cache configured.

**References:** K8s docs imagePullPolicy, Harbor/Docker registry mirror docs, OWASP A08

# Reproducible Builds

**SHOULD** produce bit-for-bit reproducible artifacts by eliminating timestamps, random paths, and nondeterministic ordering from builds.

**Why:** Non-reproducible output makes it impossible to verify that a deployed binary matches its reviewed source, hiding tampered releases.

**Detect:** `SOURCE_DATE_EPOCH` unset; build scripts embedding `date`/`hostname`; `-trimpath` absent in Go builds; unreproducible flag in `reproducible-builds.org` checks.

**References:** reproducible-builds.org, SLSA L3

# Rotatable Trust Root

**MUST** distribute update and verification roots through a versioned, rotatable metadata mechanism instead of a key baked into the client.

**Why:** A root key compiled into firmware or a client cannot be replaced when it leaks or expires, stranding every deployed device on a dead trust anchor.

**Detect:** Embedded PEM blocks or single pinned public keys in update-client code (`BEGIN PUBLIC KEY` in the updater) with no fetched, versioned root metadata.

**References:** Sigstore Fulcio, https://github.com/sigstore/fulcio, The Update Framework (TUF) specification

# SBOM Generation & Retention (CycloneDX/SPDX per build, kept for incident response)

**MUST** generate a CycloneDX or SPDX SBOM per build and retain it long enough to answer "were we affected?" in incidents.

**Why:** Without per-build inventories, Log4Shell-style emergencies become weeks of guesswork instead of minutes of lookup.

**Detect:** grep `bom-*.json`, `cyclonedx`, `spdx`, `syft`, `cdxgen` in CI pipelines and artifact repos.

**References:** NTIA SBOM minimum elements, NIST SP 800-161, OWASP CycloneDX, CWE-1357

# SBOM Minimum Elements

**MUST** publish an SBOM per build that names each component's supplier, version, and unique identifier with its dependency edges, and declares what the scan did not cover.

**Why:** An SBOM missing a minimum element cannot answer which version is affected or whom to notify, and an undeclared gap is read as coverage that was never produced.

**Detect:** grep each components[] entry for supplier, version, purl and dependencies, and for a declared scope or completeness field

**References:** NTIA SBOM minimum elements conformance checker, https://github.com/spdx/ntia-conformance-checker

# Secret Scanning

**MUST** run automated secret scanning (gitleaks, trufflehog, GitHub push protection) on every commit and full-history scans before publishing any repository.

**Why:** Developers routinely commit live credentials under deadline pressure; without scanning, leaks ship silently to public or shared remotes — and a secret once committed stays in git history forever, so rotation is the only true fix and is often missed.

**Detect:** `.gitleaks.toml`, `.pre-commit-config.yaml` with gitleaks/trufflehog hooks that reject at commit/push time, absent GitHub `secret_scanning`/push-protection settings in org config.

**References:** OWASP ASVS V2.10.4, CWE-540, CWE-319, NIST SP 800-218 (SSDF), GitHub push protection docs

# Secure Development Attestation

**SHOULD** retain signed, per-release evidence that the documented secure-development practices were followed, in a form a customer can verify.

**Why:** Procurement increasingly asks for attestation rather than a questionnaire, and evidence invented after the fact is worthless. Unsigned claims of practice cannot be distinguished from aspiration.

**Detect:** judgment: the release artifacts — a signed attestation or provenance bundle per version, mapped to the practices it claims and retrievable by version.

**References:** CISA Secure Software Development Attestation Form, https://www.cisa.gov/resources-tools/resources/secure-software-development-attestation-form, NIST SP 800-218 (SSDF)

# Short-Lived Signing Identity

**MUST** sign artifacts with short-lived credentials bound to a verified workload identity rather than long-lived static keys.

**Why:** A static signing key is a permanent impersonation token: whoever steals it signs as you forever. Minutes-scale certificates leave almost no window.

**Detect:** Keyless `cosign sign` with an OIDC-issued Fulcio certificate; flag long-lived `cosign.key` or GPG keys held in CI secrets.

**References:** Sigstore Fulcio, https://github.com/sigstore/fulcio

# Signed Commits

**SHOULD** require cryptographically signed commits on protected branches so authorship and provenance stay verifiable after the fact.

**Why:** Without signing, anyone who can reach the repository can attribute a change to a colleague, and provenance ends at the forge's own logs. Signature verification is what makes the history evidence.

**Detect:** command: `git log --show-signature` or `git verify-commit` over the branch range in CI, plus a branch-protection setting that rejects unsigned commits.

**References:** NCSC: protect your code repository, https://www.ncsc.gov.uk/collection/developers-collection/principles/protect-your-code-repository, SLSA v1.0 source requirements

# Signing Transparency Log

**MUST** record signing events in an append-only transparency log that verifiers can audit independently of the signer.

**Why:** Without a public log a compromised signer can forge artifacts and nobody can prove it happened. The log makes signing history auditable after the fact.

**Detect:** `rekor-cli get --uuid` or `cosign verify --certificate-identity` resolving an inclusion proof for each released artifact.

**References:** Sigstore Rekor, https://github.com/sigstore/sigstore, Sigstore Fulcio, https://github.com/sigstore/fulcio

# Source Release Integrity

**MUST** publish source packages containing only version-controlled content, and require consumers to build generated artifacts themselves.

**Why:** A pre-generated file shipped inside a source tarball is trusted by everyone who installs it and verified by nobody. Building from source in the consumer's pipeline removes that unearned trust.

**Detect:** command: `npm pack --dry-run`, `tar -tzf dist/*.tar.gz`, or `python -m build --sdist` inspected for generated artifacts (compiled binaries, bundled output) absent from the repository.

**References:** OpenSSF Concise Guide for Developing More Secure Software, https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Concise-Guide-for-Developing-More-Secure-Software.md, SLSA v1.0 requirements

# Subresource Integrity

**MUST** require integrity hashes on every externally hosted script or stylesheet, or record an explicit exception with its rationale.

**Why:** A third-party host or CDN that is compromised, or a package that is deleted and re-registered, serves attacker code into the page with full origin privileges.

**Detect:** grep `<script src="http` and `<link href="http` for missing `integrity=` attributes.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, W3C Subresource Integrity

# Toolchain Compromise Modeling

**MUST** include build and design toolchains such as firmware compilers, hardware design flows, and training pipelines in the supply-chain threat model.

**Why:** A purely software compromise of the tooling rewrites the artifact, so hardware-grade assurance is only as strong as the pipeline that produced it.

**Detect:** compare the provenance and SBOM scope against the toolchain inventory; build tooling absent from both is unmodelled trust.

**References:** SOLARBURST-go-silicon (arXiv 2610.22580), https://arxiv.org/abs/2610.22580

# Tokenless Artifact Publishing

**SHOULD** publish artifacts through short-lived federated identity instead of long-lived registry API tokens stored in CI.

**Why:** A publish token is stealable, rarely rotated, and usually scoped wider than one release; a federated identity exists only for the job.

**Detect:** grep NPM_TOKEN, PYPI_API_TOKEN, or CARGO_REGISTRY_TOKEN secrets in publish workflows; expect id-token: write instead

**References:** zizmor, https://github.com/zizmorcore/zizmor

# Untrusted Lookup Targets

**MUST NOT** let untrusted input choose a name-resolution, class-loading, or remote-fetch target inside an interpreter or template.

**Why:** Lookup mechanisms turn a data field into code or network reach: a logged string becomes an outbound directory request, a filename becomes a loaded class. The attacker chooses what executes or where the request goes.

**Detect:** grep `InitialContext.lookup`, `Class.forName(`, `importlib.import_module`, dynamic `require(`/`import(` with request-derived arguments, and template calls that accept a variable template name.

**References:** Cloudflare Log4j response, https://blog.cloudflare.com/how-cloudflare-security-responded-to-log4j2-vulnerability/, OWASP Injection Prevention Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html, CWE-470 Use of Externally-Controlled Input to Select Classes or Code

# Updaters Must Not Execute Manifests

**MUST NOT** allow a dependency updater to execute install or setup scripts from the dependencies it processes.

**Why:** Install and setup scripts in a freshly updated dependency run with the updater's credentials, turning an update into code execution.

**Detect:** grep insecure-external-code-execution or --allow-exec flags in updater configuration

**References:** zizmor, https://github.com/zizmorcore/zizmor

# Vendor/third-party risk management and subprocessor registers

**MUST** vet critical suppliers at onboarding and re-review their security posture on a fixed cadence.
**SHOULD** maintain a current register of every vendor and its subprocessors with review dates, data access scope, and breach-notification terms.

**Why:** Breaches frequently originate downstream; without a register you cannot assess exposure or notify affected parties when a vendor falls. A single compromised or negligent vendor becomes your breach: SolarWinds showed one upstream can poison thousands of downstream users.

**Detect:** Missing vendor register doc or spreadsheet; SaaS admin lists without subprocessor pages checked; contracts lacking breach-notification SLA clauses; no `vendor_risk`/`supplier_assessment`/`C-SCRM` records in third-party inventories, due-diligence records, or SBOM ingestion configs.

**References:** NIST SP 800-161, NIST SSDF (SP 800-218), SOC 2 CC9.2, GDPR Art. 28, ISO 27036

# Vendored Code Ownership

**MUST** assign a named owner and a documented upstream-fix process to every vendored or forked dependency before it enters the tree.

**Why:** A vendored copy stops receiving fixes the moment it is copied, yet it still looks like a normal dependency in the manifest. The fork becomes permanent unpatched surface that no scanner attributes to you.

**Detect:** judgment: `vendor/`, `third_party/`, and submodule trees, matched against CODEOWNERS and a documented patch or upgrade path for each.

**References:** NIST SP 800-218 (SSDF) PW.4, OpenSSF Concise Guide for Developing More Secure Software, https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Concise-Guide-for-Developing-More-Secure-Software.md

# Declare Non-Exploitability

**MUST** publish an explicit non-exploitability statement for every known vulnerability in shipped components that you are not fixing.

**Why:** Silence on a present-but-unreachable component makes every scan a false emergency and hides the exposures that are real.

**Detect:** command diff `trivy` or `grype` findings against the repo's OpenVEX document and flag any finding with no status entry.

**References:** OpenSSF OSPS Baseline: VEX for non-affecting vulnerabilities, https://www.bestpractices.dev/en/criteria, OpenVEX specification

