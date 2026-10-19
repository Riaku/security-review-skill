---
categories: [documentation-quality]
domains: [backend]
---

# Mechanism Assumptions and Non-Goals

**MUST** state, in the mechanism's own documentation, the assumptions it depends on and the attacks it does not stop.

**Why:** A mechanism trusted outside its assumptions is worse than none, because it displaces the control that would have covered the gap. Non-goals are what prevent that substitution.

**Detect:** Security module README or docstrings lacking a non-goals or 'does not protect against' section.

**References:** RFC 3552, https://www.rfc-editor.org/rfc/rfc3552.txt
