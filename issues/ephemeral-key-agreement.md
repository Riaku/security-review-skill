---
categories: [secrets-crypto]
domains: [infrastructure]
---

# Ephemeral Key Agreement

**MUST** use ephemeral per-connection key agreement so later compromise of a long-term key cannot decrypt recorded traffic.

**Why:** Static key exchange makes every recorded session decryptable the day the private key leaks. Forward secrecy bounds that loss to sessions in flight.

**Detect:** Static ECDH, `TLS_RSA_*` suites, or a shared symmetric key reused across sessions.

**References:** BSI TR-02102-2, https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf
