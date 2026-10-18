# CSPM Continuous Cloud Posture Scanning (misconfig drift detected continuously)

**MUST** scan cloud configuration continuously for misconfigurations rather than relying on point-in-time audits.

**Why:** Public buckets, open security groups, and disabled logging appear between audits; attackers scan for them constantly.

**Detect:** grep for CSPM tooling: `prowler`, `scoutsuite`, `cloudsploit`, `Palo Alto Prisma`, `Wiz`, `checkov --framework cloud`, scheduled posture-scan CI jobs and alert routing.

**References:** NIST CS2 (SP 800-223 CSPM), CIS Benchmarks for AWS/Azure/GCP, NIST SP 800-53 CM-6, CWE-16
