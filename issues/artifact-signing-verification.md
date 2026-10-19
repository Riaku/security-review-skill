---
categories: [deployment-release, supply-chain]
domains: [infrastructure]
---

# Artifact Signing & Verification at Deploy (cosign/sigstore verify before run)

**MUST** verify cosign/sigstore signatures on images and release artifacts at deploy time, rejecting unsigned or mismatched ones.

**Why:** An unsigned image pulled into production may be a tampered one; the deploy boundary is the last honest checkpoint.

**Detect:** grep `cosign verify`, `sigstore`, Kyverno `verifyImages`, `signature_verification: true` in deploy pipelines.

**References:** SLSA Build Level 3, sigstore/cosign docs, NIST SP 800-218 (SSDF), CWE-347
