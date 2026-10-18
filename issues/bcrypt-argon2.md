---
categories: [secrets-crypto]
domains: [backend]
---

# bcrypt & Argon2

**SHOULD** use Argon2id (preferred) or bcrypt with cost ≥12 for password hashing; MD5, SHA-1, and bare SHA-256 are unacceptable for credentials.

**Why:** Fast general-purpose hashes let GPUs test billions of guesses per second, cracking weak passwords in hours after a database breach.

**Detect:** `hashlib.md5`, `sha1(` on password fields, `bcrypt.gensalt(rounds=` below 12, absence of `argon2` in dependencies.

**References:** OWASP Password Storage Cheat Sheet, CWE-916, NIST SP 800-63B §5.1.1.2
