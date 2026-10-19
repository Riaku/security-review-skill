# third-party-integrations

SaaS integration surface: scopes, tags, webhooks, credentials.

## What this category covers

This category covers the trust and configuration surface exposed by integrating third-party services into an application: what a vendor is allowed to do, how its credentials are held, and where its data enters the system. Its member items span OAuth scope grants to identity providers, inbound SaaS webhooks, embedded third-party tags and scripts, SaaS credential inventories, and twelve-factor backing-service binding. A reviewer working here should trace each external integration from the credential that authorizes it, through the data it sends or receives, to the boundary where that data stops being trusted. Findings tend to be an integration granted more than it needs, or inbound payloads believed without verification.

- OAuth scope minimization and granted-scope drift for third-party apps.
- Inbound webhook trust: signature, origin, and replay checks on provider callbacks.
- Third-party script and tag inventory, approval, and CSP restriction.
- Credential centralization for SaaS integrations, with owner, scope, and expiry.
- Backing-service binding through environment-supplied locations, so providers stay swappable.

## What it does not cover

- [secrets-crypto](../categories/secrets-crypto.md) — the storage, encryption, and rotation mechanics of a secret belong there; this category covers the integration it authorizes, its scope, and its owner.
- [authentication](../categories/authentication.md) — the OAuth/OIDC flow, token issuance, and token validation for your own users belong there, not the scopes you request from a third party.
- [supply-chain](../categories/supply-chain.md) — build-time dependencies, package registries, and vendor risk registers belong there; this category is the runtime surface of live integrations.
- [web-client-security](../categories/web-client-security.md) — how a loaded script is sandboxed and how CSP is delivered belong there; the vendor inventory and approval decision belong here.

## What a finding here looks like

- an integration granted `mail.readwrite` or an admin scope when read-only access was all the feature used.
- an inbound provider webhook whose payload is written to the database before its signature is checked, or with no replay window.
- a marketing tag loaded without an inventory entry, so nobody can say what it collects or revoke it.
- the same SaaS API key pasted into a wiki page, a CI variable, and two developers' local files, with no owner or expiry.
- a provider hostname hardcoded in application code, so switching vendors requires a redeploy.
