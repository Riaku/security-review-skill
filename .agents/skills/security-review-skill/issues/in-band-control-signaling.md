---
categories: [api-design]
domains: [backend]
---

# Out-of-Band Control Signals

**MUST** carry authentication and routing control signals out-of-band, or authenticate them independently, when payload data shares the same channel.

**Why:** Anyone able to inject into the shared channel can forge control semantics, and the receiver cannot distinguish a forgery from a legitimate signal.

**Detect:** judgment: the protocol framing — whether control fields sit in the same stream as user data and how they are authenticated

**References:** Anderson, Security Engineering 3rd ed., ch.22, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch22.pdf
