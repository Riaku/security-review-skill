#!/usr/bin/env python3
"""The whole gate: item format is valid, and no generated artifact is tracked.

``bundles/`` is generated on demand and gitignored: a reviewing agent generates
the categories it needs (or reads ``issues/`` directly), so the bundles do not
ship and there is nothing committed that can drift.

Three things can still go wrong, and this checks all three:

  1. An item's frontmatter is missing, malformed, unsorted, or names a category
     or domain with no file. The generator owns that check, so this runs it into
     a throw-away directory and surfaces its message verbatim.
  2. Someone committed a bundle. Generated files in git is what made installing
     this skill cost twice what it needs to; if ``bundles/`` reappears in the
     index, fail and name the files.
  3. Routing drifts: a category no quick-map reaches, a quick-map route no item
     backs, or new stranded (item, category) pairs past the ratchet cap.

Exit codes:
  0  items valid, no generated artifact tracked, routing coverage holds
  1  any condition above failed
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "gen_artifacts.py"
SKILL_FILE = ROOT / "SKILL.md"

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.S)
# An unquoted plain scalar cannot contain ': ' — YAML reads it as a nested
# mapping and the whole document fails to parse. This is the class of bug that
# made the skill uninstallable and invisible to a line-count check.
BAD_PLAIN_SCALAR_RE = re.compile(r"^\s*[A-Za-z_][\w-]*:[ \t]+[^\"'|>\s][^\"'|>]*: ")


def skill_frontmatter_problem() -> str | None:
    """Why SKILL.md's frontmatter would fail a real YAML parser, if it would."""
    match = FRONTMATTER_RE.match(SKILL_FILE.read_text(encoding="utf-8"))
    if match is None:
        return "SKILL.md does not open with a '---' frontmatter block"
    body = match.group("body")
    try:
        import yaml  # noqa: PLC0415 — optional: CI installs it, local may not
    except ImportError:
        for number, line in enumerate(body.splitlines(), start=1):
            if BAD_PLAIN_SCALAR_RE.match(line):
                return (f"frontmatter line {number} looks like an unquoted "
                        f"scalar containing ': ' — quote the value: "
                        f"{line.strip()[:70]}")
        return None
    try:
        parsed = yaml.safe_load(body)
    except Exception as exc:  # noqa: BLE001 — any parse error is a failure
        return f"frontmatter is not valid YAML: {exc}"
    if not isinstance(parsed, dict):
        return "frontmatter is not a YAML mapping"
    for field in ("name", "description"):
        if not str(parsed.get(field, "")).strip():
            return f"frontmatter has no '{field}' — the installer requires it"
    return None


def tracked(prefix: str) -> list[str]:
    """Paths tracked by git under `prefix` — should always be none for these."""
    try:
        result = subprocess.run(["git", "ls-files", "--", prefix],
                                cwd=ROOT, capture_output=True, text=True)
    except FileNotFoundError:
        print("note: git not available, skipped the tracked-artifact check")
        return []
    if result.returncode != 0:
        print("note: not a git checkout, skipped the tracked-artifact check")
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


# Neither a build product nor an installed copy belongs in the repository. An
# installer run inside the working tree leaves .agents/ and skills-lock.json
# behind, and `git add -A` will happily commit a second copy of the whole corpus.
UNTRACKED_PREFIXES = ("bundles", ".agents", "skills-lock.json")

# Routing coverage. Triage reaches an item like this: a domain's detection
# signals fire, the domain's stack quick-map names categories, and items
# declaring that (category, domain) pair load with the bundle. Three ways that
# breaks:
#
#   orphan category  no quick-map routes it, so triage can never load it
#   dead route       a quick-map names a category no item pairs with the domain
#   stranded pair    an item declares (category, domain) but none of its
#                    declared domains' quick-maps route that category
#
# Orphans and dead routes are hard failures. The stranded debt introduced with
# this check (36 pairs) was fully paid in the follow-up audit, so the cap is
# zero: any new stranded pair fails the gate outright. Never raise it to pass.
STRANDED_MAX = 0


def routing_coverage() -> tuple[list[str], int]:
    """(problems, stranded_count) for the domain -> quick-map -> category chain."""
    cats = {p.stem for p in (ROOT / "categories").glob("*.md")}
    routed: dict[str, set[str]] = {}
    for dom in (ROOT / "domains").glob("*.md"):
        section = dom.read_text(encoding="utf-8").split("## Stack quick-map")[-1]
        section = section.split("\n## ")[0]
        routed[dom.stem] = {t for t in re.findall(r"[a-z][a-z0-9-]+", section)
                            if t in cats}
    items = []
    for item in (ROOT / "issues").glob("*.md"):
        fm = FRONTMATTER_RE.match(item.read_text(encoding="utf-8"))
        if fm is None:  # the generator gate above already failed on this
            continue
        body = fm.group("body")
        lists = []
        for field in ("categories", "domains"):
            found = re.search(rf"{field}:\s*\[([^\]]*)\]", body)
            lists.append([t.strip() for t in found.group(1).split(",")
                          if t.strip()] if found else [])
        items.append((lists[0], lists[1]))
    problems: list[str] = []
    for cat in sorted(cats):
        if not any(cat in r for r in routed.values()):
            problems.append(f"orphan category: {cat} is routed by no quick-map")
    for dom in sorted(routed):
        for cat in sorted(routed[dom]):
            if not any(cat in cs and dom in ds for cs, ds in items):
                problems.append(f"dead route: {dom} routes {cat}, no item "
                                f"declares both")
    stranded = sum(1 for cs, ds in items for c in cs
                   if not any(c in routed.get(d, ()) for d in ds))
    if stranded > STRANDED_MAX:
        problems.append(
            f"stranded pairs grew to {stranded} (cap {STRANDED_MAX}): an item "
            "declares a category none of its domains' quick-maps route — add a "
            "quick-map line or fix the item's domains")
    return problems, stranded


def main() -> int:
    problem = skill_frontmatter_problem()
    if problem is not None:
        print("SKILL.md frontmatter would fail the installer's parser:")
        print(f"  {problem}")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--out", tmp],
            capture_output=True, text=True)
        if result.returncode != 0:
            # The generator is the format gate and its own message is the useful
            # one, so surface that instead of a CalledProcessError traceback.
            print("item validation failed — fix the item named below:")
            error = (result.stderr or result.stdout or "").strip()
            print(f"  {error}" if error else
                  f"  {GENERATOR.relative_to(ROOT)} exited {result.returncode}")
            return 1
        generated = result.stdout.strip()

    for prefix in UNTRACKED_PREFIXES:
        stray = tracked(prefix)
        if not stray:
            continue
        if prefix == "bundles":
            print("generated artifacts are tracked by git — bundles are built on "
                  "demand and must not be committed:")
            print("  fix: git rm -r --cached bundles")
        else:
            print(f"an installed copy is tracked by git — {prefix!r} comes from "
                  f"running an installer inside this working tree, not from "
                  f"authoring, and it duplicates the corpus:")
            print("  fix: git rm -r --cached .agents skills-lock.json")
        for name in stray[:5]:
            print(f"  {name}")
        if len(stray) > 5:
            print(f"  … {len(stray) - 5} more")
        return 1

    problems, stranded = routing_coverage()
    if problems:
        print("routing coverage check failed:")
        for problem in problems[:10]:
            print(f"  {problem}")
        if len(problems) > 10:
            print(f"  ... {len(problems) - 10} more")
        return 1

    print(f"items-valid: {generated}; no generated or installed artifacts "
          f"tracked; routing: 0 orphans, 0 dead routes, "
          f"{stranded}/{STRANDED_MAX} stranded-pair budget")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
