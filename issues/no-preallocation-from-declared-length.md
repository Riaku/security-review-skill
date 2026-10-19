---
categories: [correctness-pitfalls]
domains: [backend]
---

# No Preallocation From Declared Length

**MUST NOT** size buffers, vectors, or collections from a length the untrusted caller declares before the corresponding data arrives.

**Why:** Reserving a declared length up front lets one small request allocate gigabytes, and the validation happens after the memory is already committed.

**Detect:** grep with_capacity(, reserve(, new byte[, Buffer.alloc(, malloc( whose argument comes from a request field or deserialized header

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook
