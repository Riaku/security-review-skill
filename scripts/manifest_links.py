#!/usr/bin/env python3
"""Shared link vocabulary for this skill's markdown graph.

Every document in the skill cross-links the others with *relative markdown
links*, so a human (or an agent) can click through from any entry point:
`issues/<slug>.md` <-> `categories/<cat>.md` <-> `domains/<domain>.md` <->
`SKILL.md`. No separate "what links to what" record exists; the links are in
the documents themselves.

This module is the single source of that vocabulary and is imported by:

  gen_manifests.py    writes the links: categories/, domains/, bundles/,
                      references/tool-index.md, and the nav footer appended to
                      every issues/<slug>.md
  validate_skill.py   parses the links and checks each footer is accurate
  check_links.py      resolves every relative link in the tree (generic check)

Layout constraint that makes this simple: every navigation target sits exactly
one directory below the repo root (issues/, categories/, domains/, references/,
bundles/, templates/), so the single prefix `../<dir>/<file>.md` is correct from
every document type — including an issue file inlined into a bundle, since
bundles/ is also one level deep. Do not "fix" a link to `./` or an absolute
path; prefix-relative links from the repo root only work for root-level docs
like SKILL.md.
"""
from __future__ import annotations

import re

# --- link builders ---------------------------------------------------------

SKILL_LINK = "[SKILL.md](../SKILL.md)"
ISSUES_DIR_LINK = "[issues/](../issues/)"


def issue_link(slug: str) -> str:
    return f"[{slug}](../issues/{slug}.md)"


def category_link(cat: str) -> str:
    return f"[{cat}](../categories/{cat}.md)"


def domain_link(dom: str) -> str:
    return f"[{dom}](../domains/{dom}.md)"


# --- manifest line parsers (link label and target must agree) --------------

SLUG = r"[a-z0-9][a-z0-9-]*"

# `- [slug](../issues/slug.md)` — an item listed in a categories/*.md manifest.
CAT_ITEM_RE = re.compile(rf"^- \[({SLUG})\]\(\.\./issues/\1\.md\)\s*$", re.M)

# `- [category](../categories/category.md)` — a category listed in a
# domains/*.md manifest.
DOMAIN_ITEM_RE = re.compile(rf"^- \[({SLUG})\]\(\.\./categories/\1\.md\)\s*$", re.M)


def manifest_items(path, pattern) -> list[str]:
    """Labels of every line in `path` matching `pattern` (order preserved)."""
    return pattern.findall(path.read_text())


# --- domain -> category index (single source; also mirrored in SKILL.md) ---

DOMAIN_INDEX = {
    "backend": ["web-api-security", "authentication", "authorization-access-control",
                "secrets-crypto", "api-design", "correctness-pitfalls",
                "testing-strategy", "security-practices", "multi-tenancy",
                "third-party-integrations", "documentation-quality"],
    "frontend": ["web-client-security", "seo-web-quality"],
    "data": ["database", "distributed-systems", "messaging-async", "data-pipelines"],
    "infrastructure": ["supply-chain", "cloud-network", "deployment-release",
                       "containers-k8s", "cicd-pipeline-security"],
    "reliability": ["resilience", "caching", "observability", "sre-incidents",
                    "scaling-capacity"],
    "governance": ["compliance-privacy", "ai-llm", "payments-fraud",
                   "email-security"],
    "mobile": ["mobile"],
    "government-compliance": ["hardening-benchmarks", "regulatory-frameworks"],
    "iot-embedded": ["iot-embedded"],
}


def domains_of(cats) -> list[str]:
    """Domains containing any of `cats`, in DOMAIN_INDEX declaration order."""
    wanted = set(cats)
    return [d for d, members in DOMAIN_INDEX.items() if wanted & set(members)]


# --- per-issue navigation footer ------------------------------------------

FOOTER_MARK = "**Part of:**"
FOOTER_LINE_RE = re.compile(r"^\*\*Part of:\*\*.*$", re.M)
# The trailing footer block: blank line(s), a rule, then the footer line. The
# block is repeatable, so a file that somehow carries two footers converges back
# to one instead of keeping the stale copy when the generator re-runs.
FOOTER_BLOCK_RE = re.compile(
    r"(?:\n+---\n+" + re.escape(FOOTER_MARK) + r"[^\n]*)+[ \t]*\n?\Z")


def render_footer(cats) -> str:
    """Nav footer for an issue in `cats`: category links, their domains, SKILL."""
    cats = sorted(cats)
    doms = domains_of(cats)
    parts = [category_link(c) for c in cats]
    parts += [domain_link(d) for d in doms]
    parts.append(SKILL_LINK)
    return f"---\n\n{FOOTER_MARK} " + " · ".join(parts) + "\n"


def footer_of(text: str) -> str | None:
    """The footer line of an issue file, or None if it has no footer."""
    m = FOOTER_LINE_RE.search(text)
    return m.group(0) if m else None


def footer_line(cats) -> str:
    """The one-line form of the footer, for comparison against footer_of()."""
    return render_footer(cats).splitlines()[-1]


def with_footer(text: str, cats) -> str:
    """`text` with its trailing nav footer replaced by the current one.

    Idempotent: an existing footer (anything from the last `---`/`**Part of:**`
    block at EOF) is stripped first, so regeneration never stacks footers.
    """
    body = FOOTER_BLOCK_RE.sub("", text).rstrip()
    return f"{body}\n\n{render_footer(cats)}"
