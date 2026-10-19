---
categories: [documentation-quality]
domains: [backend]
---

# BCP 14 Keyword Usage (RFC 2119 + RFC 8174)

**MUST** use requirement keywords (MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, OPTIONAL) in ALL CAPS where a requirement is intended, since only all-caps usage carries the BCP 14 meaning (RFC 8174 §2), and **SHOULD** include near the beginning of a spec, API doc, or policy document the RFC 8174 boilerplate wording "are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals".

**Why:** Mixed-case or casual "should/must" makes requirements ambiguous — readers can't tell a hard requirement from advice, and compliance reviews can't cite them.

**Detect:** grep docs for lowercase must/should/may in requirement contexts; check specs include the RFC 2119/8174 keyword-definition boilerplate; flag "must" used as emphasis rather than obligation.

**References:** RFC 2119, RFC 8174 §2, IETF BCP 14
