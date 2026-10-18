---
categories: [compliance-privacy, data-pipelines]
domains: [data, governance]
---

# Interactive-Session Artifact Leakage

**MUST NOT** commit interactive-session artifacts (notebooks with executed outputs, REPL dumps, workspace snapshots) that embed the actual data processed during the session.

**Why:** Executed notebooks persist every row/chart they touched inside the committed file — sensitive data ships silently with code review, forks, and clones, invisible to diff tools that show only code.

**Detect:** grep tracked notebook/JSON files for embedded result payloads (`"outputs"`, base64 blobs, table rows); check for output-stripping pre-commit hooks or CI checks on committed notebooks.

**References:** Jupyter notebook security best practices, nbstripout/ClearOutputPreprocessor tooling
