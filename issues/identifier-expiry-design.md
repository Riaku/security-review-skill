---
categories: [compliance-privacy]
domains: [data]
---

# Identifier Expiry Design

**SHOULD** give every identifier an expiry, replacement and deletion path instead of assuming it is permanent.

**Why:** Permanent identifiers accumulate into tracking keys and cannot be erased when a user leaves. A schema with no expiry makes retention obligations impossible to honour.

**Detect:** Identifier columns and cookies lacking `expires_at`, `ttl` or a rotate/delete path in the schema and cookie settings.

**References:** RFC 6973 Privacy Considerations, https://www.rfc-editor.org/rfc/rfc6973.txt
