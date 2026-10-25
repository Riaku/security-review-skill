---
categories: [correctness-pitfalls]
domains: [backend]
---

# Safe Temporary Files & Atomic Writes

**MUST** create temporary files exclusively (`O_CREAT|O_EXCL` or an equivalent atomic-create API) in a directory only the process can write, and **MUST** publish them by renaming into place instead of writing the destination in place.

**Why:** A predictable name in a world-writable directory can be pre-created as a symlink or swapped between the check and the use, and an in-place write leaves readers a truncated or half-rewritten file when the process dies mid-write — a state that survives the restart and corrupts the data the file was meant to protect.

**Detect:** `tempnam`, `tmpnam`, `mktemp` without a template, a hardcoded `/tmp/<name>`, `open('/tmp/…', 'w')` instead of `tempfile.mkstemp`/`NamedTemporaryFile`; a write to the final path with no `os.replace`/`File.Move`/`rename(2)` staging step; confirm the rename target is on the same filesystem, the temp file is unlinked on failure, and the directory is not group- or world-writable.

**References:** CWE-377, CWE-367
