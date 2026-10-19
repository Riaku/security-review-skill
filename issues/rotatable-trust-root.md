---
categories: [supply-chain]
domains: [infrastructure]
---

# Rotatable Trust Root

**MUST** distribute update and verification roots through a versioned, rotatable metadata mechanism instead of a key baked into the client.

**Why:** A root key compiled into firmware or a client cannot be replaced when it leaks or expires, stranding every deployed device on a dead trust anchor.

**Detect:** Embedded PEM blocks or single pinned public keys in update-client code (`BEGIN PUBLIC KEY` in the updater) with no fetched, versioned root metadata.

**References:** Sigstore Fulcio, https://github.com/sigstore/fulcio, The Update Framework (TUF) specification
