# Tooling Reference — Scanners & Security Tools

Curated map of widely used tools referenced by checklist items. Tool names in
`Detect:` lines point here: the tools an item is checked with are named in that
item's own `Detect:` line, so there is no central tool→issue index to keep in
step. This list is advisory, not exhaustive;
presence of a tool does not imply endorsement, and any tool may be
substituted with an equivalent from the same class.

## Static analysis (SAST)

| Tool | Class | What it checks |
|---|---|---|
| Semgrep | SAST, polyglot, rule-driven | Custom + community security rules across 30+ languages |
| CodeQL | SAST, query engine (GitHub) | Dataflow/taint analysis, deep vulnerability queries |
| SonarQube / SonarCloud | SAST + quality gate | Bugs, code smells, security hotspots, coverage |
| Bandit | SAST (Python) | Python-specific insecure patterns |
| Brakeman | SAST (Rails) | Rails app vulnerabilities |
| gosec / Gosec | SAST (Go) | Go security problems |
| Staticcheck | Static (Go) | Correctness and perf lints (complements gosec) |
| Clippy | Static (Rust) | Rust lints incl. safety patterns |
| ESLint security plugins | Static (JS/TS) | `eslint-plugin-security`, `eslint-plugin-react` XSS rules |
| SpotBugs + Find Security Rules | SAST (JVM) | Java/Kotlin security bugs |
| Megalinter | Meta-linter | Orchestrates many linters/scanners in one CI job |
| pre-commit | Meta-hook runner | Runs linters/scanners pre-commit |

## Secret scanning

| Tool | Class | What it checks |
|---|---|---|
| Gitleaks | Secret scanner (git history + working tree) | API keys, tokens, private keys by regex/entropy |
| TruffleHog | Secret scanner | Credentials + verified live-key detection |
| detect-secrets (Yelp) | Secret scanner + baseline | Pre-commit secret detection with baseline file |
| TruffleHog / Git-secrets | Git hook scanners | Block secrets at commit |
| GitHub Push Protection | Platform-side | Blocks secrets at push, org-wide |

## Dependency & supply-chain scanning

| Tool | Class | What it checks |
|---|---|---|
| Trivy | Unified scanner | Deps, containers, IaC, secrets, misconfig |
| Grype | Container/FS vulnerability scanner | Image layers vs vulnerability DBs |
| osv-scanner | OSV.dev-backed scanner | Ecosystem-agnostic dependency CVEs |
| OWASP Dependency-Check | Java-focused dep scanner | Maven/Gradle/NuGet CVE matching |
| npm audit / pnpm audit | Node dep scanner | package-lock vulnerabilities |
| pip-audit | Python dep scanner | PyPI vulnerabilities |
| cargo audit / cargo deny | Rust dep scanner | RustSec advisory DB, license policy |
| Snyk | SaaS SAST + deps | Deps, containers, IaC, code |
| Renovate / Dependabot | Update automation | Keeps deps patched (a control, not a scanner) |

## SBOM, signing & provenance

| Tool | Class | What it checks |
|---|---|---|
| Syft | SBOM generator | Container/FS inventory (CycloneDX/SPDX) |
| cosign | Artifact signing | Container/image sign + verify (sigstore) |
| Sigstore / Fulcio / Rekor | PKI + transparency | Keyless signing, public audit log |
| in-toto | Supply-chain attestation | Step/attestation framework (SLSA substrate) |
| SLSA provenance generators | Provenance | Build-level provenance (GitHub Actions, BuildKit) |

## IaC & cloud configuration scanning

| Tool | Class | What it checks |
|---|---|---|
| Checkov | IaC scanner | Terraform/CloudFormation/K8s/Helm misconfig |
| tfsec | IaC scanner (Terraform) | Terraform security risks |
| terrascan | IaC scanner | Multi-provider policy checks |
| kube-score / kube-linter (Datadog) | K8s manifest linting | Hardening best practices |
| kubesec | K8s risk scoring | Security risk analysis on manifests |
| Prowler | CSPM | AWS/Azure/GCP/K8s vs CIS, FedRAMP, PCI |
| ScoutSuite | Multi-cloud audit | Cloud posture reporting |
| CloudSploit | Cloud posture | AWS/Azure/GCP misconfigs |
| IAM Access Analyzer (AWS) | IAM analysis | Resource-policy reachability |
| policy_sentry | IAM design | Least-privilege policy builder, dangerous-policy lint |
| driftctl / Terraform drift plans | Drift detection | Live cloud vs IaC diff |

## Dynamic testing (DAST) & web assessment

| Tool | Class | What it checks |
|---|---|---|
| OWASP ZAP | DAST | Automated web app scanning, CI integration |
| Burp Suite (Pro/Community) | DAST + manual proxy | Web request interception, scanner |
| Nuclei | Template-based scanner | CVE/pattern checks at scale (also recon) |
| Nikto | Legacy web scanner | Server misconfigs, dangerous files |
| Arachni | DAST framework | Crawler + scanner (maintenance paused) |
| sqlmap | Specialized DAST | SQL injection verification |
| dalfox | Specialized DAST | XSS scanner (reflected/DOM) |
| ffuf / wfuzz | Fuzzers (content/API) | Directory/param fuzzing |
| httpx / katana | Crawlers | HTTP probing, URL discovery |

## Runtime & container detection

| Tool | Class | What it checks |
|---|---|---|
| Falco | Runtime threat detection (eBPF) | Syscall anomalies, reverse shells, file changes |
| Tetragon (Cilium) | eBPF enforcement | Network/process observability + enforcement |
| Sysdig Secure / OSS sysdig | Runtime + forensics | Container syscalls, drift, policies |
| Tracee (Aqua) | eBPF runtime | Host/container attack signatures |
| Docker Bench for Security | Host check | CIS Docker benchmark runner |
| kube-bench | Node check | CIS Kubernetes benchmark runner |
| Lynis | Host audit | Linux host hardening scan |
| Pamie / sysdig cloud-siem | Cloud SIEM | Log-based detection (class) |

## Fuzzing

| Tool | Class | What it checks |
|---|---|---|
| AFL++ | Coverage-guided fuzzer | Binaries/parsers, file & network formats |
| libFuzzer | In-process fuzzer (C/C++) | Library entry points |
| go-fuzz / native go fuzz | Fuzzer (Go) | Go functions |
| Jazzer | Fuzzer (JVM) | Java code, OSS-Fuzz integration |
| cargo-fuzz / honggfuzz-rs | Fuzzer (Rust) | Rust functions |
| Atheris | Fuzzer (Python) | Python code (libFuzzer-backed) |

## Recon & external attack surface

| Tool | Class | What it checks |
|---|---|---|
| Amass | Subdomain enumeration | Attack-surface discovery |
| Subfinder | Subdomain enumeration | Passive/active subdomain discovery |
| Shodan / Censys | Internet-wide scan | Exposed services fingerprinting |
| ProjectDiscovery suite (httpx, nuclei, naabu) | Recon + scan | Live hosts, ports, templates |
| CloudBrute | Cloud bucket hunting | Exposed storage/buckets |

## Usage notes for reviewers

- Prefer running 2–3 complementary classes (SAST + secret + dep) over one
  "everything" tool; each class misses what others catch.
- Tool output is input to findings, not the finding itself: ground every
  finding in file:line you read, per the skill's verification rule.
- Pin scanner versions and rule bundles in CI for reproducibility
  (see `pinned-ci-actions`).
- False-positive triage is part of the review; record suppressed findings with
  justification rather than deleting them.
