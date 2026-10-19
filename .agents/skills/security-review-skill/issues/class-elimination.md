---
categories: [security-practices]
domains: [backend]
---

# Eliminate Vulnerability Classes

**SHOULD** prefer a mechanism that eliminates a whole defect class over repeated point fixes when findings concentrate in that class.

**Why:** Removing the class turns many independent bugs into one solved problem, while point fixes leave the next instance to be discovered in production.

**Detect:** judgment: the defect trend by class across recent releases — whether one class keeps returning after repeated fixes

**References:** Anderson, Security Engineering 1st ed., ch.23, https://www.cl.cam.ac.uk/~rja14/book.html
