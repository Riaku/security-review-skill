---
categories: [security-practices]
domains: [governance]
---

# Artifact Evidence for Claims

**SHOULD** credit a security practice only when its artifact exists in the repository, such as a fuzz target, a test, or a gate config, never from a README claim.

**Why:** Claims drift while artifacts do not, and a check that names the signal proving each practice is both automatable and honest.

**Detect:** grep LLVMFuzzerTestOneInput, func Fuzz, import atheris for a fuzzing claim; repeat with the artifact each other claim implies

**References:** OpenSSF Scorecard, https://github.com/ossf/scorecard
