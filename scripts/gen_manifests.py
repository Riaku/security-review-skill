#!/usr/bin/env python3
"""Generate domains/*.md and categories/*.md manifests from scripts/topics.json.

Idempotent: re-run after topics.json changes. Detection signals and stack
quick-maps are hand-authored here (single source), lists are derived there.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOPICS = json.loads((ROOT / "scripts" / "topics.json").read_text())

DOMAINS = {
    "backend": {
        "scope": "Server-side application code: APIs, auth, business logic.",
        "signals": [
            "Server framework present (Express, Django, Flask, FastAPI, Rails, Spring, Axum, Actix, Gin, .NET)",
            "Route/handler/controller directories",
            "No browser bundle as the primary artifact",
        ],
        "quickmap": [
            "Rust/Go/Java/Python/Node backend → web-api-security, authentication, authorization-access-control, secrets-crypto, api-design, correctness-pitfalls, testing-strategy, security-practices",
            "GraphQL server → add web-api-security (depth limits) and api-design",
        ],
    },
    "frontend": {
        "scope": "Browser/client-side code: SPAs, SSR apps, browser-exposed surface.",
        "signals": [
            "package.json with react/vue/angular/svelte/next/nuxt",
            "Browser bundles, HTML templates, hydration code",
        ],
        "quickmap": [
            "React/Vue/Angular SPA or SSR → web-client-security (+ backend categories if a server is in the same repo)",
        ],
    },
    "data": {
        "scope": "Databases, replication, distributed data, queues and async pipelines.",
        "signals": [
            "Migration directories (alembic, flyway, prisma, goose, atlas)",
            "DB clients/drivers in dependencies (postgres, mysql, mongo, redis clients)",
            "Queue clients (kafka, rabbitmq, sqs, celery, sidekiq, bull)",
            "CDC/streaming tooling (debezium, flink)",
        ],
        "quickmap": [
            "Any SQL-backed service → database",
            "Queues/workers present → messaging-async",
            "Multiple datastores or replication/sharding configured → distributed-systems",
        ],
    },
    "infrastructure": {
        "scope": "How it is built and where it runs: containers, cloud, CI/CD.",
        "signals": [
            "Dockerfile / docker-compose / Containerfile",
            "Kubernetes manifests, Helm charts, kustomize, operators",
            "Terraform/OpenTofu/Pulumi/CloudFormation/Bicep",
            ".github/workflows, .gitlab-ci.yml, Jenkinsfile, argo/flux configs",
        ],
        "quickmap": [
            "Dockerfile present → containers-k8s, supply-chain",
            "K8s manifests/Helm → containers-k8s, cloud-network, sre-incidents",
            "IaC present → deployment-release, cloud-network",
            "CI config present → cicd-pipeline-security, supply-chain",
        ],
    },
    "reliability": {
        "scope": "Runtime behavior under load and failure: resilience, caching, observability, SRE.",
        "signals": [
            "Retry/timeout/circuit-breaker libraries",
            "Cache layers (redis, memcached, CDN config)",
            "Metrics/tracing/logging libraries (prometheus, OTel, structured loggers)",
            "Health endpoints, probes, autoscaling config",
        ],
        "quickmap": [
            "Any networked service → resilience, observability, sre-incidents",
            "Cache layer present → caching",
            "Autoscaling/load-sensitive → scaling-capacity",
        ],
    },
    "governance": {
        "scope": "Privacy, compliance-adjacent code, AI features, payments.",
        "signals": [
            "PII handling: user profile models, export/delete endpoints, cookies",
            "Payment SDKs (stripe, braintree, adyen) or billing code",
            "LLM API usage (openai, anthropic, ollama, langchain), vector stores",
        ],
        "quickmap": [
            "User personal data stored → compliance-privacy",
            "Payment flows → payments-fraud, compliance-privacy",
            "LLM/vector features → ai-llm, supply-chain",
        ],
    },
    "mobile": {
        "scope": "Native and cross-platform mobile clients.",
        "signals": [
            "Xcode projects (.xcodeproj, .xcworkspace), Gradle/AndroidManifest.xml",
            "React Native, Flutter/Expo manifests",
        ],
        "quickmap": [
            "iOS/Android/RN/Flutter app → mobile (+ backend categories for its API)",
        ],
    },
    "government-compliance": {
        "scope": "Hardening baselines and regulatory regimes (CIS/STIG/FedRAMP/NIST/…).",
        "signals": [
            "compliance/ directory or FedRAMP/STIG/CIS/ITAR/CUI mentions in docs",
            "kube-bench, Lynis, Trivy misconfig, SCAP tooling configs",
            "Government/defense customer contracts or data marked CUI/ITAR",
        ],
        "quickmap": [
            "Any of the above → hardening-benchmarks, regulatory-frameworks",
            "Federal cloud intent → regulatory-frameworks (FedRAMP, NIST 800-53)",
            "Health data → regulatory-frameworks (HIPAA) + compliance-privacy",
        ],
    },
}


def cat_scope(cat: str) -> str:
    return {
        "web-api-security": "Server-side API and web application attack surface.",
        "authentication": "Identity, credentials, session lifecycle.",
        "authorization-access-control": "Who may do what: RBAC, RLS, least privilege.",
        "secrets-crypto": "Secrets handling and cryptographic primitives.",
        "api-design": "Protocol and API contract design concerns.",
        "correctness-pitfalls": "Language-agnostic code-level failure modes.",
        "testing-strategy": "Test pyramid, practices, and quality gates.",
        "security-practices": "Process-level security practices (modeling, disclosure, patching).",
        "web-client-security": "Browser-side attack surface and defenses.",
        "database": "Schema, queries, transactions, replication, backup/recovery.",
        "distributed-systems": "Consistency, consensus, coordination across nodes.",
        "messaging-async": "Queues, delivery semantics, workers, jobs.",
        "supply-chain": "Dependencies, artifacts, build provenance.",
        "cloud-network": "Cloud networking, DNS, edge, cloud resource exposure.",
        "deployment-release": "Release engineering: strategies, environments, versioning.",
        "containers-k8s": "Container and Kubernetes runtime configuration.",
        "cicd-pipeline-security": "CI/CD system as an attack surface.",
        "resilience": "Fault-tolerance patterns under dependency failure.",
        "caching": "Cache correctness, performance, and eviction.",
        "observability": "Logs, metrics, traces, profiling, alerting.",
        "sre-incidents": "Operational readiness: DR, incidents, SLOs, on-call.",
        "scaling-capacity": "Scaling behavior and capacity limits.",
        "compliance-privacy": "Privacy operations and data protection in code.",
        "ai-llm": "LLM feature security and quality.",
        "payments-fraud": "Payment flows, fraud, and money-movement safety.",
        "mobile": "Mobile client security.",
        "hardening-benchmarks": "CIS/STIG-style configuration baselines.",
        "regulatory-frameworks": "Audit and regulatory regimes.",
    }[cat]


def main() -> int:
    # Domain->category index (kept in sync with SKILL.md Category Index; the
    # validator enforces every category is assigned to >=1 domain).
    INDEX = {
        "backend": ["web-api-security", "authentication", "authorization-access-control",
                    "secrets-crypto", "api-design", "correctness-pitfalls",
                    "testing-strategy", "security-practices"],
        "frontend": ["web-client-security"],
        "data": ["database", "distributed-systems", "messaging-async"],
        "infrastructure": ["supply-chain", "cloud-network", "deployment-release",
                          "containers-k8s", "cicd-pipeline-security"],
        "reliability": ["resilience", "caching", "observability", "sre-incidents",
                       "scaling-capacity"],
        "governance": ["compliance-privacy", "ai-llm", "payments-fraud"],
        "mobile": ["mobile"],
        "government-compliance": ["hardening-benchmarks", "regulatory-frameworks"],
    }
    all_cats = sorted({c for t in TOPICS for c in t["categories"]})
    mapped = {c for lst in INDEX.values() for c in lst}
    assert mapped == set(all_cats), f"index mismatch: {set(all_cats) ^ mapped}"

    (ROOT / "domains").mkdir(exist_ok=True)
    (ROOT / "categories").mkdir(exist_ok=True)

    for dom, spec in DOMAINS.items():
        lines = [f"# {dom}", "", spec["scope"], "", "Detection signals:",
                 *[f"- {s}" for s in spec["signals"]], "", "Categories:"]
        lines += [f"- `{c}`" for c in INDEX[dom]]
        lines += ["", "## Stack quick-map", ""]
        lines += [f"- {m}" for m in spec["quickmap"]]
        (ROOT / "domains" / f"{dom}.md").write_text("\n".join(lines) + "\n")

    for cat in all_cats:
        slugs = [t["slug"] for t in TOPICS if cat in t["categories"]]
        lines = [f"# {cat}", "", cat_scope(cat), "", "Issues:"]
        lines += [f"- `{s}`" for s in slugs]
        (ROOT / "categories" / f"{cat}.md").write_text("\n".join(lines) + "\n")

    # Bulk bundles: one generated file per category with every item inlined.
    # For harnesses that prefer few large reads over many small ones. Generated
    # artifact — never hand-edit; edit issues/<slug>.md and re-run this script.
    (ROOT / "bundles").mkdir(exist_ok=True)
    for cat in all_cats:
        slugs = [t["slug"] for t in TOPICS if cat in t["categories"]]
        parts = [f"# {cat} — full checklist ({len(slugs)} items)", "",
                 cat_scope(cat), "",
                 "> Generated artifact. Canonical source: `issues/<slug>.md`.", ""]
        for s in slugs:
            body = (ROOT / "issues" / f"{s}.md").read_text().rstrip()
            parts += [body, ""]
        (ROOT / "bundles" / f"{cat}.md").write_text("\n".join(parts) + "\n")

    print(f"Wrote {len(DOMAINS)} domains, {len(all_cats)} categories "
          f"(+ {len(all_cats)} bundles) covering {len(TOPICS)} topics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
