#!/usr/bin/env python3
"""Link checker for the skill repo — it walks *two* independent link graphs.

  1. External links (`http`/`https`). Every http(s) URL found in a ``*.md``
     file is fetched (HEAD, then GET on 403/405/501) and reported when it does
     not resolve. This is the network graph: it needs the internet, so it is
     skipped entirely under ``--offline``. Placeholder/example URLs are skipped
     by pattern because they document attack targets rather than real
     references. A 403/429 is treated as WAF bot-blocking (WARN), not link rot.

  2. The repo's own *relative* link graph. Every markdown link ``[label](t)``
     or image ``![alt](t)`` whose target ``t`` is a relative path must resolve
     to a file or directory that exists on disk. This mirrors the structural
     checks in ``validate_skill.py`` but is generic: it follows *any* relative
     link, so a stale cross-reference (issue <-> category <-> domain <->
     SKILL.md) fails here even when it is not one of the manifests
     ``validate_skill.py`` parses. It needs no network and therefore runs in
     both normal and ``--offline`` mode.

Extraction masks fenced code blocks (``` and ~~~) and inline code spans first,
preserving string length and newlines, so link-looking text inside code is not
mistaken for a real link and reported line numbers stay correct.

Usage:
  python3 scripts/check_links.py            # external URLs + relative links
  python3 scripts/check_links.py --offline  # relative links only
"""
from __future__ import annotations

import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent

URL_RE = re.compile(r'https?://[^\s)\]>"\'`]+')

# Placeholders: examples, attack-target illustrations, template vars,
# link-local metadata IPs — never fetched.
SKIP_PATTERNS = [
    r'\.<',            # https://mta-sts.<domain>
    r'\{',             # template vars
    r'example\.',      # example.com etc.
    r'\bphish',        # phishing illustration URLs
    r'169\.254\.',     # link-local (IMDS example)
    r'\bx\.com/ghumare64/status',  # social post, often blocks bots (checked manually)
    r'localhost',
    r'\.internal\b',
    r'\.\.\.',         # truncated URLs
    r'^http://app$',   # nginx proxy_pass example in hsts.md
    r'token\.actions\.githubusercontent\.com',  # OIDC issuer value, not a browsable page
]

UA = {"User-Agent": "Mozilla/5.0 (compatible; skill-link-checker)"}

# --- relative-link extraction ---------------------------------------------

# `[label](target)` or `![alt](target)`. Both target and label are confined to
# a single line and the target may not contain a ')', which keeps the match to
# a real markdown inline link instead of running past the closing paren.
LINK_RE = re.compile(r'!?\[[^\]\n]*\]\(([^)\n]*)\)')
# Optional title after the target: [label](../x.md "Title"). Stripped so the
# bare path is what gets resolved.
TITLE_RE = re.compile(r'^(.*?)\s+(?:"[^"]*"|\'[^\']*\'|\([^)]*\))\s*$')
# Opening OR closing fence: a line of >=3 backticks or tildes (info string ok).
FENCE_RE = re.compile(r'^[ \t]*(`{3,}|~{3,})')
# Any `scheme:` prefix (http:, https:, mailto:, data:, ...) — not a repo path.
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.\-]*:')


def is_placeholder(url: str) -> bool:
    return any(re.search(p, url) for p in SKIP_PATTERNS)


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
        k = j
        end = -1
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


def fetch_ok(url: str) -> tuple[str, str]:
    """Returns ('ok'|'blocked'|'broken', status)."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return "ok", str(r.status)
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue  # try GET
            # 403/429 from datacenter IPs is WAF bot-blocking, not link rot.
            if e.code in (403, 429):
                return "blocked", str(e.code)
            return "broken", str(e.code)
        except Exception as e:
            return "broken", type(e).__name__
    return "broken", "unreachable"


def check_relative(files) -> tuple[int, list[tuple[str, int, str]], int]:
    """Validate every relative markdown link in `files`.

    Returns (checked, broken, skipped) where `broken` is a list of
    (relative_file, line_no, raw_target) and `skipped` counts targets that are
    not repo-relative paths (anchors, schemes, absolute, placeholders).
    """
    checked = 0
    skipped = 0
    broken = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in LINK_RE.finditer(mask_code(text)):
            raw = m.group(1).strip()
            tm = TITLE_RE.match(raw)
            if tm:
                raw = tm.group(1).strip()
            path, reason = classify_target(raw)
            if reason is not None:
                skipped += 1
                continue
            checked += 1
            if not (f.parent / path).exists():
                line = text.count("\n", 0, m.start()) + 1
                broken.append((str(f.relative_to(ROOT)), line, raw))
    return checked, broken, skipped


def main() -> int:
    offline = "--offline" in sys.argv
    files = sorted(p for p in ROOT.rglob("*.md")
                  if ".git" not in p.parts)

    # --- graph 2: the repo's own relative links (no network, always runs) ---
    rel_checked, rel_broken, rel_skipped = check_relative(files)

    # --- graph 1: external http(s) URLs ------------------------------------
    urls = {}
    for f in files:
        for m in URL_RE.finditer(f.read_text(encoding="utf-8", errors="ignore")):
            u = m.group(0).rstrip(".,;:")
            urls.setdefault(u, set()).add(str(f.relative_to(ROOT)))

    real = {u: v for u, v in urls.items() if not is_placeholder(u)}
    skipped = len(urls) - len(real)
    broken = []
    blocked = []
    if not offline:
        for u in sorted(real):
            state, status = fetch_ok(u)
            mark = {"ok": "ok ", "blocked": "WARN", "broken": "FAIL"}[state]
            print(f"  {mark} {status:>4}  {u}")
            if state == "broken":
                broken.append((u, status, sorted(real[u])))
            elif state == "blocked":
                blocked.append(u)
    else:
        print(f"offline mode: {len(real)} real URLs would be checked")

    print(f"\nlinks: {len(real)} checked, {skipped} placeholders skipped, "
          f"{len(blocked)} WAF-blocked (not treated as broken), "
          f"{len(broken)} broken")
    print(f"relative links: {rel_checked} checked, {len(rel_broken)} broken"
          + (f" ({rel_skipped} non-relative/placeholder targets skipped)"
             if rel_skipped else ""))
    for u, status, where in broken:
        print(f"  BROKEN {status}: {u}")
        for w in where:
            print(f"    in {w}")
    for rel, line, target in rel_broken:
        print(f"  {rel}:{line} -> {target}")
    return 1 if broken or rel_broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
