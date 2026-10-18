# Review-Bot Neutral-Status Trap

**MUST** verify that AI review gates actually fail on unresolved findings — a required status that reports neutral/success while findings remain open does not block merges.

**Why:** Cursor documents this explicitly (findings default to neutral; you must enable fail-on-unresolved); GitHub Copilot defaults to "Comment" not "Approve" — teams often believe they have an AI gate they don't have.

**Detect:** branch protection requiring a bot check whose conclusion set lacks failure-on-findings; severity thresholds set above real risk; review config where unresolved ≠ failed.

**References:** Cursor Bugbot status semantics, GitHub Copilot review default-Comment behavior, Gemini severity-threshold filtering
