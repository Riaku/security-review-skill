---
categories: [authentication]
domains: [backend]
---

# No Human Verification Controls

**MUST NOT** rely on users comparing codes, recognizing voices, or noticing warnings as a security control; the check must be cryptographic.

**Why:** Synthetic voice and video defeat channel authentication by human senses, and optional security prompts are ignored at scale.

**Detect:** in the auth or pairing flow, identify whether the only man-in-the-middle defence is a value the user is asked to compare.

**References:** RFC 8826 §4.3.2.2, https://www.rfc-editor.org/rfc/rfc8826.html
