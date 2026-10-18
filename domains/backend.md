# backend

Server-side application code: APIs, auth, business logic.

## Detection signals

- Server framework present (Express, Django, Flask, FastAPI, Rails, Spring, Axum, Actix, Gin, .NET)
- Route/handler/controller directories
- No browser bundle as the primary artifact

## Stack quick-map

- Rust/Go/Java/Python/Node backend → web-api-security, authentication, authorization-access-control, secrets-crypto, api-design, correctness-pitfalls, testing-strategy, security-practices
- GraphQL server → add web-api-security (depth limits) and api-design
- Multi-tenant product (per-tenant data, cache or quota) → multi-tenancy
- Vendor SDKs, webhooks or third-party SaaS in the code → third-party-integrations
- ADRs, READMEs or API docs in scope → documentation-quality
