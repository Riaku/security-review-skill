#!/usr/bin/env python3
"""Crawl the skill's relative markdown link graph.

Every document in this repo cross-links its neighbours with relative markdown
links (issue <-> category <-> domain <-> SKILL.md), so the tree can be traversed
without consulting an index: follow the links. This module is that traversal —
a single, testable implementation shared by:

  gen_artifacts.py   assembles each bundle by *following* the links of its
                     category manifest (category -> issue link -> issue file)
  check_links.py     resolution, plus reachability/orphan detection from
                     SKILL.md and round-trip consistency of the graph

Link extraction masks fenced code blocks (``` / ~~~) and inline code spans
first, preserving string length and newlines, so link-looking text inside code
is never mistaken for a link and reported line numbers stay correct.

Crawl semantics:

- Start at SKILL.md (the only document that needs no inbound link).
- Follow every *relative* markdown link; external URLs, anchors and template
  placeholders are not edges (check_links.py handles the first, the checks in
  validate_skill.py the last).
- A link to a directory (`[`domains/`](domains/)`) expands to that directory's
  `*.md` files, sorted — that is what makes the directory links in SKILL.md
  reach all 35 categories, 9 domains, 7 references and 2 templates.
- A link to a non-markdown file (script, JSON) is a real target that must exist
  but is not a further crawl step.
- A link whose target does not exist is reported as broken and not followed.
"""
from __future__ import annotations

import pathlib
import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Iterable, Iterator, NamedTuple

ROOT = pathlib.Path(__file__).resolve().parent.parent

# --- link extraction -------------------------------------------------------

# `[label](target)` or `![alt](target)`. Both are confined to a single line and
# the target may not contain a ')' — that keeps the match to a real markdown
# inline link instead of running past the closing paren.
LINK_RE = re.compile(r'!?\[([^\]\n]*)\]\(([^)\n]*)\)')
# Optional title after the target: [label](../x.md "Title"). Stripped so the
# bare path is what gets resolved.
TITLE_RE = re.compile(r'^(.*?)\s+(?:"[^"]*"|\'[^\']*\'|\([^)]*\))\s*$')
# Opening OR closing fence: a line of >=3 backticks or tildes (info string ok).
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
# Any `scheme:` prefix (http:, https:, mailto:, data:, ...) — not a repo path.
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")


class Link(NamedTuple):
    """One relative link: where it was written, and what it points at."""
    source: pathlib.Path   # absolute path of the document containing it
    label: str             # link text, verbatim
    target: str            # target as written (fragment/query stripped)
    line: int              # 1-based line number in `source`
    path: pathlib.Path     # resolved absolute target (file or directory)


def mask_inline_code(line: str) -> str:
    """Blank out single-line inline code spans, preserving length.

    A span opens with a run of N backticks and closes with the next run of
    exactly N backticks on the same line; both are blanked (newlines kept).
    """
    chars = list(line)
    n = len(line)
    i = 0
    while i < n:
        if line[i] != "`":
            i += 1
            continue
        j = i
        while j < n and line[j] == "`":
            j += 1
        run_len = j - i
        k, end = j, -1
        while k < n:
            if line[k] == "`":
                m = k
                while m < n and line[m] == "`":
                    m += 1
                if m - k == run_len:
                    end = m
                    break
                k = m
            else:
                k += 1
        if end != -1:
            for x in range(i, end):
                if chars[x] != "\n":
                    chars[x] = " "
            i = end
        else:
            i = j
    return "".join(chars)


def mask_code(text: str) -> str:
    """Blank out fenced code blocks and inline code spans in `text`.

    Returns a same-length string with matched characters replaced by spaces and
    every newline preserved, so offsets (and thus line numbers) computed
    against the original text remain valid.
    """
    chars = list(text)
    pos = 0
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in text.splitlines(keepends=True):
        m = FENCE_RE.match(line)
        blank = in_fence
        if m:
            run = m.group(1)
            if not in_fence:
                in_fence, fence_char, fence_len = True, run[0], len(run)
                blank = True
            elif run[0] == fence_char and len(run) >= fence_len:
                in_fence, blank = False, True
        if blank:
            for x in range(pos, pos + len(line)):
                if chars[x] != "\n":
                    chars[x] = " "
        pos += len(line)
    masked = "".join(chars)
    return "".join(mask_inline_code(ln) for ln in masked.splitlines(keepends=True))


def classify_target(target: str) -> tuple[str | None, str | None]:
    """Decide whether `target` is a repo-relative path worth resolving.

    Returns ``(path, None)`` for a relative target (fragment/query stripped,
    URL-decoded), or ``(None, reason)`` when the target is not one — empty,
    anchor-only, absolute, a `scheme:` URL, or a `{`/`<` template placeholder.
    """
    t = target.strip()
    if not t:
        return None, "empty"
    if "{" in t or "<" in t:
        return None, "placeholder"
    if t.startswith("#"):
        return None, "anchor"
    if t.startswith("/"):
        return None, "absolute"
    if SCHEME_RE.match(t):
        return None, "scheme"
    path = t.split("#", 1)[0].split("?", 1)[0]
    path = urllib.parse.unquote(path)
    if not path:
        return None, "anchor"
    return path, None


def iter_links(source: pathlib.Path, text: str | None = None) -> Iterator[Link]:
    """Yield every *relative* markdown link in `source` (in file order)."""
    if text is None:
        text = source.read_text(encoding="utf-8", errors="ignore")
    masked = mask_code(text)
    for m in LINK_RE.finditer(masked):
        raw = m.group(2).strip()
        tm = TITLE_RE.match(raw)
        if tm:
            raw = tm.group(1).strip()
        rel, reason = classify_target(raw)
        if reason is not None:
            continue
        assert rel is not None
        line = text.count("\n", 0, m.start()) + 1
        yield Link(source, m.group(1), rel, line, (source.parent / rel).resolve())


def resolve(source: pathlib.Path, target: str) -> pathlib.Path:
    """Absolute path a relative link target points at, from `source`'s dir."""
    rel, reason = classify_target(target)
    if reason is not None or rel is None:
        raise ValueError(f"not a relative target: {target!r} ({reason})")
    return (source.parent / rel).resolve()


def kind_of(path: pathlib.Path) -> str:
    """'doc' (*.md), 'dir', or 'asset' (anything else) — how a crawl treats it."""
    if path.is_dir():
        return "dir"
    if path.suffix == ".md":
        return "doc"
    return "asset"


def docs_in(directory: pathlib.Path) -> list[pathlib.Path]:
    """sorted *.md files directly inside `directory` (the dir-link expansion)."""
    return sorted(p for p in directory.glob("*.md") if p.is_file())


# --- the crawl -------------------------------------------------------------

@dataclass
class Crawl:
    """Result of following the graph from `start`."""
    start: pathlib.Path
    root: pathlib.Path
    edges: dict[pathlib.Path, list[Link]] = field(default_factory=dict)
    docs: list[pathlib.Path] = field(default_factory=list)      # visit order
    broken: list[Link] = field(default_factory=list)
    dirs: list[pathlib.Path] = field(default_factory=list)
    assets: list[pathlib.Path] = field(default_factory=list)

    @property
    def reached(self) -> set[pathlib.Path]:
        return set(self.docs)

    def all_docs(self) -> set[pathlib.Path]:
        """Every *.md in the repo (the denominator for orphan detection)."""
        return {p.resolve() for p in self.root.rglob("*.md")
                if ".git" not in p.parts}

    def orphans(self, exempt: Iterable[str] = ()) -> list[pathlib.Path]:
        """Markdown documents no crawl path reaches, minus `exempt` names.

        `exempt` is a list of paths relative to the repo root (POSIX form), e.g.
        the root-level SKILL.md/AGENTS.md/SOURCES.md that are entry points or
        agent-managed rather than crawl targets.
        """
        skip = {(self.root / e).resolve() for e in exempt}
        return sorted(self.all_docs() - self.reached - skip)

    def inbound(self, path: pathlib.Path) -> list[Link]:
        """Links from anywhere in the crawl that point at `path`."""
        path = path.resolve()
        return [ln for links in self.edges.values() for ln in links
                if ln.path == path]


def crawl(start: pathlib.Path | None = None,
          root: pathlib.Path | None = None) -> Crawl:
    """Breadth-first crawl of the relative link graph from `start`."""
    start = (start or (ROOT / "SKILL.md")).resolve()
    root = (root or ROOT).resolve()
    c = Crawl(start=start, root=root)
    queue: list[pathlib.Path] = [start]
    seen: set[pathlib.Path] = set()
    while queue:
        doc = queue.pop(0)
        if doc in seen:
            continue
        seen.add(doc)
        c.docs.append(doc)
        links = list(iter_links(doc))
        c.edges[doc] = links
        for ln in links:
            if not ln.path.exists():
                c.broken.append(ln)
                continue
            kind = kind_of(ln.path)
            if kind == "doc":
                queue.append(ln.path)
            elif kind == "dir":
                sub = docs_in(ln.path)
                if ln.path not in c.dirs:
                    c.dirs.append(ln.path)
                queue.extend(sub)
            elif ln.path not in c.assets:
                c.assets.append(ln.path)
    return c


# --- link-form manifest readers (follow the links a manifest lists) --------

def _manifest_links(manifest: pathlib.Path, into: str) -> list[str]:
    """Link labels a manifest lists for targets inside `<root>/<into>/`.

    Deduped, first occurrence wins — a domain's stack quick-map re-links the
    same categories its list already names. Enforces the canonical form: the
    link label must equal the target's file stem
    (`- [slug](../issues/slug.md)`), so a half-rewritten line is rejected
    rather than silently accepted as an entry.
    """
    out: list[str] = []
    for ln in iter_links(manifest):
        parent = (ROOT / into).resolve()
        if ln.path.parent == parent and ln.path.suffix == ".md":
            if ln.label != ln.path.stem:
                raise ValueError(
                    f"{manifest.name}:{ln.line}: link label {ln.label!r} != "
                    f"target stem {ln.path.stem!r} (expected "
                    f"- [{ln.path.stem}](../{into}/{ln.path.stem}.md))")
            if ln.path.stem not in out:
                out.append(ln.path.stem)
    return out


def issue_slugs(manifest: pathlib.Path) -> list[str]:
    """Issue slugs a categories/*.md manifest links to, in manifest order."""
    return _manifest_links(manifest, "issues")


def category_names(manifest: pathlib.Path) -> list[str]:
    """Category names a domains/*.md manifest links to, in manifest order."""
    return _manifest_links(manifest, "categories")
