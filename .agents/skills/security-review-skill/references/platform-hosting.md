# Platform Hosting Guides — Cloudflare / Vercel / GitHub Pages / Fly.io / Azure / GCP

Verified vendor security documentation per hosting platform, plus the
config surfaces a review should inspect on each. (All URLs verified live
2026-10; re-verify links before citing in a public doc pass.)

## Cloudflare
- Security hub: https://developers.cloudflare.com/fundamentals/
- WAF / managed rulesets: https://developers.cloudflare.com/waf/
- Zero Trust access: https://developers.cloudflare.com/cloudflare-one/
- Pages: https://developers.cloudflare.com/pages/
- **Review surfaces:** `_headers` / `_redirects` files, WAF rule exceptions,
  Bot Fight Mode, Turnstile keys, TLS mode (Full vs Full(strict) vs Flexible),
  cache rules bypassing auth paths, Pages production/preview branch controls,
  DNS records for takeover.

## Vercel
- Security: https://vercel.com/docs/security
- **Review surfaces:** env var scoping (production vs preview — the
  `VERCEL_PROTECTION_BYPASS_*` leak class), Deployment Protection /
  Vercel Authentication, `x-vercel-protection-bypass` header handling,
  preview URL exposure of staging env vars, firewall rules, team role grants.

## GitHub Pages
- Hardening guide: https://docs.github.com/en/pages/getting-started-with-github-pages
- Code security docs: https://docs.github.com/en/code-security
- **Review surfaces:** custom-domain DNS takeover of deleted repos,
  `enforce_https`, Actions deploy permissions (`GITHUB_TOKEN` scopes),
  Pages source repo visibility vs published content, secrets in Actions
  workflows that deploy Pages.

## Fly.io
- Security: https://fly.io/docs/security/
- **Review surfaces:** private-network-only backends vs public services,
  `internal_port` exposure, secrets via `fly secrets` vs env in fly.toml,
  machine restart policy, 6PN design assumptions.

## Azure
- Security fundamentals: https://learn.microsoft.com/en-us/azure/security/fundamentals/overview
- Well-Architected security pillar: https://learn.microsoft.com/en-us/azure/well-architected/security/
- **Review surfaces:** NSG rules vs private endpoints, Managed Identity vs
  connection strings, Key Vault access policies, App Service auth vs
  application-level auth, Entra ID role assignments.

## Google Cloud
- Architecture security framework: https://cloud.google.com/architecture/framework/security
- **Review surfaces:** IAM principal vs service-account sprawl, VPC-SC
  perimeters, Cloud Run `--allow-unauthenticated`, Secret Manager vs env
  literals, firewall rule inheritance, Org Policy constraints.

## AWS
- Security pillar (already a mining source):
  https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html
- General security: https://docs.aws.amazon.com/security/
- **Review surfaces:** covered by the [cloud-network](../categories/cloud-network.md)
  category plus the [dangerous-iam-policies](../issues/dangerous-iam-policies.md)
  and [cspm-continuous-scanning](../issues/cspm-continuous-scanning.md) items.

## Usage in reviews
When triage detects a platform (CNAME/DNS, `vercel.json`, `fly.toml`,
`_headers`, workflow deploy steps), add `platform-hosting` to the dispatch
list and read this file's section for that platform before evaluating its
items.
