---
categories: [iot-embedded]
domains: [iot-embedded]
---

# Shared Bus Node Trust

**MUST** rate-limit and authenticate each node's contribution to a shared bus or channel, so one subverted node cannot consume the medium for all.

**Why:** A bus that trusts every node lets one reprogrammed device transmit continuously and make the whole channel, and everything depending on it, unusable.

**Detect:** judgment: the bus protocol — per-node transmit quotas, bus-off handling, and message authentication

**References:** Anderson, Security Engineering 3rd ed., ch.25, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch25.pdf
