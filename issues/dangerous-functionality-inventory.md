---
categories: [security-practices]
domains: [backend]
---

# Dangerous Functionality Inventory

**MUST** maintain a reviewed inventory of dangerous functionality - untrusted deserialization, raw binary parsing, dynamic code execution, direct memory access - and isolate it.

**Why:** These operations are code execution by design, so the only durable control is knowing where they are and keeping them few, sandboxed and separately reviewed.

**Detect:** `eval(`, `exec(`, `pickle.loads`, `yaml.load(`, `mmap(`, `ctypes.` and FFI entry points, cross-checked against the dangerous-functionality inventory.

**References:** OWASP ASVS V15 Secure Coding and Architecture, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md
