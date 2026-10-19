---
categories: [compliance-privacy]
domains: [mobile]
---

# Resettable Identifiers Only

**MUST** link user data to a resettable, app-scoped identifier, never to a hardware identifier the user cannot reset or revoke.

**Why:** A hardware identifier is a permanent cross-app tracking key that survives uninstall and cannot be cleared by the person it describes.

**Detect:** grep getDeviceId, IMEI, getMacAddress, identifierForVendor, ANDROID_ID used as an analytics or storage key

**References:** Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en_20250827.pdf
