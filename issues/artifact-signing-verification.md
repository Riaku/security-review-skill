# Artifact Signing & Verification at Deploy (cosign/sigstore verify before run)

**MUST** verify signatures (cosign/sigstore) on images and release artifacts at deploy time, rejecting unsigned or mismatched ones.

**Why:** An unsigned image pulled into production may be a tampered one; the deploy boundary is the last honest checkpoint.

**Detect:** grep `cosign verify`, `sigstore`, Kyverno `verifyImages`, `signature_verification: true`, `--verification-policy` in deploy pipelines.

**References:** SLSA levels 3-4, sigstore/cosign docs, NIST SP 800-218 PW.6, CWE-347
