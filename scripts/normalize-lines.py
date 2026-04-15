#!/usr/bin/env python3
"""
normalize-lines.py — Reflow prose paragraphs to one sentence per line.

Contexts left untouched:
  - YAML frontmatter (between --- at file start)
  - Fenced code blocks (``` or ~~~)
  - Indented code (4+ spaces / tab)
  - Directives (lines starting with :::)
  - Headings (#)
  - Tables (|)
  - List items (- / * / N.)
  - Definition list markers (:   )
  - Blank lines

Only standalone prose paragraphs are reflowed.

Usage:
    python3 normalize-lines.py             # in-place, all docs/
    python3 normalize-lines.py --dry-run   # show unified diff for first few files
    python3 normalize-lines.py path/to/file.md   # single file
"""

import difflib, os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), 'docs')

# Common abbreviations whose trailing period does NOT end a sentence.
# We protect them by replacing '.' with a placeholder before splitting.
_ABBREV_PAT = re.compile(
    r'\b(e\.g|i\.e|etc|vs\.?|cf|no|vol|pp?|eds?|approx|fig|dept|est|'
    r'incl|excl|ref|sect|app|par|ch|ver|rev|'
    r'mr|mrs|ms|dr|prof|sr|jr|gen|lt|col|maj|sgt|gov|'
    r'[a-z])\.',  # single lowercase letter (e.g. "a." in lists)
    re.IGNORECASE,
)

_PLACEHOLDER = '\x00'


def split_sentences(text: str) -> list[str]:
    """Split a prose block into individual sentences (one per element)."""
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return []

    # Protect abbreviations: replace their period with placeholder.
    protected = _ABBREV_PAT.sub(lambda m: m.group().replace('.', _PLACEHOLDER), text)

    # A sentence boundary: end-punctuation then whitespace then uppercase/quote.
    # Variable-width lookbehind not supported; use two separate patterns:
    # one for punct+quote and one for bare punct.
    parts = re.split(r'(?<=[.!?])["\']?\s+(?=[A-Z\u201C])', protected)

    return [p.replace(_PLACEHOLDER, '.').strip() for p in parts if p.strip()]


_FENCE_RE   = re.compile(r'^(`{3,}|~{3,})')
_LIST_RE    = re.compile(r'^(\s*)([-*+]|\d+[.)]) ')   # - item / 1. item
_DEFLIST_RE = re.compile(r'^:   ')                     # pandoc definition list
# Opening directive: :::something or :::{...}  Closing directive: bare :::
_DIRECT_OPEN_RE  = re.compile(r'^:::[^:\s]|^:::\{')
_DIRECT_CLOSE_RE = re.compile(r'^:::\s*$')
_DIRECT_ANY_RE   = re.compile(r'^:{1,3}')             # any ::: line


def is_structural(line: str) -> bool:
    """Lines that must not be joined into a prose paragraph."""
    s = line.rstrip()
    return (
        not s                          # blank
        or s.startswith('#')           # heading
        or s.startswith('|')           # table
        or s.startswith('    ')        # indented code / list continuation
        or s.startswith('\t')          # tab-indented code
        or bool(_LIST_RE.match(s))     # list item
        or bool(_DEFLIST_RE.match(s))  # definition list
        or bool(_DIRECT_ANY_RE.match(s))  # any directive marker
    )


def reflow_file(path: str) -> list[str]:
    """Return the reflowed lines for *path* (does not write)."""
    with open(path) as f:
        lines = f.readlines()

    out: list[str] = []
    in_frontmatter = False
    in_fence = False
    in_directive = False
    para_buf: list[str] = []

    def flush():
        if not para_buf:
            return
        block = ' '.join(l.rstrip() for l in para_buf)
        for s in split_sentences(block):
            out.append(s + '\n')
        para_buf.clear()

    for i, line in enumerate(lines):
        s = line.rstrip()

        # ── Frontmatter ────────────────────────────────────────────────────
        if i == 0 and s == '---':
            in_frontmatter = True
            out.append(line)
            continue
        if in_frontmatter:
            out.append(line)
            if s == '---' and i > 0:
                in_frontmatter = False
            continue

        # ── Code fence toggle ───────────────────────────────────────────────
        if _FENCE_RE.match(s):
            flush()
            in_fence = not in_fence
            out.append(line)
            continue

        if in_fence:
            out.append(line)
            continue

        # ── Directive block toggle (:::type ... :::) ────────────────────────
        # Opening: :::something or :::{...}
        # Closing: bare :::
        # Content inside directives passes through unchanged (may be structured).
        if _DIRECT_OPEN_RE.match(s):
            flush()
            in_directive = True
            out.append(line)
            continue
        if _DIRECT_CLOSE_RE.match(s):
            flush()
            in_directive = False
            out.append(line)
            continue
        if in_directive:
            out.append(line)
            continue

        # ── Structural / non-prose lines ────────────────────────────────────
        if is_structural(line):
            flush()
            out.append(line)
            continue

        # ── Prose: accumulate ───────────────────────────────────────────────
        para_buf.append(s)

    flush()
    return out


def process(path: str, dry_run: bool = False) -> bool:
    """Process one file. Returns True if the file changed."""
    original = open(path).readlines()
    new_lines = reflow_file(path)

    if original == new_lines:
        return False

    if not dry_run:
        with open(path, 'w') as f:
            f.writelines(new_lines)
    return True


def show_diff(path: str, new_lines: list[str]) -> None:
    original = open(path).readlines()
    diff = list(difflib.unified_diff(original, new_lines,
                                     fromfile=path, tofile=path + ' (reflowed)', n=2))
    if diff:
        sys.stdout.writelines(diff[:60])
        if len(diff) > 60:
            print(f'  ... ({len(diff) - 60} more diff lines)')
        print()


def main() -> None:
    args = sys.argv[1:]
    dry_run   = '--dry-run' in args
    show_only = '--show'    in args
    args = [a for a in args if not a.startswith('--')]

    if args:
        paths = [os.path.abspath(a) for a in args]
    else:
        paths = sorted(
            os.path.join(root, f)
            for root, _, files in os.walk(DOCS)
            for f in files
            if f.endswith('.md')
        )

    changed = 0
    for path in paths:
        if dry_run or show_only:
            new_lines = reflow_file(path)
            original  = open(path).readlines()
            if original != new_lines:
                show_diff(path, new_lines)
                changed += 1
        else:
            if process(path):
                changed += 1

    verb = 'would change' if (dry_run or show_only) else 'changed'
    print(f'{verb}: {changed}/{len(paths)} files')


if __name__ == '__main__':
    main()
