---
categories: [secrets-crypto]
domains: [backend]
---

# Stream Message Authentication

**MUST** authenticate and integrity-check each message on a continuous media or telemetry stream, not only the session handshake that opened it.

**Why:** Without per-message authentication an attacker on the path injects content silently, turning eavesdropping into media or command insertion.

**Detect:** grep media/signalling config for SRTP protection disabled or optional (`srtp-policy: optional`, `use_srtp` unset, DTLS-SRTP off) and for RTP sources accepted without an auth tag check.

**References:** OWASP ASVS v5.0 V17.2.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x26-V17-WebRTC.md, RFC 3711 (SRTP)
