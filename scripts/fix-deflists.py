#!/usr/bin/env python3
"""
fix-deflists.py — Convert CommonMark-style definition lists to braised :::dl/:::item blocks.

Source format (pandoc-generated):
    `term` (type)

    :   First paragraph of definition.

        Continuation paragraph (4-space indented).

        :::{.callout type="note"}
        ...
        :::

Target format:
    :::{.dl}
    :::{.item term="`term` (type)"}
    First paragraph of definition.

    Continuation paragraph.

    :::{.callout type="note"}
    ...
    :::
    :::
    :::{/dl}

Rules:
  - A "term" is a non-blank, non-heading, non-indented line immediately followed
    (after one optional blank line) by a line starting with ':   '.
  - Consecutive (term + definition) pairs grouped into one :::dl block.
  - Definition body: strip leading 4 spaces from every non-blank continuation line.
  - Term attribute: double-quoted; internal " replaced with '.

Usage:
    python3 fix-deflists.py           # in-place, all docs/
    python3 fix-deflists.py --dry-run
    python3 fix-deflists.py path/to/file.md
"""

import difflib, os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), 'docs')

_FENCE_RE       = re.compile(r'^(`{3,}|~{3,})')
_HEADING_RE     = re.compile(r'^#{1,6} ')
_DEF_OPEN_RE    = re.compile(r'^:   ')          # definition marker
_INDENT4_RE     = re.compile(r'^    ')           # 4-space continuation


def _is_blank(line: str) -> bool:
    return not line.strip()


def _is_term_candidate(line: str) -> bool:
    """True if line could be a definition list term."""
    s = line.rstrip()
    if not s:
        return False
    if _HEADING_RE.match(s):
        return False
    if s.startswith(' ') or s.startswith('\t'):
        return False
    if _FENCE_RE.match(s):
        return False
    if _DEF_OPEN_RE.match(s):
        return False
    if s.startswith('|'):
        return False
    if s.startswith('---') or s == '---':
        return False
    return True


def _next_nonblank(lines: list[str], start: int) -> int:
    """Return index of next non-blank line at or after start, or len(lines)."""
    i = start
    while i < len(lines) and _is_blank(lines[i]):
        i += 1
    return i


def _is_term_at(lines: list[str], i: int) -> bool:
    """True if lines[i] is a definition list term (next non-blank is ':   ')."""
    if not _is_term_candidate(lines[i]):
        return False
    j = _next_nonblank(lines, i + 1)
    if j >= len(lines):
        return False
    return _DEF_OPEN_RE.match(lines[j]) is not None


def _collect_definition(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    Collect definition body starting at lines[start] (which must start with ':   ').
    Returns (body_lines_unindented, next_index).
    Body lines have 4-space prefix stripped; blank lines preserved as-is.
    """
    body: list[str] = []
    i = start

    # First line: strip ':   ' (4 chars)
    first = lines[i]
    body.append(first[4:] if first.startswith(':   ') else first)
    i += 1

    # Continuation: blank lines and 4-space indented lines
    while i < len(lines):
        line = lines[i]
        if _is_blank(line):
            # Blank line: might be end of definition or internal blank.
            # Look ahead to decide.
            j = _next_nonblank(lines, i + 1)
            if j >= len(lines):
                # End of file: end definition (don't include trailing blank)
                break
            next_s = lines[j]
            # Continue if next non-blank content is still indented 4+
            if _INDENT4_RE.match(next_s) or _DEF_OPEN_RE.match(next_s):
                body.append(line)   # preserve internal blank line
                i += 1
                continue
            # Otherwise end of definition
            break
        elif _INDENT4_RE.match(line):
            body.append(line[4:])   # strip 4-space indent
            i += 1
        else:
            # Non-indented non-blank: end of definition
            break

    # Strip trailing blank lines from body
    while body and _is_blank(body[-1]):
        body.pop()

    return body, i


def _term_attr(term: str) -> str:
    """Format term as a double-quoted attribute value; escape internal "."""
    val = term.rstrip().replace('"', "'")
    return f'term="{val}"'


def convert_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    in_fence = False

    while i < len(lines):
        line = lines[i]
        s = line.rstrip()

        # Track code fences
        if _FENCE_RE.match(s):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue

        if in_fence:
            out.append(line)
            i += 1
            continue

        # Check if this line is a definition list term
        if _is_term_at(lines, i):
            # Open a :::dl group
            out.append(':::{.dl}\n')

            while i < len(lines) and _is_term_at(lines, i):
                term = lines[i].rstrip()
                i += 1

                # Skip blank lines between term and ':   '
                while i < len(lines) and _is_blank(lines[i]):
                    i += 1

                if i >= len(lines) or not _DEF_OPEN_RE.match(lines[i]):
                    # Shouldn't happen given _is_term_at check, but be safe
                    out.append(term + '\n')
                    break

                body, i = _collect_definition(lines, i)

                out.append(f':::{{.item {_term_attr(term)}}}\n')
                for bl in body:
                    out.append(bl if bl.endswith('\n') else bl + '\n')
                out.append(':::{/item}\n')

                # Skip blank lines between items
                blanks: list[str] = []
                while i < len(lines) and _is_blank(lines[i]):
                    blanks.append(lines[i])
                    i += 1

                # If next non-blank is another term, continue group
                if i < len(lines) and _is_term_at(lines, i):
                    pass  # loop continues
                else:
                    # End of group: emit collected blanks and close
                    out.append(':::{/dl}\n')
                    out.extend(blanks)
                    break
            else:
                # Exited loop normally (i >= len or not a term) → close dl
                out.append(':::{/dl}\n')

            continue

        out.append(line)
        i += 1

    return out


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
    args    = [a for a in args if a != '--dry-run']

    paths = (
        [os.path.abspath(a) for a in args if a.endswith('.md')]
        if args else
        sorted(os.path.join(r, f)
               for r, _, files in os.walk(DOCS)
               for f in files if f.endswith('.md'))
    )

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
