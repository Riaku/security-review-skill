---
categories: [secrets-crypto]
domains: [backend]
---

# Explicit Cipher Transformation

**MUST** name the full cipher transformation, including algorithm, mode, and padding, at every call site, and reject provider defaults.

**Why:** Provider defaults have historically resolved to ECB or PKCS#1 v1.5, so the same call is safe or broken depending on the runtime and its version.

**Detect:** grep for transformation strings without a mode (Cipher.getInstance("AES")), for /ECB/, and for manual CBC built on a bare block cipher

**References:** Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en_20250827.pdf
