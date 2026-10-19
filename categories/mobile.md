# mobile

Mobile client security.

## What this category covers

This category covers security problems specific to shipped mobile clients, where the binary is fully inspectable and the network is hostile. Items span network trust and certificate pinning, validation of deep links and universal links, device-integrity and tamper detection, on-device secure storage, push notification payloads and token binding, and secrets left in the shipped binary. A reviewer should expect to see iOS and Android client code, network configuration, push registration handlers, and keychain or keystore usage.

- Network trust — certificate or public-key pinning for API traffic, with backup pins and a rotation plan.
- Inbound link handling — validating scheme, host, and parameters of deep links and universal links, treating link-supplied identifiers as untrusted and re-checking authorization server-side.
- Client integrity — detecting rooted or jailbroken devices, debuggers, and repackaged builds, and gating high-risk features on server-side attestation.
- On-device storage — tokens, credentials, and PII in Keychain or Keystore-backed storage rather than SharedPreferences, UserDefaults, plaintext files, or web storage.
- Push handling — payloads free of secrets and full PII, and device tokens bound to the authenticated user and device.
- Shipped-binary secrets — API keys and symmetric secrets kept out of source, assets, and compiled artifacts.

## What it does not cover

- [web-client-security](../categories/web-client-security.md) — browser-side concerns such as CSP, CSRF, cookie flags, and postMessage origin checks belong there; app-binary and OS-integration risks are scoped here.
- [authentication](../categories/authentication.md) — token issuance, refresh, revocation, and session invalidation belong there; carrying those tokens safely on a mobile client is scoped here.
- [secrets-crypto](../categories/secrets-crypto.md) — secret storage, rotation, and crypto-primitive choice belong there; extracting a secret from a decompiled app binary is scoped here.
- [web-api-security](../categories/web-api-security.md) — server-side input validation and authorization for API endpoints belong there; validating the client's incoming deep link is scoped here.

## What a finding here looks like

- API traffic with no certificate pinning, so a user-installed root CA can intercept every app request.
- A deep-link handler that reads a user id from the link and fetches that user's data without a server-side authorization re-check.
- Session tokens written to SharedPreferences, UserDefaults, or `localStorage` instead of Keychain or Keystore.
- Push payloads carrying a magic-login link, one-time code, or full card number that render on the lock screen.
- A hardcoded API key or `BEGIN PRIVATE KEY` in app source, assets, or the compiled IPA or APK.
