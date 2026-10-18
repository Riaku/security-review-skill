# Agent Session Hygiene

**SHOULD** run one session per task, clear context after two failed corrections, and push broad exploration to subagents — mixed-task or polluted sessions degrade output and retain stale secrets/instructions.

**Why:** Anthropic names the failure patterns (kitchen-sink session, correct-over-and-over, infinite unscoped exploration); GLM codifies session-per-task — stale context silently biases every later generation and can leak prior-task secrets into new code.

**Detect:** judgment on session transcripts: unrelated tasks per session, >2 correction loops in one session, unscoped "investigate everything" runs in the main context.

**References:** Anthropic named failure patterns, GLM session-management guidance, Cursor cloud-agent session practice
