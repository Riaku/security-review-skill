---
categories: [compliance-privacy]
domains: [mobile]
---

# Layered Consent

**SHOULD** obtain separate just-in-time consent for each sensitive data class transmitted, instead of relying on one blanket acceptance at install or first launch.

**Why:** Users cannot evaluate future data uses at install time, so a single upfront acceptance cannot authorize categories they never saw and cannot later withdraw.

**Detect:** consent screens and consent records: one record per data purpose with its own timestamp, not one global accepted flag

**References:** Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en_20250827.pdf
