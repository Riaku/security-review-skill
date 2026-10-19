---
categories: [compliance-privacy]
domains: [data]
---

# Track the Privacy Budget

**MUST** track cumulative privacy budget across every query and release of a dataset published under differential privacy, and refuse further releases once the budget is exhausted.

**Why:** Epsilon is not a per-query setting: noisy answers compose, so ten queries at epsilon 1 can isolate an individual even though each looked harmless in isolation.

**Detect:** grep query paths for an `epsilon` argument with no accumulator behind it — no budget store keyed by dataset and analyst, or accounting that resets between sessions; confirm the limit is enforced server-side, not in a client default.

**References:** Dwork & Roth, The Algorithmic Foundations of Differential Privacy, https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf, Google differential-privacy library, https://github.com/google/differential-privacy, NIST SP 800-226, https://csrc.nist.gov/pubs/sp/800/226/final
