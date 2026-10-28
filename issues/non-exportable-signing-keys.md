---
categories: [secrets-crypto]
domains: [governance, infrastructure]
---

# Non-Exportable Signing Keys

**MUST** keep code-signing, SSH, and package-publish credentials on hardware tokens so private key material cannot be exported and each use requires physical presence.

**Why:** A key file on disk, even passphrase-protected, is copyable by malware and one cracked passphrase away from full impersonation.

**Detect:** ssh-add -l lists only hardware-backed keys; any file-based signing key is a finding

**References:** Fystack Developer Security Handbook, https://github.com/fystack/developer-security-handbook
