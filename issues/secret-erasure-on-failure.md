---
categories: [secrets-crypto]
domains: [backend]
---

# Secret Erasure on Failure

**MUST** keep secrets in dedicated buffers and wipe them on every exit path, including error and exception paths.

**Why:** Secrets left in memory survive in core dumps, swap and crash reports. Error paths are the ones nobody writes the cleanup for.

**Detect:** Key material held in ordinary strings or heap objects; missing `explicit_bzero`/`zeroize`/`memset_s` on the failure branch of a verification routine.

**References:** ANSSI secure C programming rules, https://messervices.cyber.gouv.fr/guides/regles-de-programmation-pour-le-developpement-securise-de-logiciels-en-langage-c
