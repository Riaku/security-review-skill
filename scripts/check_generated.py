#!/usr/bin/env python3
"""Check that the tree's generated regions match what the generator produces.

Runs scripts/gen_artifacts.py, then fails if any generated region changed. The
generated regions are exactly:

  bundles/*.md      the whole file (every item of one category, inlined)
  categories/*.md   the tail — ml.CAT_TAIL_HEAD ("## Issues") to EOF
  domains/*.md      the tail — ml.DOM_TAIL_HEAD ("## Categories") to EOF
  issues/*.md       the trailing "---" + "**Part of:**" nav footer block (EOF)

Everything above a manifest's tail is hand-authored, and an issue's frontmatter
and body are the author's, so this script neither compares nor rewrites them:
editing an issue's prose, a scope line, detection signals or a stack quick-map
is not drift and is never reported. What it does catch is a generated region
left behind by a change the generator was not re-run for — an item refiled into
another category, a bundle assembled from an older manifest, a stale nav
footer, or a generated file that was never committed.

The region vocabulary lives in scripts/manifest_links.py (the tail headings,
the tail extractor, the EOF-anchored footer block); this module imports it
instead of re-deriving the boundaries.

Exit codes:
  0  every generated region matches the generator's output
  1  at least one region drifted, or the generator itself failed

Drifting files are listed with a short before/after diff. Run before
committing; CI enforces it.
"""
import difflib
import pathlib
import subprocess
import sys

import manifest_links as ml

ROOT = pathlib.Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "gen_artifacts.py"

# Every directory whose *.md files carry a generated region. A generated
# directory missing from this list is silently unchecked, so it is the one
# place to add a new artifact kind.
GENERATED_DIRS = ("bundles", "categories", "domains", "issues")

# Cap on the unified-diff lines printed per drifting file.
DIFF_LINES = 12


def generated_region(path: pathlib.Path, text: str) -> str | None:
    """The generated region of `text`, or None if it carries none.

    Delegates every boundary to manifest_links: the whole file for a bundle,
    the heading-to-EOF tail for a manifest, the EOF-anchored footer block for an
    issue. None means "this file has no such region yet", which compares unequal
    to a region the generator has just written — that is drift too.
    """
    d = path.parent.name
    if d == "categories":
        return ml.tail_of(text, ml.CAT_TAIL_HEAD)
    if d == "domains":
        return ml.tail_of(text, ml.DOM_TAIL_HEAD)
    if d == "issues":
        match = ml.FOOTER_BLOCK_RE.search(text)
        return match.group(0) if match else None
    # bundles/*, and anything whole-file added later: compare conservatively
    # rather than silently narrowing the check to a region.
    return text


def region_label(path: pathlib.Path) -> str:
    """How `path`'s generated region is named in the drift report."""
    d = path.parent.name
    if d == "categories":
        return f"tail from '{ml.CAT_TAIL_HEAD}'"
    if d == "domains":
        return f"tail from '{ml.DOM_TAIL_HEAD}'"
    if d == "issues":
        return "nav footer only, item body and frontmatter untouched"
    return "whole file"


def diff_of(before: str | None, after: str | None) -> list[str]:
    """Indented unified-diff lines between the on-disk and generated regions."""
    lines = list(difflib.unified_diff(
        (before or "").splitlines(), (after or "").splitlines(),
        fromfile="on disk", tofile="generated", lineterm="", n=1))[2:]
    if len(lines) > DIFF_LINES:
        lines = lines[:DIFF_LINES] + [
            f"... {len(lines) - DIFF_LINES} more diff line(s)"]
    return [f"    {line}" for line in lines]


def generated_paths() -> list[pathlib.Path]:
    """Every *.md file under the generated directories, sorted."""
    return sorted(p for d in GENERATED_DIRS for p in (ROOT / d).glob("*.md"))


def main() -> int:
    paths = generated_paths()
    before = {p: generated_region(p, p.read_text()) for p in paths}

    subprocess.run([sys.executable, str(GENERATOR)],
                   check=True, stdout=subprocess.DEVNULL)

    drifted = []
    for p in paths:
        after = generated_region(p, p.read_text())
        if after != before[p]:
            drifted.append((p, before[p], after))
    # A generated file the generator just created has no snapshot to compare
    # against — report it as drift rather than letting it ride in uncommitted.
    created = [p for p in generated_paths() if p not in before]

    if not drifted and not created:
        print(f"generated-in-sync: {len(paths)} files OK")
        return 0

    print(f"DRIFT: generated regions are stale — re-run "
          f"`python3 scripts/{GENERATOR.name}` and commit:")
    for p, was, now in drifted:
        print(f"  {p.relative_to(ROOT)}  ({region_label(p)})")
        for line in diff_of(was, now):
            print(line)
    for p in created:
        print(f"  {p.relative_to(ROOT)}  (new generated file, not committed)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
