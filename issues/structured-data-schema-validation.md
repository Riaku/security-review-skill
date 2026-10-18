# Structured Data (Schema.org) Validation

**SHOULD** emit valid JSON-LD structured data (Organization, Product, Article, FAQ, BreadcrumbList) and validate it before deploy.

**Why:** Invalid or misleading structured data forfeits rich results and can trigger a structured-data manual action; valid markup is free SERP real estate.

**Detect:** grep templates for `application/ld+json`; run Rich Results Test / Schema validator in CI; diff required vs emitted properties per type.

**References:** Google Search Central structured data docs, schema.org validators, Rich Results Test
