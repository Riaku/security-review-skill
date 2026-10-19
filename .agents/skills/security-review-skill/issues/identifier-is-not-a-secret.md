---
categories: [authentication]
domains: [iot-embedded]
---

# Identifier Is Not a Secret

**MUST NOT** authenticate with a serial number, MAC address, or other identifier that is printed on the device or shared with third parties.

**Why:** Identifiers are visible to dealers, registries, and anyone on the local link, so they leak by design and cannot be rotated after exposure.

**Detect:** grep serial, imei, mac_address values used in password comparison, token derivation, or as HMAC key material

**References:** Ross Anderson, Security Engineering (3rd ed.), https://www.cl.cam.ac.uk/~rja14/book.html
