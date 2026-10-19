---
categories: [mobile]
domains: [mobile]
---

# IPC Entry Point Validation

**MUST** treat every inter-process or inter-app entry point as attacker-reachable and validate its payload, even when only first-party apps call it.

**Why:** Any app on the device can usually send the same intent, message or bound-service call. 'Only our apps use this' is an assumption the platform does not enforce.

**Detect:** `android:exported="true"` components, custom URL schemes, and `onReceive`/`onStartCommand` handlers parsing extras without validation.

**References:** JSSEC Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en.pdf
