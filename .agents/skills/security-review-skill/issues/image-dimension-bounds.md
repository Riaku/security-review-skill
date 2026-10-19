---
categories: [web-api-security]
domains: [backend]
---

# Image Dimension Bounds

**MUST** bound decoded pixel dimensions and total pixel count before decoding an image, not just the file's byte size.

**Why:** A small compressed file can decode to gigapixels, so a size limit on the wire passes an image that exhausts memory in the decoder.

**Detect:** grep image decode paths (`Image.open`, `image.Decode`, `sharp(`) for a pixel or dimension limit and for `MAX_IMAGE_PIXELS`-style guards.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md, CWE-400
