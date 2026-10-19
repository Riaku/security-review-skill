---
categories: [security-practices]
domains: [governance]
---

# Structured Security Requirements

**MUST** track each security requirement as a structured record linked to its implementation and verification, not as prose in a document.

**Why:** Prose requirements cannot be queried, traced to code, or counted at audit time, so they rot silently. Structured records keep every requirement visible until it is verified.

**Detect:** Inspect the requirements store: each requirement has an ID, an owner, a link to implementing code and a verification artifact.

**References:** SAFECode Fundamental Practices for Secure Software Development v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf
