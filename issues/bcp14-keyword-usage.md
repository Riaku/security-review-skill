# BCP 14 Keyword Usage (RFC 2119 + RFC 8174)

**MUST** use requirement keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) in ALL CAPS with their RFC 2119/8174 meanings in specs, API docs, and policy documents, and define them on first use per RFC 8174 §3.

**Why:** Mixed-case or casual "should/must" makes requirements ambiguous — readers can't tell a hard requirement from advice, and compliance reviews can't cite them.

**Detect:** grep docs for lowercase must/should/may in requirement contexts; check specs include the RFC 2119/8174 keyword-definition boilerplate; flag "must" used as emphasis rather than obligation.

**References:** RFC 2119, RFC 8174 §3, IETF BCP 14

---

**Part of:** [documentation-quality](../categories/documentation-quality.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
