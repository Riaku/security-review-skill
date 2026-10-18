#!/usr/bin/env python3
"""Generate every bundle from the items' frontmatter.

An item declares where it belongs in its own YAML frontmatter:

    issues/<slug>.md
        ---
        categories: [a, b]
        domains: [c]
        ---

        # Title
        ...authored body...

``bundles/<category>.md`` is the only generated artifact in this repository: a
header (title, item count, the category manifest's overview line, an
attribution line), then the body of every item whose frontmatter names that
category, in slug order. Nothing is written into ``issues/``, ``categories/``
or ``domains/`` — those documents are authored end to end, and the footers and
item lists that used to be generated into them are gone.

This script is also the format gate. It refuses to write anything, exiting 1
with the offending file named, when:

  - an item has no frontmatter, or one that does not parse, or that is missing
    ``categories:`` or ``domains:``
  - a frontmatter list is empty, repeats a name, or is not sorted
  - an item names a category or domain with no file in ``categories/`` or
    ``domains/``
  - an item body does not open with an H1 title
  - a category manifest has no overview line, or no item declares it
  - ``SKILL.md`` is missing

Generation is deterministic: a second run rewrites byte-identical files.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_FILE = ROOT / "SKILL.md"
ISSUES_DIR = ROOT / "issues"
CATEGORIES_DIR = ROOT / "categories"
DOMAINS_DIR = ROOT / "domains"
BUNDLES_DIR = ROOT / "bundles"

LIST_LINE_RE = re.compile(r"^(categories|domains):\s*\[(?P<names>.*?)\]\s*$")
META_BLOCK_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n(?P<rest>.*)\Z", re.S)
FOOTER_RE = re.compile(r"\n*-{3,}\n+\*\*Part of:\*\*[^\n]*\n*\Z", re.S)


class BuildError(Exception):
    """A condition this script refuses to generate through (exit 1)."""


def _rel(path: pathlib.Path) -> str:
    return str(path.relative_to(ROOT))


def _md_files(directory: pathlib.Path) -> list[pathlib.Path]:
    """Sorted ``*.md`` files directly inside `directory`."""
    return sorted(p for p in directory.glob("*.md") if p.is_file())


def read_item(path: pathlib.Path) -> tuple[dict[str, list[str]], str]:
    """``(frontmatter, body)`` for one item file; raises BuildError if malformed."""
    text = path.read_text(encoding="utf-8")
    match = META_BLOCK_RE.match(text)
    if match is None:
        raise BuildError(
            f"{_rel(path)}: no YAML frontmatter — every item must open with a "
            f"'---' block declaring 'categories:' and 'domains:'")
    meta: dict[str, list[str]] = {}
    for line in match.group("body").splitlines():
        if not line.strip():
            continue
        line_match = LIST_LINE_RE.match(line)
        if line_match is None:
            raise BuildError(
                f"{_rel(path)}: frontmatter line {line.strip()!r} is neither "
                f"'categories: [...]' nor 'domains: [...]'")
        key = line_match.group(1)
        names = [n.strip() for n in line_match.group("names").split(",") if n.strip()]
        if not names:
            raise BuildError(f"{_rel(path)}: '{key}:' lists nothing")
        if len(set(names)) != len(names):
            raise BuildError(f"{_rel(path)}: '{key}:' repeats a name — {names}")
        if names != sorted(names):
            raise BuildError(f"{_rel(path)}: '{key}:' is not sorted — {names}")
        meta[key] = names
    for key in ("categories", "domains"):
        if key not in meta:
            raise BuildError(f"{_rel(path)}: frontmatter is missing '{key}:'")
    body = FOOTER_RE.sub("", match.group("rest")).strip("\n")
    if not body.startswith("# "):
        raise BuildError(f"{_rel(path)}: body does not open with an H1 title")
    return meta, body


def overview_of(path: pathlib.Path) -> str:
    """The authored overview line under a category manifest's H1."""
    seen_h1 = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if not seen_h1:
            seen_h1 = line.startswith("# ")
            continue
        if line.strip():
            return line.strip()
    raise BuildError(
        f"{_rel(path)}: no overview line under the H1 — every category manifest "
        f"needs one, and each bundle quotes it")


def main() -> int:
    if not SKILL_FILE.exists():
        raise BuildError("SKILL.md not found at the repo root")

    manifests = {p.stem: p for p in _md_files(CATEGORIES_DIR)}
    known_doms = {p.stem for p in _md_files(DOMAINS_DIR)}

    items: dict[str, tuple[dict[str, list[str]], str]] = {}
    for path in _md_files(ISSUES_DIR):
        meta, body = read_item(path)
        for cat in meta["categories"]:
            if cat not in manifests:
                raise BuildError(
                    f"{_rel(path)}: names category {cat!r}, but "
                    f"categories/{cat}.md does not exist")
        for dom in meta["domains"]:
            if dom not in known_doms:
                raise BuildError(
                    f"{_rel(path)}: names domain {dom!r}, but "
                    f"domains/{dom}.md does not exist")
        items[path.stem] = (meta, body)

    by_cat: dict[str, list[str]] = {cat: [] for cat in manifests}
    for slug, (meta, _) in items.items():
        for cat in meta["categories"]:
            by_cat[cat].append(slug)

    BUNDLES_DIR.mkdir(exist_ok=True)
    for cat in sorted(manifests):
        slugs = sorted(by_cat[cat])
        if not slugs:
            raise BuildError(
                f"categories/{cat}.md exists but no item declares it — name the "
                f"category in an item's frontmatter, or delete the manifest")
        parts = [f"# {cat} — full checklist ({len(slugs)} items)", "",
                 overview_of(manifests[cat]), "",
                 "> Generated artifact — edit the issue files, not this one. "
                 f"Manifest: [categories/{cat}.md](../categories/{cat}.md) · "
                 f"Index: [SKILL.md](../SKILL.md)", ""]
        for slug in slugs:
            parts += [items[slug][1], ""]
        (BUNDLES_DIR / f"{cat}.md").write_text("\n".join(parts) + "\n",
                                              encoding="utf-8")

    print(f"wrote {len(manifests)} bundles from {len(items)} items "
          f"({len(manifests)} categories, {len(known_doms)} domains)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
