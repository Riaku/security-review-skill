# Artifact Signing & Verification at Deploy (cosign/sigstore verify before run)

**MUST** verify signatures (cosign/sigstore) on container images and release artifacts at deploy time, rejecting anything unsigned or mismatched.

**Why:** An unsigned image pulled into production may be a tampered one; verification at the deploy boundary is the last honest checkpoint.

**Detect:** grep for `cosign verify`, `sigstore`, `signature_verification: true`, Kyverno `verifyImages`, admission signature policies, `--verification-policy` in deploy pipelines.

**References:** SLSA levels 3-4, sigstore/cosign docs, NIST SP 800-218 PW.6, CIS Docker Benchmark 4.x, CWE-347
