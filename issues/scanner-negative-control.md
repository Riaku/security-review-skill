---
categories: [testing-strategy]
domains: [backend]
---

# Negative Control for Security Scanners

**MUST** validate each security scanner against a fixture with a known finding before trusting a clean result on real code.

**Why:** A scanner that crashes, misconfigures, or skips its target reports no findings, which is indistinguishable from a clean codebase.

**Detect:** run the scanner in CI against a seeded vulnerable fixture and assert the expected finding is reported

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook, AppSec Guide, https://appsec.guide/
