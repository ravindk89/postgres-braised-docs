#!/usr/bin/env python3
"""
fix-longlines.py — Reflow over-long prose lines at sentence boundaries.

Strategy:
  - Find safe split points: '. ', '? ', '! ' followed by a word character,
    OUTSIDE of inline code spans and links.
  - Only split lines where ALL resulting pieces are <= WRAP_WIDTH.
  - Leave lines untouched if no safe split brings every piece under the limit.

Categories (for analysis mode):
  SAFE    plain prose or emphasis-only, can split anywhere
  CODE    contains backtick spans — split only outside spans
  LINK    contains markdown links — split only outside links
  SKIP    no safe split point found

Usage:
    python3 fix-longlines.py           # in-place, all docs/
    python3 fix-longlines.py --dry-run
    python3 fix-longlines.py --analyze # stats + per-file summary, no changes
    python3 fix-longlines.py path/to/file.md
"""

import difflib, os, re, sys

DOCS        = os.path.join(os.path.dirname(__file__), 'docs')
THRESH      = 400    # flag lines longer than this
WRAP_WIDTH  = 120    # target line width after wrapping

_FENCE_RE    = re.compile(r'^(`{3,}|~{3,})')
_OPEN_RE     = re.compile(r'^\s*:::\{')
_CLOSE_RE    = re.compile(r'^\s*:::')
_FRONT_END   = re.compile(r'^---\s*$')

# Patterns for detecting markdown spans
_CODE_SPAN   = re.compile(r'`[^`]+`')
_LINK_SPAN   = re.compile(r'\[[^\]]+\]\([^)]+\)')
_EMPH_SPAN   = re.compile(r'\*[^*]+\*|_[^_]+_')

# Sentence-end split candidates: '. ', '? ', '! ' before a word/link/backtick
_SPLIT_RE    = re.compile(r'(?<=[.?!]) +(?=[\w`\[\*])')


def _span_ranges(line: str) -> list[tuple[int, int]]:
    """Return list of (start, end) ranges occupied by code spans and links."""
    ranges: list[tuple[int, int]] = []
    for m in _CODE_SPAN.finditer(line):
        ranges.append((m.start(), m.end()))
    for m in _LINK_SPAN.finditer(line):
        ranges.append((m.start(), m.end()))
    return ranges


def _in_span(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(s <= pos < e for s, e in spans)


def _try_reflow(line: str) -> str | None:
    """
    Try to reflow `line` by splitting at safe sentence boundaries.
    Returns the reflowed text (newline-joined) or None if no safe split exists
    that keeps all pieces <= WRAP_WIDTH.
    """
    s = line.rstrip()
    if len(s) <= THRESH:
        return None

    spans = _span_ranges(s)
    split_points: list[int] = []

    for m in _SPLIT_RE.finditer(s):
        # m.start() is the position of the space(s) — the split is after the
        # sentence-ending punctuation.  Check neither edge is inside a span.
        punct_end = m.start()   # position right after ./?/!
        if not _in_span(punct_end, spans):
            split_points.append(m.start() + 1)   # start of next sentence

    if not split_points:
        return None

    # Greedily pack words into lines <= WRAP_WIDTH using split_points
    pieces: list[str] = []
    prev = 0
    for sp in split_points:
        chunk = s[prev:sp].rstrip()
        if len(chunk) <= WRAP_WIDTH:
            pieces.append(chunk)
            prev = sp
        # else: skip this split point, continue accumulating
    tail = s[prev:].rstrip()
    if tail:
        pieces.append(tail)

    # Only emit if we actually split and every piece fits
    if len(pieces) <= 1:
        return None
    if any(len(p) > WRAP_WIDTH for p in pieces):
        return None

    return '\n'.join(pieces)


def _classify(line: str) -> str:
    s = line.rstrip()
    if _CODE_SPAN.search(s) or _LINK_SPAN.search(s):
        return 'CODE/LINK'
    if _EMPH_SPAN.search(s):
        return 'EMPH'
    return 'PLAIN'


def convert_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    in_front = in_fence = False
    depth = 0

    for i, line in enumerate(lines, 1):
        s = line.rstrip()

        if i == 1 and s == '---':
            in_front = True
            out.append(line)
            continue
        if in_front:
            if _FRONT_END.match(s):
                in_front = False
            out.append(line)
            continue

        if _FENCE_RE.match(s):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        if _OPEN_RE.match(s):
            depth += 1
            out.append(line)
            continue
        if _CLOSE_RE.match(s):
            if depth > 0:
                depth -= 1
            out.append(line)
            continue

        # Skip headings, tables, blank lines, list items, directive content
        if s.startswith('#') or s.startswith('|') or not s:
            out.append(line)
            continue
        if s.startswith(' ') or s.startswith('\t'):
            out.append(line)
            continue
        if depth > 0:
            out.append(line)
            continue

        if len(s) > THRESH:
            reflowed = _try_reflow(s)
            if reflowed:
                # Preserve trailing newline style
                ending = '\n' if line.endswith('\n') else ''
                out.append(reflowed + ending)
                continue

        out.append(line)

    return out


def _analyze(paths: list[str]) -> None:
    from collections import Counter
    total = fixed = manual = 0
    by_cat: Counter = Counter()
    skipped_files: list[tuple[str, int, int]] = []  # (rel, total, manual)

    for path in paths:
        rel = os.path.relpath(path, DOCS)
        f_total = f_manual = 0
        in_front = in_fence = False
        depth = 0

        with open(path) as fh:
            lines = fh.readlines()

        for i, line in enumerate(lines, 1):
            s = line.rstrip()
            if i == 1 and s == '---': in_front = True; continue
            if in_front:
                if _FRONT_END.match(s): in_front = False
                continue
            if _FENCE_RE.match(s): in_fence = not in_fence; continue
            if in_fence: continue
            if _OPEN_RE.match(s): depth += 1; continue
            if _CLOSE_RE.match(s):
                if depth > 0: depth -= 1
                continue
            if s.startswith('#') or s.startswith('|') or not s: continue
            if s.startswith(' ') or s.startswith('\t'): continue
            if depth > 0: continue
            if len(s) <= THRESH: continue

            total += 1; f_total += 1
            cat = _classify(s)
            by_cat[cat] += 1
            if _try_reflow(s):
                fixed += 1
            else:
                manual += 1; f_manual += 1

        if f_manual > 0:
            skipped_files.append((rel, f_total, f_manual))

    print(f'Total long prose lines:  {total}')
    print(f'  Auto-wrappable:        {fixed}  (will be fixed)')
    print(f'  Need manual review:    {manual}')
    print()
    print('By content type:')
    for cat, cnt in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f'  {cat:12s}: {cnt}')
    print()
    print(f'Files with manual-review lines ({len(skipped_files)}):')
    for rel, tot, man in sorted(skipped_files, key=lambda x: -x[2])[:20]:
        print(f'  {man:3d}/{tot:3d}  {rel}')
    if len(skipped_files) > 20:
        print(f'  … and {len(skipped_files)-20} more')


def process(path: str, dry_run: bool = False) -> bool:
    original = open(path).readlines()
    new_lines = convert_lines(original)
    if original == new_lines:
        return False
    if not dry_run:
        with open(path, 'w') as f:
            f.writelines(new_lines)
    return True


def show_diff(path: str) -> None:
    original = open(path).readlines()
    new_lines = convert_lines(original)
    diff = list(difflib.unified_diff(original, new_lines,
                                     fromfile=path, tofile=path + ' (fixed)', n=2))
    if diff:
        sys.stdout.writelines(diff[:80])
        if len(diff) > 80:
            print(f'  … ({len(diff) - 80} more diff lines)')
        print()


def main() -> None:
    args    = sys.argv[1:]
    dry_run = '--dry-run' in args
    analyze = '--analyze' in args
    args    = [a for a in args if a not in ('--dry-run', '--analyze')]

    paths = (
        [os.path.abspath(a) for a in args if a.endswith('.md')]
        if args else
        sorted(os.path.join(r, f)
               for r, _, files in os.walk(DOCS)
               for f in files if f.endswith('.md'))
    )

    if analyze:
        _analyze(paths)
        return

    changed = 0
    for path in paths:
        if dry_run:
            show_diff(path)
        if process(path, dry_run=dry_run):
            changed += 1

    verb = 'would change' if dry_run else 'changed'
    print(f'{verb}: {changed}/{len(paths)} files')


if __name__ == '__main__':
    main()
