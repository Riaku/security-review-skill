---
categories: [security-practices]
domains: [backend]
---

# Proportionate QA Tiering

**SHOULD** match review/QA rigor to the risk tier of what's being changed: critical-path and high-impact components get deep review, dual verification, and testing; throwaway work gets proportionate scrutiny.

**Why:** Uniform maximum rigor exhausts reviewers into rubber-stamping; uniform minimum rigor misses disasters. Both failure modes come from never assigning a risk tier in the first place.

**Detect:** judgment on whether a documented risk tier / QA plan exists and matches the component's actual criticality (user impact, data sensitivity, money movement).

**References:** OWASP SAMM, risk-based testing practice
