---
categories: [authorization-access-control]
domains: [backend]
---

# Permissions From Declared Operation

**MUST** derive the runtime permission of a tool invocation from the operation it declares, not from the ambient rights of the approving process.

**Why:** Approving a narrow action while handing the executor broad host access creates a laundering channel where steered arguments reach files outside the declared scope.

**Detect:** grep tool and plugin host config for ambient grants applied to per-call execution (`privileged: true`, `--mount`, `cap_add`, `seccomp=unconfined`) where the declared operation needs none.

**References:** My Credentials, Please: tool approval scope laundering, https://arxiv.org/abs/2610.22301
