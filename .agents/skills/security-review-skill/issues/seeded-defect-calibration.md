---
categories: [testing-strategy]
domains: [backend]
---

# Seeded-Defect Review Calibration

**SHOULD** seed a known number of defects into a review round and use the detection ratio to estimate how many unknown defects remain.

**Why:** A review that finds nothing is indistinguishable from a review that missed everything unless its sensitivity has been measured.

**Detect:** judgment: the last calibration exercise's found-versus-seeded table and the residual estimate it implies

**References:** Anderson, Security Engineering 1st ed., ch.23, https://www.cl.cam.ac.uk/~rja14/book.html
