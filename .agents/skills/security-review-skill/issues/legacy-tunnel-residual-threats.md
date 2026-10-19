---
categories: [cloud-network]
domains: [infrastructure]
---

# Tunnel Residual Threats

**MUST** document which threats a tunnel removes and which remain when wrapping an unauthenticated legacy protocol, including command injection from inside either endpoint network.

**Why:** The tunnel protects transit only; the legacy protocol still accepts unauthenticated commands from any host on the far side, which is where the practical attack lands.

**Detect:** judgment — read the design or threat model for the tunneled protocol and check it names the residual in-network command-injection path and its control.

**References:** NCSC cloud suitability for OT: tunneling legacy protocols, https://www.ncsc.gov.uk/collection/operational-technology
