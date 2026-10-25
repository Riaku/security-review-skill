---
categories: [correctness-pitfalls, scaling-capacity]
domains: [backend, reliability]
---

# Bounded Directory Traversal

**MUST** bound every recursive directory walk, glob, or archive listing by depth and entry count, and **MUST NOT** follow symbolic links out of the traversal root without an explicit cycle guard.

**Why:** One symlink loop, a recursive bind mount, or an archive with deep nesting turns a walk into an unbounded loop that exhausts file descriptors or fills the log while the worker looks merely hung; the same walk re-reads a growing tree on every retry and can run past the request timeout on a directory that was small at launch.

**Detect:** `os.walk`, `filepath.Walk`/`WalkDir`, `Files.walk`, `glob(..., recursive=True)`, `Directory.GetFiles(..., SearchOption.AllDirectories)`, `find` in scripts and Makefiles; check for a depth or `maxdepth` cap, an entry counter that aborts, `followlinks=False` or an `lstat`/`O_NOFOLLOW` guard, and whether the walk root is request-controlled.

**References:** CWE-400, CWE-674
