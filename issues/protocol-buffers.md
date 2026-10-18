---
categories: [api-design]
domains: [backend]
---

# Protocol Buffers

**MUST NOT** reuse or repurpose reserved field numbers in .proto definitions; mark removed fields `reserved` to prevent wire-level confusion.

**Why:** A redeployed service decoding an old message under a reassigned field silently misinterprets data, corrupting records across versions.

**Detect:** .proto diffs removing fields without adding `reserved N;`; missing `reserved` blocks in evolved messages.

**References:** CWE-707, protobuf docs field reserved, Buf breaking-change rules

---

**Part of:** [api-design](../categories/api-design.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
