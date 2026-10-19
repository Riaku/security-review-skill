---
categories: [compliance-privacy, supply-chain]
domains: [governance]
---

# Inbound Grants Match Outbound Licence

**MUST** require every contribution to carry an inbound grant no broader than the project's outbound licence — DCO sign-off, CLA, or explicit statement — enforced in CI, not by goodwill.

**Why:** One patch copied from a differently licensed project can force the whole distribution onto terms the project never chose, and unsigned history leaves no way to prove provenance afterwards.

**Detect:** grep commit trailers and PR metadata for `Signed-off-by`, a CLA-bot label, or a CONTRIBUTING section stating contribution terms; flag merged PRs that carry none of the three, and vendored files with no origin note.

**References:** Developer Certificate of Origin, https://developercertificate.org/, ASF Contributor License Agreements, https://www.apache.org/licenses/contributor-agreements.html, REUSE Specification, https://reuse.software/spec/
