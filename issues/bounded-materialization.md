---
categories: [correctness-pitfalls, scaling-capacity]
domains: [backend, reliability]
---

# Bounded Materialization of Results

**MUST NOT** materialize an unbounded result into memory as one array, list, or string when the consumer can read it incrementally, and **MUST** cap every in-memory collection it does build with a limit tied to a real bound.

**Why:** A query with no `LIMIT`, a full-table read, or a whole file loaded into a string holds the entire result in memory at once, so the process footprint grows with the data rather than with traffic — it passes every test on a small dataset and OOM-kills in production the week the table crosses the size that was nobody's launch criterion, while the same work read in pages would have stayed flat.

**Detect:** `.fetchall(`, `.toList(`, `read(`, `readFile`/`readFileSync`, `json.load` on an unbounded file or response, `SELECT *` with no `LIMIT` feeding an in-memory collection; a list appended inside a loop with no size cap; a report or export built entirely in memory before serialization. Check for a cursor/iterator/streaming API on the same path and for a hard `LIMIT`/`max_results` on collection size.

**References:** CWE-400, CWE-770, CWE-789
