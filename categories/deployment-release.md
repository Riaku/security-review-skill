# deployment-release

Release engineering: strategies, environments, versioning.

## What this category covers

This category covers how code and configuration move from a reviewed commit to a running production system. Member items span rollout strategies, environment parity, artifact promotion, release hooks, migration cutover, and rollback. They also cover the infrastructure side of releasing — infrastructure as code, GitOps reconciliation, drift detection, policy gates, and where release secrets and state live. A reviewer should expect findings about whether what was tested is what runs, whether a bad release can be reversed, and whether an out-of-band change can bypass the release path entirely.

- Rollout strategy: blue-green, canary gates, and traffic cutover.
- Artifact promotion: build once, immutable digests, signed provenance, and version semantics.
- Release mechanics: Helm hook order, startup dependency ordering, and one-off admin processes.
- Change control: infrastructure as code under review, GitOps as the source of truth, and drift between live state and Git.
- Reversibility: rehearsed rollbacks, backward-compatible migrations, and code/data rollback pairing.
- Environment hygiene: staging parity, masked data, debug-mode exclusion, and plaintext-secret avoidance.

## What it does not cover

- [cicd-pipeline-security](../categories/cicd-pipeline-security.md) — runner isolation, workflow injection, and the pipeline's own credentials belong there; this category starts at the artifact.
- [containers-k8s](../categories/containers-k8s.md) — pod specs, probes, and runtime cluster configuration belong there.
- [database](../categories/database.md) — schema design, query correctness, and migration internals belong there; this category covers only the release sequencing around them.

## What a finding here looks like

- A per-environment rebuild produces a binary that differs from the one that passed staging review.
- A code rollback runs past a destructive migration, and the old binary writes against a schema it no longer matches.
- A Helm migration hook fails but the rollout proceeds, starting new pods against an unmigrated schema.
- A hand-applied manifest diverges from the Git revision, and drift detection either alerts late or is absent.
- A rollback path exists on paper but has never been executed, and its down-migration is untested.
