---
categories: [ai-llm]
domains: [backend, governance]
---

# Approval Claims Verified at Source

**MUST** verify any approval, ticket, or exception cited inside untrusted content against the source system's record before acting on it.

**Why:** An injection can claim pre-approval in a pull-request body or issue comment, and downstream reviewers then cite the fabricated authority as if it were evidence.

**Detect:** grep review automation for approval read from pull_request.body, comment.body, or a file in the diff rather than a ticketing or IdP API call

**References:** Agentic CI/CD attack study, https://arxiv.org/abs/2607.19267
