#!/usr/bin/env python3
"""List the slugs a category owns, and check a sub-agent's return against them.

An item's frontmatter is the only membership record, and `gen_artifacts.read_item`
is the only reader of it, so this script and the generator cannot disagree about
who belongs where:

    python3 scripts/category_slugs.py web-api-security
    python3 scripts/category_slugs.py web-api-security --check findings.jsonl

``--check`` reads one finding object per line (JSONL, the sub-agent output
contract) and compares the slugs it reports with the slugs the category owns. A
partial return is the failure mode that matters: a sub-agent that reports 28 of
34 items produces a clean parse and a plausible report, and the six it dropped
would otherwise look reviewed.

Exit codes:
  0  every owned slug was reported (and --check was given)
  1  no such category, the category owns nothing, or slugs are missing
  2  the findings file has no parseable objects
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gen_artifacts import (CATEGORIES_DIR, ISSUES_DIR, BuildError, md_files,
                           read_item)


def owned_slugs(category: str) -> list[str]:
    """Every slug whose frontmatter `categories:` list names `category`."""
    slugs = []
    for path in md_files(ISSUES_DIR):
        try:
            meta, _ = read_item(path)
        except BuildError:
            # A malformed item is the gate's finding, not this script's; skip it
            # rather than fail a coverage check for an unrelated reason.
            continue
        if category in meta["categories"]:
            slugs.append(path.stem)
    return slugs


def reported_slugs(findings: pathlib.Path) -> set[str]:
    """Slugs from a JSONL findings file; tolerates prose and fences around it."""
    found: set[str] = set()
    for line in findings.read_text(encoding="utf-8").splitlines():
        line = line.strip().rstrip(",")
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        slug = obj.get("slug") if isinstance(obj, dict) else None
        if isinstance(slug, str) and slug.strip():
            found.add(slug.strip())
    return found


def main(argv: list[str]) -> int:
    if not argv or argv[0].startswith("-"):
        print("usage: category_slugs.py <category> [--check findings.jsonl]",
              file=sys.stderr)
        return 1
    category = argv[0]
    if not (CATEGORIES_DIR / f"{category}.md").exists():
        print(f"error: categories/{category}.md does not exist", file=sys.stderr)
        return 1
    owned = owned_slugs(category)
    if not owned:
        print(f"error: no item declares {category!r} — the manifest is orphaned",
              file=sys.stderr)
        return 1

    if "--check" not in argv:
        print("\n".join(owned))
        return 0

    try:
        findings = pathlib.Path(argv[argv.index("--check") + 1])
    except IndexError:
        print("error: --check needs a findings file", file=sys.stderr)
        return 1
    reported = reported_slugs(findings)
    if not reported:
        print(f"error: no parseable finding objects in {findings}", file=sys.stderr)
        return 2

    missing = [slug for slug in owned if slug not in reported]
    extra = sorted(reported - set(owned))
    print(f"{category}: {len(owned)} owned, {len(reported & set(owned))} reported, "
          f"{len(missing)} missing")
    for slug in missing:
        print(f"  MISSING  {slug}")
    for slug in extra:
        print(f"  UNKNOWN  {slug}  (not in {category})")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
