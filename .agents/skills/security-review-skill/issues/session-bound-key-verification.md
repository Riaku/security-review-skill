---
categories: [authentication]
domains: [backend]
---

# Session-Bound Key Verification

**MUST** bind a presented certificate or key to the session it was negotiated for, and terminate the channel when the binding does not match.

**Why:** A valid certificate that is not tied to this session admits any holder of any valid certificate as a man in the middle.

**Detect:** grep for fingerprint or channel-binding comparison in the handshake (`sdp fingerprint`, `tls-server-end-point`, `ExportKeyingMaterial`); its absence means the key is trusted on chain validity alone.

**References:** OWASP ASVS v5.0 V17.2.8, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x26-V17-WebRTC.md, RFC 5705 (keying material exporters), CWE-295
