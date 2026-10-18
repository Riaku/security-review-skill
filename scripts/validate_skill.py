#!/usr/bin/env python3
"""Validate the security-review-skill tree.

Checks (hard-fail each with a per-item message):
  1. SKILL.md exists; frontmatter starts at byte 0 with '---', closes with
     '---', has name == 'security-review-skill' and non-empty description <= 1024.
  2. Every issues/*.md opens with a well-formed frontmatter block declaring
     `categories:` and `domains:` — sorted, duplicate-free slugs naming real
     manifests (parsed by scripts/manifest_links.py::item_meta).
  3. Every issue file is listed in >=1 categories/*.md manifest.
  4. Every slug in a category manifest has an issues/<slug>.md file.
  5. Every issue body (frontmatter stripped): H1 title; a bolded BCP 14 keyword
     within its first 300 characters; a '**References:**' line.
  6. Every category listed in a domain manifest exists in categories/; every
     category file appears in >=1 domain manifest.
  7. Membership agrees both ways. A category manifest's '## Issues' list is
     exactly the items whose frontmatter names it, and a domain manifest's
     '## Categories' list is exactly the categories whose items name that
     domain. Those lists are generated from the frontmatter, so a disagreement
     means the generator has not been re-run (python3 scripts/gen_artifacts.py).
  8. Every issue's nav footer appears exactly once and lists exactly the
     categories and domains its frontmatter declares.
  9. SKILL.md's Category Index table agrees with the domain manifests and its
     cells link to categories/<cat>.md and domains/<domain>.md.
 10. No data files: the corpus is markdown plus issue frontmatter, so a *.json
     or *.csv anywhere in the tree fails the build.

Manifest entries are relative markdown links (see scripts/manifest_links.py):
`- [slug](../issues/slug.md)` in categories/*.md, `- [cat](../categories/cat.md)`
in domains/*.md. A malformed line is invisible to these checks — that is what
check_links.py and check_generated.py are for.

--allow-missing: skip checks 3 and 7 (incremental authoring, before the
generator has been re-run).
Exit 0 with 'OK: N issues, C categories, D domains' on success.
"""
import pathlib
import re
import sys

import manifest_links as ml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
CAT_DIR = ROOT / "categories"
DOM_DIR = ROOT / "domains"
ISSUE_DIR = ROOT / "issues"
BCP14 = ("**MUST**", "**MUST NOT**", "**SHOULD**", "**SHOULD NOT**", "**MAY**")
DATA_SUFFIXES = (".json", ".csv", ".tsv")

# SKILL.md's Category Index: | [category](categories/category.md) | [domain](domains/domain.md) |
TABLE_ROW_RE = re.compile(r"^\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$", re.M)
TABLE_LINK_RE = re.compile(
    r"^\[([a-z0-9][a-z0-9-]*)\]\(\.{0,2}/?(categories|domains)/([a-z0-9][a-z0-9-]*)/?\.md\)$")

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
            fm[key] = "" if val in (">-", ">", "|", "|-") else val.strip("\"'")
        elif key and line.startswith("  "):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm


def manifest_slugs(path: pathlib.Path):
    """Issue slugs (link labels) listed in a categories/*.md manifest."""
    return ml.manifest_items(path, ml.CAT_ITEM_RE)


def domain_cats(path: pathlib.Path):
    """Category names (link labels) listed in a domains/*.md manifest."""
    return ml.manifest_items(path, ml.DOMAIN_ITEM_RE)


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

    cat_files = sorted(CAT_DIR.glob("*.md")) if CAT_DIR.is_dir() else []
    dom_files = sorted(DOM_DIR.glob("*.md")) if DOM_DIR.is_dir() else []
    issue_files = sorted(ISSUE_DIR.glob("*.md")) if ISSUE_DIR.is_dir() else []
    cat_names = {f.stem for f in cat_files}
    dom_names = {f.stem for f in dom_files}

    # 2. issue frontmatter: the single declaration of membership
    meta: dict[str, dict[str, list[str]]] = {}
    for f in issue_files:
        try:
            meta[f.stem] = ml.item_meta(f.read_text())
        except ValueError as exc:
            err(f"{f.name}: bad frontmatter — {exc}")
            continue
        for cat in meta[f.stem]["categories"]:
            if cat not in cat_names:
                err(f"{f.name}: frontmatter names unknown category {cat!r} "
                    f"(no categories/{cat}.md)")
        for dom in meta[f.stem]["domains"]:
            if dom not in dom_names:
                err(f"{f.name}: frontmatter names unknown domain {dom!r} "
                    f"(no domains/{dom}.md)")

    # per-manifest lists, in file order (order is part of the agreement check)
    cat_slugs = {f.stem: manifest_slugs(f) for f in cat_files}
    dom_cats = {f.stem: domain_cats(f) for f in dom_files}

    # the generated tails must be there at all
    for f in cat_files:
        if ml.tail_of(f.read_text(), ml.CAT_TAIL_HEAD) is None:
            err(f"categories/{f.name}: no '{ml.CAT_TAIL_HEAD}' tail "
                "(run python3 scripts/gen_artifacts.py)")
    for f in dom_files:
        if ml.tail_of(f.read_text(), ml.DOM_TAIL_HEAD) is None:
            err(f"domains/{f.name}: no '{ml.DOM_TAIL_HEAD}' tail "
                "(run python3 scripts/gen_artifacts.py)")

    # 3. every issue file in >=1 category manifest
    listed = set().union(*(set(v) for v in cat_slugs.values())) if cat_slugs else set()
    if not allow_missing:
        for f in issue_files:
            if f.stem not in listed:
                err(f"issue not referenced by any category manifest: {f.name}")

    # 4. manifest slugs exist on disk
    for cat, slugs in cat_slugs.items():
        for s in slugs:
            if not (ISSUE_DIR / f"{s}.md").exists():
                err(f"{cat}: slug has no issue file: {s}")

    # 5. issue file content (body only — frontmatter is checked in 2)
    for f in issue_files:
        body = ml.strip_meta(f.read_text())
        if not body.startswith("# "):
            err(f"{f.name}: body must start with '# ' H1 title")
        if not any(k in body[:300] for k in BCP14):
            err(f"{f.name}: no bolded BCP 14 keyword in first 300 chars of body")
        if "**References:**" not in body:
            err(f"{f.name}: missing '**References:**' line")

    # 6. domain <-> category wiring
    for dom, cats in dom_cats.items():
        for c in cats:
            if c not in cat_names:
                err(f"domain {dom}: category manifest missing: categories/{c}.md")
    dom_union = set().union(*(set(v) for v in dom_cats.values())) if dom_cats else set()
    for c in sorted(cat_names - dom_union):
        err(f"category not assigned to any domain: {c}")

    # 7. membership agrees with the frontmatter, both ways
    if not allow_missing:
        for cat in sorted(cat_names):
            want = sorted(s for s, m in meta.items() if cat in m["categories"])
            have = cat_slugs[cat]
            if have != want:
                extra = sorted(set(have) - set(want))
                missing = sorted(set(want) - set(have))
                err(f"categories/{cat}.md: list disagrees with the items' "
                    f"frontmatter — it lists {extra} that do not name it and "
                    f"omits {missing} that do "
                    "(run python3 scripts/gen_artifacts.py)")
        for dom in sorted(dom_names):
            want = sorted(c for c in cat_names
                          if any(dom in meta[s]["domains"]
                                 for s, m in meta.items() if c in m["categories"]))
            have = dom_cats[dom]
            if have != want:
                extra = sorted(set(have) - set(want))
                missing = sorted(set(want) - set(have))
                err(f"domains/{dom}.md: list disagrees with the items' "
                    f"frontmatter — it lists {extra} no item claims and omits "
                    f"{missing} that items claim "
                    "(run python3 scripts/gen_artifacts.py)")

    # 8. nav footer per issue: present exactly once, exactly this item's
    #    categories and domains (gen_artifacts.py writes it).
    for f in issue_files:
        m = meta.get(f.stem)
        if m is None:
            continue
        text = f.read_text()
        got = ml.footer_of(text)
        want = ml.footer_line(m["categories"], m["domains"])
        n_footers = text.count(ml.FOOTER_MARK)
        if got is None:
            err(f"{f.name}: missing nav footer "
                "(run python3 scripts/gen_artifacts.py)")
        elif n_footers != 1:
            err(f"{f.name}: {n_footers} nav footers (want exactly 1) "
                "(run python3 scripts/gen_artifacts.py)")
        elif got.strip() != want:
            err(f"{f.name}: nav footer out of date "
                "(run python3 scripts/gen_artifacts.py)\n"
                f"      have: {got.strip()}\n      want: {want}")

    # 9. SKILL.md Category Index mirrors the domain manifests; every cell is a
    #    relative link to categories/<cat>.md / domains/<domain>.md.
    table_rows = []
    for row in TABLE_ROW_RE.finditer(SKILL.read_text() if SKILL.exists() else ""):
        left, right = row.groups()
        if not left.startswith("[") or not right.startswith("["):
            continue  # header row or separator
        table_rows.append((left, right))
    expected: dict[str, set[str]] = {}
    for dom, cats in dom_cats.items():
        for c in cats:
            expected.setdefault(c, set()).add(dom)
    seen = {}
    for left, right in table_rows:
        cat_m, dom_m = TABLE_LINK_RE.match(left), TABLE_LINK_RE.match(right)
        if not cat_m or not dom_m:
            err("SKILL.md Category Index row is not a pair of relative links "
                f"to categories/ and domains/: {left} | {right}")
            continue
        cat, cat_kind, cat_target = cat_m.group(1), cat_m.group(2), cat_m.group(3)
        dom, dom_kind, dom_target = dom_m.group(1), dom_m.group(2), dom_m.group(3)
        if cat_kind != "categories" or cat != cat_target:
            err(f"SKILL.md Category Index: category cell must link to "
                f"categories/{cat}.md, got {left}")
        if dom_kind != "domains" or dom != dom_target:
            err(f"SKILL.md Category Index: domain cell must link to "
                f"domains/{dom}.md, got {right}")
        if cat in seen:
            err(f"SKILL.md Category Index lists {cat} twice")
        seen[cat] = dom
    for cat, dom in sorted(seen.items()):
        if dom not in expected.get(cat, set()):
            have = sorted(expected.get(cat, [])) or ["<assigned to no domain>"]
            err(f"SKILL.md Category Index: {cat} -> {dom}, "
                f"domain manifests say {have}")
    for cat in sorted(set(expected) - set(seen)):
        err(f"SKILL.md Category Index is missing: {cat}")
    for cat in sorted(set(seen) - set(expected)):
        err(f"SKILL.md Category Index lists unknown category: {cat}")
    if not table_rows:
        err("SKILL.md Category Index table not found or not linkified")

    # 10. no data files: markdown plus issue frontmatter, nothing machine-readable
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or ".git" in p.relative_to(ROOT).parts:
            continue
        if p.suffix in DATA_SUFFIXES:
            err(f"data file in the corpus: {p.relative_to(ROOT)} "
                "(membership is declared in each issue's frontmatter)")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"\n{len(errors)} error(s)")
        return 1
    print(f"OK: {len(issue_files)} issues, {len(cat_names)} categories, "
          f"{len(dom_files)} domains")
    return 0


if __name__ == "__main__":
    sys.exit(main())
