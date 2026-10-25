# supply-chain

Dependencies, artifacts, build provenance.

## What this category covers

This category covers everything a build pulls in and everything it produces: third-party dependencies, the tooling that fetches them, and the signed artifacts and provenance that let you answer whether a given component was affected. Its member items span dependency resolution (lockfiles, dependency confusion, hallucinated packages, vulnerability and malware alerts), the build itself (hermetic and reproducible builds, CI action pinning, IaC plans from untrusted PRs), artifacts and provenance (SLSA-style attestation, SBOM generation and retention, image scanning, image and firmware signing, digest pinning, registry-outage tolerance), secret scanning, and vendor risk (NIST SP 800-161 supplier vetting, subprocessor registers, the EU Cyber Resilience Act). A reviewer here should be able to name, for any released artifact, what it is made of, who built it, and whether it was tampered with between build and run. The recurring failure is a component that entered the build from an unpinned, unverified, or unexpected source and left no record behind.

- Dependency integrity: lockfiles, unpinned or confusable packages, advisory and malware signals.
- Build integrity: hermetic and reproducible builds, pinned runtime and toolchain versions, CI action pinning, untrusted-PR plans.
- Artifact provenance: signed attestation, SBOM generation and retention, verification at deploy.
- Image and firmware trust: scanning, digest pinning, signing, registry-outage tolerance.
- Secret scanning across history and pushes.
- Vendor and supplier risk: NIST SP 800-161 vetting, subprocessor registers, EU Cyber Resilience Act duties.

## What it does not cover

- [cicd-pipeline-security](../categories/cicd-pipeline-security.md) — the pipeline's own credentials, permissions, and runner isolation belong there; the dependencies and artifacts flowing through it belong here.
- [containers-k8s](../categories/containers-k8s.md) — runtime pod and cluster configuration belongs there; image provenance, scanning, and digest pinning belong here.
- [third-party-integrations](../categories/third-party-integrations.md) — runtime SaaS integrations and their credentials belong there; build-time and vendor-provenance concerns belong here.
- [ai-llm](../categories/ai-llm.md) — model behavior, prompting, and output handling belong there; the integrity of the model artifact itself and third-party MCP/plugin trust belong here.

## What a finding here looks like

- a dependency resolved from a public registry under a name that should have come from the internal index.
- a third-party CI action referenced by a mutable tag instead of a commit SHA.
- a released artifact with no signed provenance and no SBOM, so an advisory cannot be triaged against it.
- `terraform apply` running automatically from a forked pull request.
- a production manifest referencing an image by `latest` instead of a digest.
- a build job resolving `lts/*` or `stable` while the repository pins no toolchain version.
