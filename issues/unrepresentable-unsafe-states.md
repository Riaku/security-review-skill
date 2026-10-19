---
categories: [correctness-pitfalls]
domains: [backend]
---

# Make Unsafe States Unrepresentable

**SHOULD** encode security-relevant state in types or schema constraints so illegal combinations cannot be constructed by a careless caller.

**Why:** Rules enforced by convention fail at the first forgotten check; rules enforced by the type system or schema fail at build time.

**Detect:** grep parallel boolean flags (`is_active`, `is_deleted`, `is_pending`), nullable `user_id`/`tenant_id` pairs, and status strings compared as free text.

**References:** NIST SP 800-218 SSDF, https://csrc.nist.gov/pubs/sp/800/218/final, Rust API Guidelines, https://rust-lang.github.io/api-guidelines/, Anderson, Security Engineering, https://www.cl.cam.ac.uk/~rja14/book.html
