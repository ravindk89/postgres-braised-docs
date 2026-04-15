#!/usr/bin/env python3
"""
fix-item-closes.py — Replace bare ::: item closes with :::{/item}.

Now that `item` is a structural block in braised (can contain nested blocks
like callouts), it requires a named close :::{/item} instead of a simple :::.

Algorithm: maintain a flat stack of open block names.
  - :::{.name ...}  → push name
  - :::{/name}      → pop matching name (named close, leave line as-is)
  - :::             → pop top; if top was "item", upgrade line to :::{/item}

Usage:
    python3 fix-item-closes.py           # in-place, all docs/
    python3 fix-item-closes.py --dry-run
    python3 fix-item-closes.py path/to/file.md
"""

import difflib, os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), 'docs')

_FENCE_RE        = re.compile(r'^(`{3,}|~{3,})')
_OPEN_RE         = re.compile(r'^:::\{\.(\S+)')        # :::{.name ...}
_NAMED_CLOSE_RE  = re.compile(r'^:::\{/([^}]+)\}')     # :::{/name}
_SIMPLE_CLOSE_RE = re.compile(r'^:::\s*$')              # ::: bare


def _block_name(s: str) -> str | None:
    """Return block name from :::{.name ...} line, or None."""
    m = _OPEN_RE.match(s)
    if not m:
        return None
    # name ends at first space, }, or end
    raw = m.group(1)
    return re.split(r'[\s}]', raw)[0]


def convert_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    in_fence = False
    stack: list[str] = []   # names of currently open blocks

    for line in lines:
        s = line.rstrip()

        # Track code fences — don't touch content inside
        if _FENCE_RE.match(s):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        # Named close :::{/name}
        m = _NAMED_CLOSE_RE.match(s)
        if m:
            name = m.group(1)
            # Pop the matching block from the stack (find innermost match)
            for j in range(len(stack) - 1, -1, -1):
                if stack[j] == name:
                    stack.pop(j)
                    break
            out.append(line)
            continue

        # Simple close :::
        if _SIMPLE_CLOSE_RE.match(s):
            if stack:
                top = stack.pop()
                if top == 'item':
                    out.append(':::{/item}\n')
                    continue
            out.append(line)
            continue

        # Block open :::{.name ...}
        name = _block_name(s)
        if name:
            stack.append(name)

        out.append(line)

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
