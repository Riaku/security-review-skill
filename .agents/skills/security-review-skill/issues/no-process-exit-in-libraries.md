---
categories: [correctness-pitfalls]
domains: [backend]
---

# No Process Exit in Libraries

**MUST NOT** call process-exit primitives from library or handler code.

**Why:** An immediate exit skips every destructor, deferred call, and finally block, leaving locks held, buffers unflushed, and temp files behind.

**Detect:** grep os.Exit(, process.exit(, System.exit(, std::process::exit, die( outside main or entrypoint files

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook
