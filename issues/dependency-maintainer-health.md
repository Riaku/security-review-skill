---
categories: [supply-chain]
domains: [governance]
---

# Dependency Maintainer Health

**SHOULD** treat maintainer dormancy, ownership transfer, or single-maintainer status in a critical dependency as a security event requiring review.

**Why:** Registry compromises usually arrive through a trusted maintainer account rather than a vulnerability. Abandoned or handed-over projects lose the one person who would have noticed the malicious release.

**Detect:** command: `npm view <pkg> maintainers time.modified`, `pip index versions`, or the registry API for maintainer list and last publish date, compared against the review date in the dependency register.

**References:** xz backdoor announcement (upstream maintainer page), https://tukaani.org/xz-backdoor/, event-stream maintainer handover, https://github.com/dominictarr/event-stream/issues/116
