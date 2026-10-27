# OWASP Coverage Map

Which items carry each control on the three OWASP lists this skill tracks, and how firmly.
Coverage is judged by **obligation** — what an item's statement actually requires — not by the
citation strings in its `**References:**` line, which can be inherited from a bulk import or
attached to the wrong item. A control is covered when at least one item states an obligation
that would prevent it, and strengthened when several items cover different layers: the rule,
the test that proves it, and the detection that catches it in production.

Versions tracked: **OWASP Top 10 (2021)**, **OWASP API Security Top 10 (2023)**,
**OWASP Top 10 for LLM Applications (2025)**. Item count: 998. Last verified: 2026-10-27.

## OWASP Top 10 (2021)

### A01:2021 Broken Access Control — MUST

`authorization-default-deny` · `idor` · `api-gateway-missing-authorizers` · `composed-path-tenant-isolation` · `csrf`

### A02:2021 Cryptographic Failures — MUST

`crypto-inventory` · `encryption-at-rest` · `jwt-algorithm-confusion` · `bcrypt-argon2` · `hsts`

### A03:2021 Injection — MUST

`sql-injection` · `xss` · `os-command-injection` · `path-traversal` · `server-side-template-injection` · `nosql-injection` · `ldap-injection` · `crlf-header-injection` · `log-injection`

### A04:2021 Insecure Design — MUST

`threat-modeling` · `secure-by-design` · `abuse-case-per-feature` · `security-requirements-explicit` · `fail-secure-configuration` · `business-logic-bypass`

Citations for this control previously landed on cache and rate-limit items; the design-time carriers above now cite it directly.

### A05:2021 Security Misconfiguration — MUST

`debug-mode-in-production` · `security-headers` · `cors` · `content-security-policy` · `open-directory-listing` · `cspm-continuous-scanning`

### A06:2021 Vulnerable and Outdated Components — MUST

`dependency-vulnerabilities` · `lockfiles` · `image-scanning` · `sbom-generation` · `patch-management-sla` · `end-of-support-components`

### A07:2021 Identification and Authentication Failures — MUST

`account-enumeration` · `brute-force-protection` · `breached-password-blocklist` · `account-recovery-security` · `jwt-audience-issuer-validation`

### A08:2021 Software and Data Integrity Failures — MUST

`insecure-deserialization` · `dependency-confusion` · `artifact-integrity-verification` · `build-provenance-attestation` · `ci-action-pinning` · `subresource-integrity`

The application half (deserialization, dependency confusion) was cited; the build and artifact half above was not.

### A09:2021 Security Logging and Monitoring Failures — MUST

`audit-logs` · `k8s-api-audit-logging` · `management-plane-activity-alerting` · `detection-log-source-liveness` · `alert-delivery-verification` · `runtime-threat-detection` · `object-level-data-access-logging`

No primary logging or alerting item cited this control before; the two items that did were about cache write policy and cost alarms.

### A10:2021 Server-Side Request Forgery — MUST

`ssrf` · `egress-control` · `cloud-metadata-endpoint` · `dns-rebinding`

## OWASP API Security Top 10 (2023)

### API1:2023 Broken Object Level Authorization — MUST

`idor` · `object-authz-beyond-spec` · `spec-derived-bola-tests` · `tenant-id-spoofing-api-boundary`

### API2:2023 Broken Authentication — MUST

`mfa` · `brute-force-protection` · `jwt-expiry` · `session-fixation` · `account-enumeration`

Coverage is spread across the JWT, session, and credential cluster rather than concentrated in one authentication item.

### API3:2023 Broken Object Property Level Authorization — MUST

`excessive-data-exposure` · `mass-assignment`

### API4:2023 Unrestricted Resource Consumption — MUST

`rate-limiting` · `cost-based-rate-limiting` · `request-size-limits` · `per-request-resource-budgets` · `parser-resource-limits` · `cursor-based-pagination`

### API5:2023 Broken Function Level Authorization — MUST

`api-gateway-missing-authorizers` · `rbac` · `http-method-semantics`

No item is titled after this control; the route-level default-deny rule in the first item is the control.

### API6:2023 Unrestricted Access to Sensitive Business Flows — MUST

`business-logic-bypass` · `bot-protection` · `fraud-structural-invariants` · `push-bombing-defense`

### API7:2023 Server Side Request Forgery — MUST

`ssrf` · `dns-rebinding` · `cloud-metadata-endpoint`

### API8:2023 Security Misconfiguration — MUST

`cors` · `security-headers` · `debug-mode-in-production` · `generic-error-responses`

### API9:2023 Improper Inventory Management — MUST

`openapi-specs` · `openapi-implementation-drift-check` · `api-version-retirement` · `input-entry-point-inventory` · `attack-surface-management`

### API10:2023 Unsafe Consumption of APIs — MUST

`third-party-response-validation` · `webhook-signature-verification` · `webhook-replay-protection` · `payment-webhook-reconciliation`

## OWASP Top 10 for LLM Applications (2025)

### LLM01:2025 Prompt Injection — MUST

`prompt-injection` · `tool-argument-injection` · `eval-outcome-classification`

### LLM02:2025 Sensitive Information Disclosure — MUST

`llm-api-pii-redaction` · `training-data-reconstruction` · `embedding-inversion-vector-stores` · `synthetic-data-memorisation-checks`

### LLM03:2025 Supply Chain — MUST

`ai-third-party-components` · `model-artifact-integrity` · `mcp-plugin-trust` · `hallucinated-packages` · `model-version-pinning`

Weight-level tampering is covered only through artifact integrity and version pinning, not by a rule about backdoored weights.

### LLM04:2025 Data and Model Poisoning — MUST

`training-data-trust-boundary` · `rag-poisoning` · `codegen-corpus-security-vetting`

### LLM05:2025 Improper Output Handling — MUST

`llm-output-untrusted` · `output-filter-bypass` · `agent-output-trust-per-hop`

### LLM06:2025 Excessive Agency — MUST

`agent-tool-authorization` · `agent-tool-call-value-authorization` · `agent-hitl-approval` · `unattended-agent-automation-governance`

### LLM07:2025 System Prompt Leakage — SHOULD

`system-prompt-extraction`

One item, SHOULD-strength: it governs what may be placed in a prompt, not whether the prompt itself is treated as confidential.

### LLM08:2025 Vector and Embedding Weaknesses — MUST

`vector-retrieval-authorization` · `embedding-inversion-vector-stores` · `rag-poisoning` · `agent-memory-isolation`

Retrieval-time authorization (`vector-retrieval-authorization`) was the missing half; the item was added with this map.

### LLM09:2025 Misinformation — MUST

`llm-answer-grounding`

No item covered this control before (`llm-answer-grounding`, added with this map). It is the only control on any of the three lists that had no carrier at all. Human sign-off before an irreversible agent action is carried by `agent-hitl-approval`; for user-facing claims this item requires withholding instead of review.

### LLM10:2025 Unbounded Consumption — MUST

`llm-denial-of-wallet` · `model-extraction-throttling` · `context-windows`

Spend and context limits were covered; model extraction through the inference API (`model-extraction-throttling`, added with this map) was not.

## Soft spots

- **A06 fixed versions.** `dependency-vulnerabilities` requires scanning and `patch-management-sla`
  bounds time-to-fix, but nothing binds a resolved version to an advisory's `Fixed in` field:
  no item forbids shipping a lockfile that pins a below-fix version of a known-vulnerable package.
- **LLM07** is a single SHOULD-strength item about prompt content. If a deployment treats the
  system prompt as an asset (routing rules, guard logic, tenant configuration), there is no rule
  requiring it to survive disclosure.
- **LLM03 weights.** Provenance and pinning catch substitution, but a backdoored first-party
  fine-tune is only caught by evaluation, and no item requires adversarial evaluation of a model
  before promotion.
- **API inventory.** `openapi-specs` and `openapi-implementation-drift-check` cover the declared
  surface; nothing enumerates endpoints that never made it into a spec, beyond
  `input-entry-point-inventory`.

## Maintaining this map

When an item is added, renamed, or split, update its control line here in the same change — a
slug that no longer exists is a broken map, and `scripts/check_generated.py` does not catch it.
Re-audit a list by reading each item's statement against the control definition; do not audit by
grepping `References`, which is how the citation defects in this map accumulated in the first
place.
