---
categories: [mobile]
domains: [mobile]
---

# Peer App Signing Identity

**MUST** identify peer applications by signing-certificate digest, never by package name or a self-declared identifier alone.

**Why:** Package names are global and can be squatted, and any app can claim a caller name. Only the signing certificate proves who is on the other end.

**Detect:** `getPackageInfo(` calls using `GET_SIGNATURES`/`checkSignatures`, and IPC servers authorizing callers by `packageName` only.

**References:** JSSEC Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en.pdf
