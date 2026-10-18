# mobile — full checklist (5 items)

Mobile client security.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Mobile Certificate Pinning

**MUST** pin the server's certificate or public key (SPKI hash) for API traffic, with a documented rotation plan and backup pins.

**Why:** Without pinning, a user-installed root CA or compromised CA lets attackers intercept and modify all app traffic via MITM proxies.

**Detect:** grep for `certificatePinner`, `TrustKit`, `ServerTrustPolicy`, `network_security_config.xml` with `pin-set`; absence in Retrofit/OkHttp/URLSession configs.

**References:** OWASP MASVS-NETWORK-4, CWE-295, OWASP MAS Testing Guide Network Interception

# Mobile Secure Storage (Keychain/Keystore)

**MUST NOT** store tokens, credentials, or PII in SharedPreferences, UserDefaults, plaintext files, or web localStorage; use Keychain (iOS) or EncryptedSharedPreferences backed by the Keystore (Android).

**Why:** Rooted or backed-up devices expose world-readable storage, handing attackers live session tokens and personal data.

**Detect:** grep `SharedPreferences`, `UserDefaults`, `localStorage` near `token`, `password`, `api_key`; check for `kSecAttrAccessible` / `EncryptedSharedPreferences` usage.

**References:** OWASP MASVS-STORAGE-1, CWE-922, CWE-312, NIST SP 800-63B

# Deep Link / Universal Link Validation

**SHOULD** validate scheme, host, and parameters of every incoming deep link server-side, treating link-supplied identifiers as untrusted input.

**Why:** Unvalidated links enable phishing into authenticated flows, IDOR jumps to other users' resources, and intent hijacking on Android.

**Detect:** grep `AppDelegate continueUserActivity`, `onNewIntent`, `intent-filter`, `universalLinksOnly`; review handlers for missing authz checks on link parameters.

**References:** OWASP MASVS-PLATFORM-6, CWE-20, CWE-639, OWASP MAS Testing Guide Client-Side Attack Surface

# Hardcoded API keys and secrets in mobile app binaries

**MUST NOT** embed API keys, tokens, or symmetric secrets in app source, assets, or compiled binaries; ship them via short-lived server-issued credentials instead.

**Why:** Anyone can decompile the shipped IPA/APK and extract embedded secrets, since client code is fully inspectable.

**Detect:** run `strings`/mobSF scan on the binary; grep repo for `apiKey =`, `secret`, `BEGIN PRIVATE KEY`, hardcoded `AIza`/`sk-` prefixes in source and Info.plist/assets.

**References:** OWASP MASVS-STORAGE-2, CWE-798, CWE-321, MAS Testing Guide Reverse Engineering

# Mobile Reverse-Engineering & Tamper Protection

**SHOULD** detect rooted/jailbroken devices, debuggers, and repackaged builds, and gate high-risk features accordingly rather than trusting the client.

**Why:** Tampered clients bypass in-app restrictions, enabling fraud, license piracy, and automated abuse that server-side-only checks miss if nothing reports integrity.

**Detect:** grep `SafetyNet`/`Play Integrity`, `jailbreak`/`rootbeer`, `isDebuggerConnected`, `ptrace`, `frida`; verify Play Integrity / App Attest server-side validation exists.

**References:** OWASP MASVS-RESILIENCE-1..4, CWE-919, MAS Testing Guide Tampering and Reverse Engineering

