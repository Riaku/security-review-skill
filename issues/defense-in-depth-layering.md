# Defense-in-Depth Layering

**SHOULD** protect each asset with multiple independent control layers (network, app, data, runtime) so no single failure exposes it; layers must be independent, not correlated.

**Why:** Every control fails eventually — a bypassed WAF, a missed CVE, a phished credential. Correlated layers (all bypassed by the same trick) are one layer wearing a trench coat.

**Detect:** map each crown-jewel asset to its control stack; flag assets protected by a single layer; check layer independence (e.g. WAF + app validation + DB authz vs WAF-only; secrets not readable by the same principal that reaches the app).

**References:** OWASP Secure Product Design Cheat Sheet, NIST SP 800-53 defense-in-depth, CISA Secure by Design
