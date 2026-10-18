---
categories: [mobile]
domains: [mobile]
---

# Mobile Secure Storage (Keychain/Keystore)

**MUST NOT** store tokens, credentials, or PII in SharedPreferences, UserDefaults, plaintext files, or web localStorage; use Keychain (iOS) or EncryptedSharedPreferences backed by the Keystore (Android).

**Why:** Rooted or backed-up devices expose world-readable storage, handing attackers live session tokens and personal data.

**Detect:** grep `SharedPreferences`, `UserDefaults`, `localStorage` near `token`, `password`, `api_key`; check for `kSecAttrAccessible` / `EncryptedSharedPreferences` usage.

**References:** OWASP MASVS-STORAGE-1, CWE-922, CWE-312, NIST SP 800-63B

---

**Part of:** [mobile](../categories/mobile.md) · [mobile](../domains/mobile.md) · [SKILL.md](../SKILL.md)
