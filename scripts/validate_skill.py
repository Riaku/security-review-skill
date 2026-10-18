#!/usr/bin/env python3
"""Validate the security-review-skill tree.

Checks (hard-fail each with a per-item message):
  1. SKILL.md exists; frontmatter starts at byte 0 with '---', closes with
     '---', has name == 'security-review-skill' and non-empty description <= 1024.
  2. Every topics.json slug has issues/<slug>.md.
  3. Every issues/*.md file is listed in >=1 category manifest.
  4. Every slug in a category manifest exists in topics.json and on disk.
  5. Every issue file: H1 title; a bolded BCP 14 keyword within the first 300
     chars; a '**References:**' line.
  6. Every category listed in a domain manifest exists in categories/; every
     category file appears in >=1 domain.
  7. Coverage: union of category manifests == all topics.json slugs.

--allow-missing: skip checks 2 and 7 (for incremental authoring).
Exit 0 with 'OK: N issues, C categories, D domains' on success.
"""
import json
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
TOPICS = ROOT / "scripts" / "topics.json"
CAT_DIR = ROOT / "categories"
DOM_DIR = ROOT / "domains"
ISSUE_DIR = ROOT / "issues"
BCP14 = ("**MUST**", "**MUST NOT**", "**SHOULD**", "**SHOULD NOT**", "**MAY**")
SLUG_RE = re.compile(r"^- `([a-z0-9][a-z0-9-]*)`\s*$", re.M)

errors = []


def err(msg: str) -> None:
    errors.append(msg)


def frontmatter(text: str):
    if not text.startswith("---"):
        err("SKILL.md: frontmatter must start at byte 0 with '---'")
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        err("SKILL.md: unterminated frontmatter")
        return {}
    fm = {}
    key = None
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            fm[key] = "" if val in (">-", ">", "|", "|-") else val.strip('"\'')
        elif key and line.startswith("  "):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm


def manifest_slugs(path: pathlib.Path):
    return SLUG_RE.findall(path.read_text())


def main() -> int:
    allow_missing = "--allow-missing" in sys.argv

    # 1. SKILL.md frontmatter
    if not SKILL.exists():
        err("SKILL.md missing")
    else:
        fm = frontmatter(SKILL.read_text())
        if fm.get("name") != "security-review-skill":
            err(f"SKILL.md name must be 'security-review-skill', got {fm.get('name')!r}")
        desc = fm.get("description", "")
        if not desc:
            err("SKILL.md description missing")
        elif len(desc) > 1024:
            err(f"SKILL.md description {len(desc)} chars > 1024")

    topics = json.loads(TOPICS.read_text()) if TOPICS.exists() else []
    topic_slugs = {t["slug"] for t in topics}
    cat_files = sorted(CAT_DIR.glob("*.md")) if CAT_DIR.is_dir() else []
    dom_files = sorted(DOM_DIR.glob("*.md")) if DOM_DIR.is_dir() else []
    issue_files = sorted(ISSUE_DIR.glob("*.md")) if ISSUE_DIR.is_dir() else []

    cat_slugs = {f.stem: set(manifest_slugs(f)) for f in cat_files}

    # 2. every topic has an issue file
    if not allow_missing:
        for s in sorted(topic_slugs):
            if not (ISSUE_DIR / f"{s}.md").exists():
                err(f"missing issue file: issues/{s}.md")

    # 3. every issue file in >=1 category manifest
    listed = set().union(*cat_slugs.values()) if cat_slugs else set()
    for f in issue_files:
        if f.stem not in listed:
            err(f"issue not referenced by any category manifest: {f.name}")

    # 4. manifest slugs exist in topics.json and on disk
    for cat, slugs in cat_slugs.items():
        for s in sorted(slugs):
            if topic_slugs and s not in topic_slugs:
                err(f"{cat}: slug not in topics.json: {s}")
            if not (ISSUE_DIR / f"{s}.md").exists():
                err(f"{cat}: slug has no issue file: {s}")

    # 5. issue file content
    for f in issue_files:
        text = f.read_text()
        if not text.startswith("# "):
            err(f"{f.name}: must start with '# ' H1 title")
        if not any(k in text[:300] for k in BCP14):
            err(f"{f.name}: no bolded BCP 14 keyword in first 300 chars")
        if "**References:**" not in text:
            err(f"{f.name}: missing '**References:**' line")

    # 6. domain <-> category wiring
    dom_cats = {f.stem: set(manifest_slugs(f)) for f in dom_files}
    cat_names = {f.stem for f in cat_files}
    for dom, cats in dom_cats.items():
        for c in sorted(cats):
            if c not in cat_names:
                err(f"domain {dom}: category manifest missing: categories/{c}.md")
    dom_union = set().union(*dom_cats.values()) if dom_cats else set()
    for c in sorted(cat_names - dom_union):
        err(f"category not assigned to any domain: {c}")

    # 7. full coverage
    if not allow_missing and topic_slugs:
        missing = topic_slugs - listed
        extra = listed - topic_slugs
        if missing:
            err(f"topics with no category: {sorted(missing)}")
        if extra:
            err(f"categories list unknown slugs: {sorted(extra)}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"\n{len(errors)} error(s)")
        return 1
    print(f"OK: {len(topic_slugs)} issues, {len(cat_names)} categories, "
          f"{len(dom_files)} domains")
    return 0


if __name__ == "__main__":
    sys.exit(main())
