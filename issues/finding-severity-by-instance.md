---
categories: [security-practices]
domains: [governance]
---

# Severity from Instance Attributes

**MUST** rate a finding by the concrete instance — data reachable, identifier predictability, read versus write — rather than by vulnerability class alone.

**Why:** One class spans trivial to critical depending on what the specific object exposes, so class-level severity both inflates reports and buries real criticals.

**Detect:** judgment: the finding record — whether severity cites reachable data and identifier entropy

**References:** Bugcrowd Vulnerability Rating Taxonomy, https://github.com/bugcrowd/vulnerability-rating-taxonomy
