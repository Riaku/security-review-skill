#!/usr/bin/env python3
"""Shared conventions for this skill's markdown documents.

Every document cross-links the others with *relative markdown links*, so a
human (or an agent) can click through from any entry point:
`issues/<slug>.md` <-> `categories/<cat>.md` <-> `domains/<domain>.md` <->
`SKILL.md`. There is no "what links to what" record and no data file of any
kind — the links, and each item's membership, live in the documents themselves.

Which parts of each document are authored, and which are generated:

  issues/<slug>.md      authored body; YAML frontmatter declaring the
                        `categories:` and `domains:` the item belongs to (the
                        single source of membership); generated trailing
                        "**Part of:**" nav footer
  categories/<cat>.md   authored scope; generated "## Issues" list + nav line
  domains/<domain>.md   authored scope, detection signals, stack quick-map;
                        generated "## Categories" list + nav line
  bundles/<cat>.md      fully generated: every item of a category inlined

This module is the single source of that vocabulary and is imported by:

  gen_artifacts.py    writes the generated blocks (bundles, manifest list
                      tails, issue nav footers) from the items' frontmatter
  validate_skill.py   parses the links and the frontmatter, checks they agree
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

SLUG = r"[a-z0-9][a-z0-9-]*"

# --- link builders ---------------------------------------------------------

SKILL_LINK = "[SKILL.md](../SKILL.md)"
ISSUES_DIR_LINK = "[issues/](../issues/)"


def issue_link(slug: str) -> str:
    return f"[{slug}](../issues/{slug}.md)"


def category_link(cat: str) -> str:
    return f"[{cat}](../categories/{cat}.md)"


def domain_link(dom: str) -> str:
    return f"[{dom}](../domains/{dom}.md)"


# --- issue frontmatter: the single source of membership --------------------
#
# Authored, on every issues/<slug>.md, exactly:
#
#   ---
#   categories: [a, b]
#   domains: [c]
#   ---
#
# Both keys are required, non-empty, duplicate-free and sorted (canonical form,
# so regeneration is stable); the values are slugs of existing manifests.

META_KEYS = ("categories", "domains")
META_BLOCK_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n\n?", re.S)
META_LINE_RE = re.compile(r"^(categories|domains):\s*\[([^\]]*)\]\s*$")


def meta_block(cats, doms) -> str:
    """Canonical frontmatter block (sorted values) for an issue file."""
    return ("---\n"
            f"categories: [{', '.join(sorted(cats))}]\n"
            f"domains: [{', '.join(sorted(doms))}]\n"
            "---\n\n")


def strip_meta(text: str) -> str:
    """`text` without its leading frontmatter block (the authored body)."""
    return META_BLOCK_RE.sub("", text, count=1)


def item_meta(text: str) -> dict[str, list[str]]:
    """Parsed frontmatter of an issue file; raises ValueError if malformed."""
    m = META_BLOCK_RE.match(text)
    if not m:
        raise ValueError("no frontmatter block at start of file")
    meta: dict[str, list[str]] = {}
    for line in m.group("body").splitlines():
        lm = META_LINE_RE.match(line)
        if not lm:
            raise ValueError(f"line is not `key: [a, b]` — {line!r}")
        raw = lm.group(2).strip()
        meta[lm.group(1)] = [v.strip() for v in raw.split(",")] if raw else []
    missing = [k for k in META_KEYS if k not in meta]
    if missing:
        raise ValueError(f"missing key(s) {', '.join(missing)}")
    extra = sorted(set(meta) - set(META_KEYS))
    if extra:
        raise ValueError(f"unexpected key(s) {', '.join(extra)}")
    for key in META_KEYS:
        vals = meta[key]
        if not vals:
            raise ValueError(f"{key}: empty — an item belongs to at least one")
        if len(set(vals)) != len(vals):
            raise ValueError(f"{key}: repeated value in {vals}")
        if vals != sorted(vals):
            raise ValueError(f"{key}: not sorted — write {sorted(vals)}")
        bad = [v for v in vals if not re.fullmatch(SLUG, v)]
        if bad:
            raise ValueError(f"{key}: not a slug — {', '.join(bad)}")
    return meta


# --- manifest list parsers (link label and target must agree) --------------

# `- [slug](../issues/slug.md)` — an item listed in a categories/*.md manifest.
CAT_ITEM_RE = re.compile(rf"^- \[({SLUG})\]\(\.\./issues/\1\.md\)\s*$", re.M)

# `- [category](../categories/category.md)` — a category listed in a
# domains/*.md manifest.
DOMAIN_ITEM_RE = re.compile(rf"^- \[({SLUG})\]\(\.\./categories/\1\.md\)\s*$", re.M)


def manifest_items(path, pattern) -> list[str]:
    """Labels of every line in `path` matching `pattern` (order preserved)."""
    return pattern.findall(path.read_text())


# --- generated manifest tails ----------------------------------------------
#
# A categories/*.md or domains/*.md file is an authored head (H1, scope, and
# for domains the detection signals and stack quick-map) followed by one
# generated tail: the heading, the membership list, and a nav line. Everything
# from the heading to EOF belongs to the generator; nothing above it is touched.

CAT_TAIL_HEAD = "## Issues"
DOM_TAIL_HEAD = "## Categories"


def tail_of(text: str, heading: str) -> str | None:
    """The generated tail of a manifest (heading to EOF), or None if absent."""
    m = re.search(rf"^{re.escape(heading)}$", text, re.M)
    return text[m.start():] if m else None


def with_tail(text: str, heading: str, tail: str) -> str:
    """`text` with everything from `heading` to EOF replaced by `tail`."""
    m = re.search(rf"^{re.escape(heading)}$", text, re.M)
    head = text[:m.start()] if m else text
    return f"{head.rstrip()}\n\n{tail}"


def render_category_tail(slugs, doms) -> str:
    """`## Issues` tail for a category manifest: its items, then its domain(s)."""
    doms = sorted(doms)
    label = "Domain:" if len(doms) == 1 else "Domains:"
    nav = " · ".join([*(domain_link(d) for d in doms), f"Index: {SKILL_LINK}"])
    lines = [CAT_TAIL_HEAD, "", *[f"- {issue_link(s)}" for s in sorted(slugs)],
             "", f"{label} {nav}"]
    return "\n".join(lines) + "\n"


def render_domain_tail(cats) -> str:
    """`## Categories` tail for a domain manifest: the categories under it."""
    lines = [DOM_TAIL_HEAD, "", *[f"- {category_link(c)}" for c in sorted(cats)],
             "", f"Index: {SKILL_LINK}"]
    return "\n".join(lines) + "\n"


# --- per-issue navigation footer ------------------------------------------

FOOTER_MARK = "**Part of:**"
FOOTER_LINE_RE = re.compile(r"^\*\*Part of:\*\*.*$", re.M)
# The trailing footer block: blank line(s), a rule, then the footer line. The
# block is repeatable, so a file that somehow carries two footers converges back
# to one instead of keeping the stale copy when the generator re-runs.
FOOTER_BLOCK_RE = re.compile(
    r"(?:\n+---\n+" + re.escape(FOOTER_MARK) + r"[^\n]*)+[ \t]*\n?\Z")


def render_footer(cats, doms) -> str:
    """Nav footer for an issue: category links, their domains, then SKILL.md."""
    parts = [category_link(c) for c in sorted(cats)]
    parts += [domain_link(d) for d in sorted(doms)]
    parts.append(SKILL_LINK)
    return f"---\n\n{FOOTER_MARK} " + " · ".join(parts) + "\n"


def footer_of(text: str) -> str | None:
    """The footer line of an issue file, or None if it has no footer."""
    m = FOOTER_LINE_RE.search(text)
    return m.group(0) if m else None


def footer_line(cats, doms) -> str:
    """The one-line form of the footer, for comparison against footer_of()."""
    return render_footer(cats, doms).splitlines()[-1]


def with_footer(text: str, cats, doms) -> str:
    """`text` with its trailing nav footer replaced by the current one.

    Idempotent: an existing footer (anything from the last `---`/`**Part of:**`
    block at EOF) is stripped first, so regeneration never stacks footers. The
    frontmatter block is left alone.
    """
    body = FOOTER_BLOCK_RE.sub("", text).rstrip()
    return f"{body}\n\n{render_footer(cats, doms)}"
