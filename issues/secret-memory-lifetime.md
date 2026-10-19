---
categories: [secrets-crypto]
domains: [backend]
---

# Secret Memory Lifetime

**SHOULD** minimize how long secrets and decrypted key material live in process memory, wiping buffers as soon as they are no longer needed.

**Why:** A single memory-disclosure bug or core dump walks the heap and finds whatever the process forgot to wipe. Long-lived plaintext secrets turn a read primitive into credential theft.

**Detect:** grep for `mlock`, `explicit_bzero`, `memset_s`, `Zeroize`, or equivalent wipe calls on buffers holding keys; flag key material copied into long-lived objects, caches, or log statements.

**References:** Heartbleed, https://heartbleed.com/, CWE-316 Cleartext Storage of Sensitive Information in Memory
