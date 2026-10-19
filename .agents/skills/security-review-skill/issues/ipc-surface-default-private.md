---
categories: [mobile]
domains: [mobile]
---

# Private IPC Entry Points

**MUST** keep every inter-process entry point private by default, exporting one only when a named external consumer requires it and its payload is authorized.

**Why:** An accidentally exported activity, service, receiver, or provider is a permanent public API that any installed application can invoke with attacker-chosen input.

**Detect:** grep 'android:exported="true"' in AndroidManifest.xml for activities, services, receivers and providers; confirm each has an intent-filter and a caller check

**References:** Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en_20250827.pdf
