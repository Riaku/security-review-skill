# governance

Privacy, compliance-adjacent code, AI features, payments.

## Detection signals

- PII handling: user profile models, export/delete endpoints, cookies
- Payment SDKs (stripe, braintree, adyen) or billing code
- LLM API usage (openai, anthropic, ollama, langchain), vector stores

## Stack quick-map

- User personal data stored → compliance-privacy
- Payment flows → payments-fraud, compliance-privacy
- LLM/vector features → ai-llm, supply-chain
- Outbound email (transactional or bulk) → email-security
- Any codebase under review → security-practices (design review is governance work)
- Regulated product (payments, health, children, EU users) → regulatory-frameworks
- Control or policy effectiveness claims → testing-strategy
- Crypto code in scope or artifacts that quote secrets → secrets-crypto
- Artifact publishing or release-account process → authentication
- Policy-as-code or RBAC config present → authorization-access-control
- Vendor contracts or DPAs in scope → third-party-integrations
