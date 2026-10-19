# third-party-integrations — full checklist (5 items)

SaaS integration surface: scopes, tags, webhooks, credentials.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/third-party-integrations.md](../categories/third-party-integrations.md) · Index: [SKILL.md](../SKILL.md)

# Integration Credential Sprawl

**SHOULD** centralize third-party SaaS credentials in a secrets manager with owner, scope, and expiry metadata — no credentials in shared docs, wikis, or personal accounts.

**Why:** SaaS credential sprawl (one per engineer, pasted in runbooks, never rotated) makes offboarding impossible to audit and breach blast radius unknowable.

**Detect:** inventory integration creds: count vs documented owners; grep wikis/runbooks/env files for SaaS API keys; check rotation history per integration; flag creds tied to individual employees.

**References:** NIST SP 800-53 IA-5, OWASP Secrets Management Cheat Sheet, vendor SSO/API-token best practices

# OAuth Third-Party Scope Minimization

**MUST** request the minimum OAuth scopes from identity providers and audit granted-scope drift for third-party app integrations.

**Why:** Over-scoped integrations (`offline_access`, full mailbox, full repo) turn a third-party breach into your breach; scopes granted years ago silently persist.

**Detect:** review OAuth app registrations for scopes beyond current feature needs; grep client code for scope strings vs actual API calls used; check admin consent logs for over-granted apps.

**References:** OAuth 2.0 BCP scope guidance, OWASP API Security (insufficient scope), Microsoft/Google admin consent audit docs

# Third-Party Tag & Script Governance

**MUST** inventory, approve, and CSP-restrict every third-party script loaded in the app (analytics, marketing tags, chat widgets).

**Why:** Marketing tags execute with your page's full privileges — a compromised tag is a Magecart-class supply-chain attack on your users' sessions and payment data.

**Detect:** list `<script src>` third-party hosts in templates; check CSP `script-src` uses nonces/hashes not `unsafe-inline`/wildcards; look for tag-manager sprawl without an approval list.

**References:** OWASP Magecart/Client-side supply chain, CSP script-src guidance, W3C CSP Level 3

# 12-Factor Apps

**SHOULD** externalize config to the environment — reaching every backing service (database, queue, cache, SMTP) through an environment-supplied location and credential so the provider or instance can be swapped without a code change — and treat processes as stateless, so no secret or session state is baked into images or local disk.

**Why:** Config compiled into images leaks through registry access and forces rebuilds to rotate credentials, slowing response to a compromise; hardcoded provider hostnames and instance identifiers likewise block credential rotation and moving to a managed or failover instance, and leak internal topology into the repo.

**Detect:** grep images/repos for hardcoded hosts, ports, credentials, connection strings, provider URLs, and instance IDs instead of `env`/`ConfigMap` or injected bindings; check for session data written to container filesystem paths; verify a staging deploy can point at a different provider instance with config only.

**References:** 12factor.net config/stateless factors, 12factor.net/backing-services, OWASP Docker Top 10 D06 (Protect Secrets), CWE-798 hardcoded credentials

# Webhook Signature & Origin Verification

**MUST** verify the provider HMAC over the raw body with constant-time comparison before acting on any webhook, validate the `Origin` header against an explicit allowlist, and treat payload contents — identity fields included — as untrusted input.

**Why:** Unsigned endpoints accept forged events — fake payments, refunds, account changes — from anyone who finds the URL; a handler that trusts payload identity fields blindly is the same exposure, and SaaS signing secrets rotate, so an unverified integration hides the breakage until it fails.

**Detect:** Handlers with no signature check; `hmac.compare_digest` absent; verification skipped in dev branches; no origin check; no idempotency-key dedupe; provider SDK helpers (`constructEvent`) unused; handlers that trust payload identity fields blindly.

**References:** CWE-347, CWE-345, CWE-208, OWASP Webhook Security practices, Stripe/GitHub webhook signing/verification docs

