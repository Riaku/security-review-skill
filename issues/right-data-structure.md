---
categories: [correctness-pitfalls, scaling-capacity]
domains: [backend, reliability]
---

# Keyed Lookup Instead of Repeated Scans

**MUST NOT** resolve each element of a collection by scanning another collection — `in` / `indexOf` / `find` / a nested filter — when a set, map, or index keyed on the lookup field can answer the same question in constant time.

**Why:** Every element of one collection checked against every element of the other is a product, not a sum: a 10k × 10k pairing is 100M comparisons that a single pass building a keyed structure answers with 10k lookups, and the cost grows with data volume while the request rate stays flat — so it degrades in production as tables fill, not under load, and shows up as unexplained CPU rather than a failing test.

**Detect:** `x in list`, `.includes(`, `.indexOf(`, `.find(`, `Array.prototype.some(` inside a loop over another collection; `filter` nested in `map`; a join implemented in application code by matching keys across two result sets; repeated `sorted(` per iteration. Then check the scanned collection's size: a handful of constants is fine, anything that grows with tenants, rows, or files is the finding.

**References:** CWE-407, CWE-1176
