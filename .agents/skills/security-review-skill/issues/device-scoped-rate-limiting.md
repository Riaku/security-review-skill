---
categories: [authentication]
domains: [backend]
---

# Lockout-Resistant Throttling

**MUST NOT** let failed-login throttling disable a known account; rate-limit per credential and source so an attacker cannot lock the owner out.

**Why:** Account-only lockout hands an attacker a denial-of-service switch against any known user; throttling per credential and source slows the attack without disabling the owner.

**Detect:** Login and OTP handlers that lock or disable the account after N failures, keyed on `username`/`email` alone.

**References:** Application Security Handbook: Trusted Devices, https://github.com/0xn3va/application-security-handbook/blob/main/Web%20Application/Concept%20of%20Trusted%20Devices/README.md
