# mobile — full checklist (19 items)

Mobile client security.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/mobile.md](../categories/mobile.md) · Index: [SKILL.md](../SKILL.md)

# Biometric Key Binding

**MUST** bind biometric verification to a keystore key that requires a fresh biometric match and is invalidated when enrollment changes.

**Why:** A biometric check that only returns a boolean leaves the underlying secret valid after fingerprints are added or the device is compromised.

**Detect:** grep for setUserAuthenticationRequired and setInvalidatedByBiometricEnrollment (Android) or kSecAccessControlBiometryCurrentSet (iOS) on key generation

**References:** OWASP MASTG best practices, https://github.com/OWASP/mastg/tree/master/best-practices

# Mobile Certificate Pinning

**MUST** pin the server's certificate or public key (SPKI hash) for API traffic, with a documented rotation plan and backup pins.

**Why:** Without pinning, a user-installed root CA or compromised CA lets attackers intercept and modify all app traffic via MITM proxies.

**Detect:** grep for `certificatePinner`, `TrustKit`, `ServerTrustPolicy`, `network_security_config.xml` with `pin-set`; absence in Retrofit/OkHttp/URLSession configs.

**References:** OWASP MASVS-NETWORK-1, CWE-295, OWASP MAS Testing Guide Network Interception

# Deep Link / Universal Link Validation

**SHOULD** validate scheme, host, and parameters of every incoming deep link on the client, treating link-supplied identifiers as untrusted input, and re-check authorization server-side before acting on them.

**Why:** Unvalidated links enable phishing into authenticated flows, IDOR jumps to other users' resources, and intent hijacking on Android.

**Detect:** grep `AppDelegate continueUserActivity`, `onNewIntent`, `intent-filter`, `universalLinksOnly`; review handlers for missing authz checks on link parameters.

**References:** OWASP MASVS-PLATFORM-1, CWE-20, CWE-639, OWASP MAS Testing Guide Client-Side Attack Surface

# Immutable Deferred Actions

**MUST** make deferred actions handed to the platform immutable and explicitly targeted, with a frozen payload and a fixed component.

**Why:** A mutable or implicitly routed pending action can be intercepted, redirected, or have its extras rewritten before the system delivers it.

**Detect:** grep for PendingIntent built without FLAG_IMMUTABLE, or with an implicit intent instead of an explicit component

**References:** OWASP MASTG best practices, https://github.com/OWASP/mastg/tree/master/best-practices

# Interpreter Features by Provenance

**MUST** enable script interpreters in embedded webviews only for content the app fully controls, never for remote or user content.

**Why:** A JavaScript bridge in a webview exposes native capabilities to whatever page loads. One redirect or injected frame turns the bridge into remote code execution.

**Detect:** `setJavaScriptEnabled(true)`, `addJavascriptInterface(` or `setAllowFileAccess(true)` next to a load of a remote URL.

**References:** JSSEC Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en.pdf

# IPC Entry Point Validation

**MUST** treat every inter-process or inter-app entry point as attacker-reachable and validate its payload, even when only first-party apps call it.

**Why:** Any app on the device can usually send the same intent, message or bound-service call. 'Only our apps use this' is an assumption the platform does not enforce.

**Detect:** `android:exported="true"` components, custom URL schemes, and `onReceive`/`onStartCommand` handlers parsing extras without validation.

**References:** JSSEC Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en.pdf

# Private IPC Entry Points

**MUST** keep every inter-process entry point private by default, exporting one only when a named external consumer requires it and its payload is authorized.

**Why:** An accidentally exported activity, service, receiver, or provider is a permanent public API that any installed application can invoke with attacker-chosen input.

**Detect:** grep 'android:exported="true"' in AndroidManifest.xml for activities, services, receivers and providers; confirm each has an intent-filter and a caller check

**References:** Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en_20250827.pdf

# Keyboard Caching of Sensitive Input

**MUST** disable predictive text, autocorrect, and keyboard learning for fields that accept secrets or sensitive personal data.

**Why:** System keyboards retain and sync typed text, so a value typed once can persist in the user's dictionary and cloud backup.

**Detect:** grep for textNoSuggestions or textVisiblePassword input flags and autocorrect=false on sensitive fields

**References:** OWASP MASTG best practices, https://github.com/OWASP/mastg/tree/master/best-practices

# Legacy Platform Security Defaults

**MUST** set security-relevant platform defaults explicitly when supporting older runtime versions, rather than inheriting the weaker defaults those versions shipped with.

**Why:** A default that is safe on the current platform silently permits cleartext traffic, user-added CAs, or broad storage access on older versions still in the support matrix.

**Detect:** grep the manifest and build config for cleartext traffic, trust-anchor, and external-storage settings against minSdk

**References:** Google android-security-lints, https://github.com/google/android-security-lints

# Minimum Client Version

**SHOULD** enforce a minimum supported client version server-side and block older clients from sensitive operations instead of trusting them to update.

**Why:** A shipped client that cannot be forced forward is a permanent foothold for every vulnerability fixed after its release.

**Detect:** grep request middleware for a minimum-version or X-Client-Version comparison that returns an upgrade-required status

**References:** OWASP MASVS v2 (Resilience, update enforcement)

# Mobile Reverse-Engineering & Tamper Protection

**SHOULD** detect rooted/jailbroken devices, debuggers, and repackaged builds, and gate high-risk features accordingly rather than trusting the client.

**Why:** Tampered clients bypass in-app restrictions, enabling fraud, license piracy, and automated abuse that server-side-only checks miss if nothing reports integrity.

**Detect:** grep `SafetyNet`/`Play Integrity`, `jailbreak`/`rootbeer`, `isDebuggerConnected`, `ptrace`, `frida`; verify Play Integrity / App Attest server-side validation exists.

**References:** OWASP MASVS-RESILIENCE-1..4, MAS Testing Guide Tampering and Reverse Engineering

# Mobile Secure Storage (Keychain/Keystore)

**MUST NOT** store tokens, credentials, or PII in SharedPreferences, UserDefaults, plaintext files, or web localStorage; use Keychain (iOS) or EncryptedSharedPreferences backed by the Keystore (Android).

**Why:** Rooted or backed-up devices expose world-readable storage, handing attackers live session tokens and personal data.

**Detect:** grep `SharedPreferences`, `UserDefaults`, `localStorage` near `token`, `password`, `api_key`; check for `kSecAttrAccessible` / `EncryptedSharedPreferences` usage.

**References:** OWASP MASVS-STORAGE-1, CWE-922, CWE-312, NIST SP 800-63B

# Header Controls Miss Non-Browsers

**MUST** enforce security controls for non-browser clients in client or server logic, never by relying on response headers those clients ignore.

**Why:** Mobile, SDK, and embedded HTTP clients do not implement HSTS, CSP, or frame protections, so a header-only defense does nothing for the traffic that carries tokens.

**Detect:** judgment — inspect the mobile or SDK HTTP layer for certificate validation, redirect refusal, and cookie handling implemented in code rather than assumed from server headers.

**References:** Security header support in HTTP clients, https://arxiv.org/abs/2111.03601

# Input Under Obscuring Overlays

**MUST** reject touch and click events that arrive while the view is obscured by another application's overlay, so a co-located app cannot harvest consent or confirmations.

**Why:** An overlay drawn over a control lets a malicious app capture the tap and redirect it to a destructive or consent action the user never intended.

**Detect:** grep for setFilterTouchesWhenObscured / filterTouchesWhenObscured on sensitive views

**References:** Google android-security-lints, https://github.com/google/android-security-lints

# Peer App Signing Identity

**MUST** identify peer applications by signing-certificate digest, never by package name or a self-declared identifier alone.

**Why:** Package names are global and can be squatted, and any app can claim a caller name. Only the signing certificate proves who is on the other end.

**Detect:** `getPackageInfo(` calls using `GET_SIGNATURES`/`checkSignatures`, and IPC servers authorizing callers by `packageName` only.

**References:** JSSEC Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en.pdf

# Push-Payload Sensitivity

**MUST NOT** put secrets, tokens, full PII, or account-identifying detail in push notification payloads (they are stored/transmitted by third-party OS infrastructure and shown on lock screens).

**Why:** Push bodies pass through Apple/Google infrastructure and render on unlocked screens; a notification with a magic-login link or full card number is a shoulder-surf and relay attack.

**Detect:** grep push payload construction for tokens, codes, amounts, addresses; verify payloads are content-neutral ("You have a new message — open the app") with sensitive detail fetched in-app.

**References:** OWASP MASVS-STORAGE, APNs payload security guidance, lock-screen disclosure studies

# Push-Token Binding & Rotation

**MUST** bind APNs/FCM device tokens to the authenticated user+device and invalidate on logout/account change; never accept a token from an unauthenticated registration.

**Why:** Unbound push tokens let an attacker register their device against someone's account (token swap) and receive their notifications — 2FA codes, account alerts, private messages.

**Detect:** grep push registration endpoints for auth requirement and user+device binding; check logout path unregisters tokens; flag token storage without account association or per-install rotation.

**References:** OWASP MASVS-AUTH, APNs/FCM security guidance, push-token hijacking CVEs

# Screen Capture of Sensitive Views

**MUST** opt sensitive screens out of OS screenshot, screen-recording, and recents-thumbnail capture rather than assuming users will not capture them.

**Why:** The platform renders whatever the app draws, so a view showing tokens, balances, or personal data persists in the recents store and in any recorder.

**Detect:** grep for FLAG_SECURE on sensitive activities and the secure-capture equivalent on token and PII screens

**References:** OWASP MASTG best practices, https://github.com/OWASP/mastg/tree/master/best-practices

# Hardcoded API keys and secrets in mobile app binaries

**MUST NOT** embed API keys, tokens, or symmetric secrets in app source, assets, or compiled binaries; ship them via short-lived server-issued credentials instead.

**Why:** Anyone can decompile the shipped IPA/APK and extract embedded secrets, since client code is fully inspectable.

**Detect:** run `strings`/mobSF scan on the binary; grep repo for `apiKey =`, `secret`, `BEGIN PRIVATE KEY`, hardcoded `AIza`/`sk-` prefixes in source and Info.plist/assets.

**References:** OWASP MASVS-STORAGE-2, CWE-798, CWE-321, MAS Testing Guide Reverse Engineering

