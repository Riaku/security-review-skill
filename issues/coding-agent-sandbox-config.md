# Coding-Agent Sandbox & Permission-Mode Review

**MUST** review how coding agents are configured: OS-level sandbox on, writes workspace-scoped, network off by default, approval policy enforced — and flag bypass flags (`--yolo`, `dangerously-*`, `bypassPermissions`, `approval=never`).

**Why:** The agent's technical reach, not its instructions, is the real boundary; full-access modes inside a dev container let a malicious repo exfiltrate everything reachable, including the agent's own credentials.

**Detect:** grep agent configs for `--yolo`, `dangerously-bypass`, `sandbox_mode = "danger-full-access"`, `approval_policy = "never"`, `bypassPermissions`; check for OS-enforced sandbox vs advisory-only policy.

**References:** OpenAI Codex approvals/security model, Anthropic /sandbox + permissions, Cursor Run Modes ("best-effort, not a hard boundary")
