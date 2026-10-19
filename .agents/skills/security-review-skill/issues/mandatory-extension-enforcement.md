---
categories: [api-design]
domains: [backend]
---

# Mandatory Extension Enforcement

**MUST** fail the connection when a peer does not acknowledge a security-critical protocol extension, even where the feature it protects is unused locally.

**Why:** An extension that is negotiated but not required lets a downgrade happen quietly, which is how renegotiation and triple handshake attacks survived patches.

**Detect:** testssl.sh --severity HIGH against the endpoint; it reports Secure Renegotiation and Extended Master Secret support.

**References:** RFC 9325 §3.5, https://www.rfc-editor.org/rfc/rfc9325.html, RFC 7627 (extended master secret), CVE-2009-3555
