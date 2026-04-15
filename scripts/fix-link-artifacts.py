#!/usr/bin/env python3
"""
fix-link-artifacts.py — Fix two categories of pandoc link artifacts:

  1. Leading space in link text:  [ Title](#anchor) → [Title](#anchor)
     (also in braised:ref links)

  2. [example_title](#id) → [example](#id)
     (pandoc placeholder for DocBook <xref> to an <example> element)

Usage:
    python3 fix-link-artifacts.py           # in-place, all docs/
    python3 fix-link-artifacts.py --dry-run
    python3 fix-link-artifacts.py path/to/file.md
"""

import difflib, os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), 'docs')

# Leading space: [ Some Text](url)
_LEADING_SPACE_RE = re.compile(r'\[ ([^\]]+)\]\(')

# example_title placeholder
_EXAMPLE_TITLE_RE = re.compile(r'\[example_title\]\(([^)]+)\)')


def fix_line(line: str) -> str:
    # 1. Strip leading space from link text
    line = _LEADING_SPACE_RE.sub(lambda m: f'[{m.group(1)}](', line)
    # 2. example_title → [example](url)
    line = _EXAMPLE_TITLE_RE.sub(lambda m: f'[example]({m.group(1)})', line)
    return line


def fix_file_lines(lines: list[str]) -> list[str]:
    out = []
    in_fence = False
    for line in lines:
        s = line.rstrip()
        if re.match(r'^(`{3,}|~{3,})', s):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        out.append(fix_line(line))
    return out


def process(path: str, dry_run: bool = False) -> bool:
    original = open(path).readlines()
    new_lines = fix_file_lines(original)
    if original == new_lines:
        return False
    if not dry_run:
        with open(path, 'w') as f:
            f.writelines(new_lines)
    return True


def show_diff(path: str) -> None:
    original = open(path).readlines()
    new_lines = fix_file_lines(original)
    diff = list(difflib.unified_diff(original, new_lines,
                                     fromfile=path, tofile=path + ' (fixed)', n=2))
    if diff:
        sys.stdout.writelines(diff[:60])
        if len(diff) > 60:
            print(f'  … ({len(diff) - 60} more diff lines)')
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
