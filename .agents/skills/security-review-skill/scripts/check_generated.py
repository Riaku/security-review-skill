#!/usr/bin/env python3
"""The whole gate: item format is valid, and no generated artifact is tracked.

``bundles/`` is generated on demand and gitignored: a reviewing agent generates
the categories it needs (or reads ``issues/`` directly), so the bundles do not
ship and there is nothing committed that can drift.

Two things can still go wrong, and this checks both:

  1. An item's frontmatter is missing, malformed, unsorted, or names a category
     or domain with no file. The generator owns that check, so this runs it into
     a throw-away directory and surfaces its message verbatim.
  2. Someone committed a bundle. Generated files in git is what made installing
     this skill cost twice what it needs to; if ``bundles/`` reappears in the
     index, fail and name the files.

Exit codes:
  0  items valid and no generated artifact tracked
  1  either condition above failed
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

sys.path.insert(0, str(ROOT / "scripts"))
import category_slugs  # noqa: E402 — same directory, resolved via sys.path above

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


def tracked_bundles() -> list[str]:
    """Bundles that are tracked by git — should always be none."""
    try:
        result = subprocess.run(["git", "ls-files", "--", "bundles"],
                                cwd=ROOT, capture_output=True, text=True)
    except FileNotFoundError:
        print("note: git not available, skipped the tracked-bundle check")
        return []
    if result.returncode != 0:
        print("note: not a git checkout, skipped the tracked-bundle check")
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def membership_mismatches(bundles_dir: pathlib.Path) -> list[str]:
    """Categories where category_slugs.py and the generator disagree on membership.

    The Phase 3 coverage check trusts category_slugs.py, so its reading of the
    frontmatter has to match the generator's. If they drift, a sub-agent's complete
    return would be reported as missing slugs.
    """
    bad = []
    for path in sorted(bundles_dir.glob("*.md")):
        header = path.read_text(encoding="utf-8").splitlines()[0]
        match = re.search(r"\((\d+) items\)", header)
        if match is None:
            bad.append(f"{path.name}: header carries no item count")
            continue
        owned = category_slugs.owned_slugs(path.stem)
        if int(match.group(1)) != len(owned):
            bad.append(f"{path.stem}: bundle holds {match.group(1)} items, "
                       f"category_slugs.py owns {len(owned)}")
    return bad


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
        mismatches = membership_mismatches(pathlib.Path(tmp))

    if mismatches:
        print("category membership disagrees between the generator and "
              "category_slugs.py — the coverage check would lie:")
        for line in mismatches:
            print(f"  {line}")
        return 1

    tracked = tracked_bundles()
    if tracked:
        print("generated artifacts are tracked by git — bundles are built on "
              "demand and must not be committed:")
        for name in tracked:
            print(f"  {name}")
        print("  fix: git rm -r --cached bundles")
        return 1

    print(f"items-valid: {generated}; no generated artifacts tracked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
