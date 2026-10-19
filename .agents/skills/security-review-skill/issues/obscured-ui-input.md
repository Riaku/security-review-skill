---
categories: [mobile]
domains: [mobile]
---

# Input Under Obscuring Overlays

**MUST** reject touch and click events that arrive while the view is obscured by another application's overlay, so a co-located app cannot harvest consent or confirmations.

**Why:** An overlay drawn over a control lets a malicious app capture the tap and redirect it to a destructive or consent action the user never intended.

**Detect:** grep for setFilterTouchesWhenObscured / filterTouchesWhenObscured on sensitive views

**References:** Google android-security-lints, https://github.com/google/android-security-lints
