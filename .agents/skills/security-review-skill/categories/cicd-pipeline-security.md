# cicd-pipeline-security

CI/CD system as an attack surface.

## What this category covers

This category covers the build and delivery system as an attack surface in its own right: who can change it, what it executes, and what credentials it holds. Member items span workflow triggers, runner isolation, action and image pinning, secret handling in logs and build layers, deploy-credential scope, and the review gates that decide what merges. They also cover build integrity — hermetic builds, signed provenance and SBOMs, benchmark and static-analysis gates — and the governance of unattended agents. A reviewer should expect findings about a pipeline step that runs attacker-controlled content with production authority, or a gate that reports success without blocking anything.

- Triggers and privilege: privileged workflow triggers, infrastructure plan or apply from forks, and privileged build steps.
- Runner and workspace isolation: ephemeral runners, shared caches, and Docker-in-Docker.
- Supply of build inputs: unpinned actions, mutable tags, and undeclared network dependencies.
- Secret exposure: build logs, build arguments, image layers, and deploy credentials shared across jobs.
- Merge gates: branch protection, independent review, enforced rather than advisory scans, and review config the change cannot edit.
- Agent automation: AI review that actually fails, and scheduled or webhook-triggered agents with bounded tools.

## What it does not cover

- [supply-chain](../categories/supply-chain.md) — dependency selection, third-party artifact trust, and provenance of upstream components belong there.
- [deployment-release](../categories/deployment-release.md) — what happens to the artifact after it leaves the pipeline belongs there.
- [secrets-crypto](../categories/secrets-crypto.md) — secret storage and rotation belong there; this category covers their exposure through the pipeline.

## What a finding here looks like

- A workflow holding write tokens or secrets checks out and executes code from a fork or untrusted pull request.
- A third-party action or build image is referenced by tag rather than commit SHA or digest.
- A secret is printed to build output, baked into an image layer, or passed as a plain build argument.
- A required scan or AI review reports neutral or success while findings remain open.
- Deploy credentials for every environment are available to every job, so one compromised workflow reaches production.
