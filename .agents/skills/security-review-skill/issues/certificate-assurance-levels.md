---
categories: [cloud-network]
domains: [infrastructure]
---

# Certificate Assurance Levels

**SHOULD** weigh a certificate for the validation actually performed: domain validation proves control of a name, not the identity of the organization behind it.

**Why:** Mapping any CA-issued certificate to organizational trust overstates what was checked and is defeated by a single domain takeover.

**Detect:** openssl x509 -in cert.pem -noout -text  and read the policy OIDs and validation type before treating the issuer as identity evidence

**References:** Ross Anderson, Security Engineering (3rd ed.), https://www.cl.cam.ac.uk/~rja14/book.html
