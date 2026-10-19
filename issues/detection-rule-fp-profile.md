---
categories: [observability]
domains: [infrastructure]
---

# Detection Rule FP Profile

**SHOULD** record each detection rule's maturity status and its known false-positive profile inside the rule, and review both whenever the rule changes.

**Why:** An undeclared false-positive rate is discovered by analysts at 3am, and the rule is then disabled or ignored wholesale.

**Detect:** grep for falsepositives: and status: fields in every rule file, and compare declared profile against alert volume per rule

**References:** Sigma rule schema, https://github.com/SigmaHQ/sigma
