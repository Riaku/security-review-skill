---
categories: [secrets-crypto]
domains: [backend]
---

# Key Lifecycle Recovery

**MUST** define backup, recovery, rotation, and destruction for every long-lived key, protecting the recovery path as strongly as the key.

**Why:** A weak recovery path is a backdoor, and no recovery path turns one lost key into permanent data loss.

**Detect:** key-store inspection (`aws kms get-key-rotation-status`, key policy, deletion window) — rotation enabled, escrow documented, and destruction requiring the same approvers as creation.

**References:** OWASP Key Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html
