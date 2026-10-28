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
- Service calls an LLM, embeds documents or runs agent tooling → ai-llm
- Cloud SDKs, VPC/security-group code or service mesh → cloud-network
- Server-rendered HTML or a browser surface in the same repo → web-client-security
- Pinned dependencies, base images or vendored code → supply-chain
- Personal-data models, cookies or export/delete endpoints → compliance-privacy
- Metrics, logs or alert wiring present → observability
- Payment, pricing or billing flows → payments-fraud
- Rate limits, quotas or load-sensitive endpoints → scaling-capacity
- Outbound calls or background jobs → resilience
- Service sends email (transactional or bulk) → email-security
