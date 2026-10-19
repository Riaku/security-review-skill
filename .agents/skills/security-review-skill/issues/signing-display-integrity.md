---
categories: [authentication]
domains: [backend]
---

# Trusted Display for Signing

**MUST** include the display path that shows a user what they approve inside the trusted boundary, or the signature attests only to what a compromised host chose to show.

**Why:** Certifying the signing device while the adjacent screen is attacker-controlled produces valid signatures on transactions the user never saw.

**Detect:** judgment: the approval flow — which machine renders the transaction details, and whether it is inside the evaluated boundary

**References:** Anderson, Security Engineering 1st ed., ch.23, https://www.cl.cam.ac.uk/~rja14/book.html
