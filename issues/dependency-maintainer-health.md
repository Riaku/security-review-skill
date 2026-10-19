---
categories: [supply-chain]
domains: [governance]
---

# Dependency Maintainer Health

**SHOULD** treat maintainer dormancy, ownership transfer, or single-maintainer status in a critical dependency as a security event requiring review.

**Why:** Registry compromises usually arrive through a trusted maintainer account rather than a vulnerability. Abandoned or handed-over projects lose the one person who would have noticed the malicious release.

**Detect:** command: `npm view <pkg> maintainers time.modified`, `pip index versions`, or the registry API for maintainer list and last publish date, compared against the review date in the dependency register.

**References:** OpenSSF analysis of the xz backdoor, https://openssf.org/blog/2024/04/30/more-continuous-security-validation-faster-detection-of-the-xz-lib-backdoor/, event-stream maintainer handover, https://github.com/dominictarr/event-stream/issues/116
