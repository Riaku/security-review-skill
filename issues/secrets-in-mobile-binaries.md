---
categories: [mobile, secrets-crypto]
domains: [backend, mobile]
---

# Hardcoded API keys and secrets in mobile app binaries

**MUST NOT** embed API keys, tokens, or symmetric secrets in app source, assets, or compiled binaries; ship them via short-lived server-issued credentials instead.

**Why:** Anyone can decompile the shipped IPA/APK and extract embedded secrets, since client code is fully inspectable.

**Detect:** run `strings`/mobSF scan on the binary; grep repo for `apiKey =`, `secret`, `BEGIN PRIVATE KEY`, hardcoded `AIza`/`sk-` prefixes in source and Info.plist/assets.

**References:** OWASP MASVS-STORAGE-2, CWE-798, CWE-321, MAS Testing Guide Reverse Engineering

---

**Part of:** [mobile](../categories/mobile.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [mobile](../domains/mobile.md) · [SKILL.md](../SKILL.md)
