#!/usr/bin/env python3
"""Generate the skill's link-bearing artifacts from scripts/topics.json.

Writes:
  domains/*.md              detection signals + quick-map, categories as links
  categories/*.md           the category's items as links to issues/<slug>.md
  bundles/*.md              every item of a category inlined (bulk artifact)
  references/tool-index.md  tool -> issue links
  issues/*.md               ONLY the trailing "**Part of:**" nav footer

Everything cross-links by relative markdown link (see scripts/manifest_links.py)
so any document can be clicked through to its neighbours.

Idempotent: re-run after topics.json changes. Detection signals, scopes, and
stack quick-maps are hand-authored here (single source); the link lists and the
per-issue nav footers are derived from scripts/topics.json.
"""
import json
import pathlib
import re

import manifest_links as ml

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
        "scope": "Databases, replication, distributed data, queues, async pipelines, and data/ETL platforms.",
        "signals": [
            "Migration directories (alembic, flyway, prisma, goose, atlas)",
            "DB clients/drivers in dependencies (postgres, mysql, mongo, redis clients)",
            "Queue clients (kafka, rabbitmq, sqs, celery, sidekiq, bull)",
            "CDC/streaming tooling (debezium, flink)",
            "Data-pipeline tooling (airflow/ dags/ dir, dbt projects, spark jobs, glue, dataflow)",
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
    "iot-embedded": {
        "scope": "Firmware, embedded devices, and device-paired services.",
        "signals": [
            "Firmware toolchains: PlatformIO.ini, ESP-IDF, Zephyr, mbed, MCUboot, linker scripts for MCU targets",
            "C/C++ bare-metal or RTOS code, .bin/.elf firmware artifacts, OTA update services",
            "Hardware SDKs paired with mobile/cloud apps (BLE/Matter/MQTT device code)",
        ],
        "quickmap": [
            "Any firmware/OTA/device-provisioning code → iot-embedded, supply-chain",
            "Device + cloud backend → also backend categories for the paired API",
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
        "seo-web-quality": "Search visibility, crawl/index hygiene, and page experience (Google Search Central, CWV, Lighthouse).",
        "multi-tenancy": "Tenant isolation across API, data, cache, queues, and lifecycle.",
        "email-security": "Mail authentication, brand protection, and email-content trust.",
        "iot-embedded": "Firmware, OTA, and device-identity security.",
        "third-party-integrations": "SaaS integration surface: scopes, tags, webhooks, credentials.",
        "data-pipelines": "ETL/orchestration security: pipeline creds, lineage, backfill safety.",
        "documentation-quality": "Docs and comments quality: BCP 14 keywords, style, sync with code, runnable READMEs.",
    }[cat]


def linkify_cats(text: str, cats) -> str:
    """Link full-word category names in prose to their manifest.

    One pass over an alternation sorted longest-first, so a name that is a
    prefix of another (or that appears inside an inserted link target) is never
    matched twice.
    """
    names = sorted(cats, key=len, reverse=True)
    pattern = re.compile(r"(?<![\w-])(" + "|".join(re.escape(c) for c in names)
                         + r")(?![\w-])")
    return pattern.sub(lambda m: ml.category_link(m.group(1)), text)


def main() -> int:
    # Domain->category index (single source in manifest_links.py; SKILL.md's
    # Category Index mirrors it and the validator enforces both the assignment
    # of every category to >=1 domain and the SKILL.md table's agreement).
    INDEX = ml.DOMAIN_INDEX
    all_cats = sorted({c for t in TOPICS for c in t["categories"]})
    mapped = {c for lst in INDEX.values() for c in lst}
    assert mapped == set(all_cats), f"index mismatch: {set(all_cats) ^ mapped}"

    (ROOT / "domains").mkdir(exist_ok=True)
    (ROOT / "categories").mkdir(exist_ok=True)

    # Per-issue nav footer (category links + their domains + SKILL.md). Written
    # before bundles so the inlined copies carry the same footer. Only the
    # trailing footer block is touched; the item body is canonical content.
    for t in TOPICS:
        f = ROOT / "issues" / f"{t['slug']}.md"
        text = f.read_text()
        updated = ml.with_footer(text, t["categories"])
        if updated != text:
            f.write_text(updated)

    for dom, spec in DOMAINS.items():
        lines = [f"# {dom}", "", spec["scope"], "",
                 f"Index: {ml.SKILL_LINK}", "",
                 "Detection signals:",
                 *[f"- {s}" for s in spec["signals"]], "", "Categories:"]
        lines += [f"- {ml.category_link(c)}" for c in INDEX[dom]]
        lines += ["", "## Stack quick-map", ""]
        lines += [f"- {linkify_cats(m, all_cats)}" for m in spec["quickmap"]]
        (ROOT / "domains" / f"{dom}.md").write_text("\n".join(lines) + "\n")

    for cat in all_cats:
        slugs = [t["slug"] for t in TOPICS if cat in t["categories"]]
        doms = ml.domains_of([cat])
        dom_label = "Domain:" if len(doms) == 1 else "Domains:"
        nav = (f"{dom_label} "
               + " · ".join([*[ml.domain_link(d) for d in doms],
                             f"Index: {ml.SKILL_LINK}"]))
        lines = [f"# {cat}", "", cat_scope(cat), "", nav, "", "Issues:"]
        lines += [f"- {ml.issue_link(s)}" for s in slugs]
        (ROOT / "categories" / f"{cat}.md").write_text("\n".join(lines) + "\n")

    # Bulk bundles: one generated file per category with every item inlined.
    # For harnesses that prefer few large reads over many small ones. Generated
    # artifact — never hand-edit; edit issues/<slug>.md and re-run this script.
    # Each inlined item keeps its nav footer, so a bundle entry clicks through
    # to its canonical issues/<slug>.md.
    (ROOT / "bundles").mkdir(exist_ok=True)
    for cat in all_cats:
        slugs = [t["slug"] for t in TOPICS if cat in t["categories"]]
        parts = [f"# {cat} — full checklist ({len(slugs)} items)", "",
                 cat_scope(cat), "",
                 "> Generated artifact — edit the issue files, not this one. "
                 f"Sources: {ml.ISSUES_DIR_LINK} · manifest: "
                 f"{ml.category_link(cat)} · index: {ml.SKILL_LINK}", ""]
        for s in slugs:
            body = (ROOT / "issues" / f"{s}.md").read_text().rstrip()
            parts += [body, ""]
        (ROOT / "bundles" / f"{cat}.md").write_text("\n".join(parts) + "\n")

    # Tool -> issues reverse index from scripts/tool-issues.json (standard
    # machine-readable mapping; single source for tool cross-references).
    mapping = json.loads((ROOT / "scripts" / "tool-issues.json").read_text())
    slug_set = {t["slug"] for t in TOPICS}
    for tool, slugs in mapping.items():
        missing = [s for s in slugs if s not in slug_set]
        assert not missing, f"tool {tool} references unknown issues: {missing}"
    (ROOT / "references").mkdir(exist_ok=True)
    lines = ["# Tool → Issues Index", "",
             "Generated from `scripts/tool-issues.json` (do not hand-edit). "
             f"Sources: {ml.ISSUES_DIR_LINK} · index: {ml.SKILL_LINK}", ""]
    for tool in sorted(mapping):
        lines.append(f"## {tool}")
        lines += [f"- {ml.issue_link(s)}" for s in mapping[tool]]
        lines.append("")
    (ROOT / "references" / "tool-index.md").write_text("\n".join(lines) + "\n")

    print(f"Wrote {len(DOMAINS)} domains, {len(all_cats)} categories "
          f"(+ {len(all_cats)} bundles, {len(mapping)} tool mappings) "
          f"covering {len(TOPICS)} topics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
