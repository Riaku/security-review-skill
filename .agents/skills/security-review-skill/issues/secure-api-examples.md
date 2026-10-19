---
categories: [documentation-quality]
domains: [backend]
---

# Secure API Examples

**MUST** ship a complete, secure, copy-ready example for every security-sensitive API, and review that example as production code.

**Why:** Developers copy the example rather than the prose; when it is missing or unsafe they improvise the crypto, and the vulnerability ships with the library's blessing.

**Detect:** judgment — for each auth, crypto, and signing API in the docs, confirm an end-to-end example with key generation, error handling, and no placeholder secrets.

**References:** CryptoExamples controlled experiment, https://arxiv.org/abs/1807.01095
