# third-party-integrations — full checklist (5 items)

SaaS integration surface: scopes, tags, webhooks, credentials.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/third-party-integrations.md](../categories/third-party-integrations.md) · Index: [SKILL.md](../SKILL.md)

# Backing Services as Attached Resources

**SHOULD** access every backing service (database, queue, cache, SMTP) through an environment-supplied location and credential so the specific provider or instance can be swapped without code changes.

**Why:** Hardcoded provider hostnames and instance identifiers block credential rotation, block moving to a managed or failover instance, and leak internal topology into the repo. A compromise of one provider instance becomes a code-change emergency instead of a config swap.

**Detect:** grep code for hardcoded connection strings, provider URLs, and instance IDs instead of injected bindings; verify a staging deploy can point at a different provider instance with config only.

**References:** 12factor.net/backing-services, OWASP Docker Top 10 (D-04 secrets), CWE-798 hardcoded credentials

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

# SaaS Webhook Consumer Trust

**MUST** verify signature, origin, and replay-protection on every inbound webhook from third-party SaaS — and treat payload contents as untrusted input.

**Why:** Unverified webhook endpoints accept forged events ("payment captured", "user verified") from anyone who finds the URL; SaaS signing secrets also rotate, which unverified integrations hide until they break.

**Detect:** grep webhook handlers for signature verification (HMAC compare, provider SDK `constructEvent`), timestamp tolerance checks, idempotency-key dedupe; flag handlers that trust payload identity fields blindly.

**References:** OWASP Webhook Security practices, Stripe/GitHub webhook verification docs, CWE-345 insufficient verification of data authenticity

# Third-Party Tag & Script Governance

**MUST** inventory, approve, and CSP-restrict every third-party script loaded in the app (analytics, marketing tags, chat widgets).

**Why:** Marketing tags execute with your page's full privileges — a compromised tag is a Magecart-class supply-chain attack on your users' sessions and payment data.

**Detect:** list `<script src>` third-party hosts in templates; check CSP `script-src` uses nonces/hashes not `unsafe-inline`/wildcards; look for tag-manager sprawl without an approval list.

**References:** OWASP Magecart/Client-side supply chain, CSP script-src guidance, W3C CSP Level 3

