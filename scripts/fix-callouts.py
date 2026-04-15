#!/usr/bin/env python3
"""
fix-callouts.py — Convert pandoc-style ::: note/tip/warning/caution directives
to braised :::{.callout type="..."} syntax.

Patterns handled:
  1. ::: note/tip/warning/caution       → :::{.callout type="name"}
     (with any leading whitespace preserved)

  2. ::: note/::: title/Title/:::       → :::{.callout type="note" title="Title"}
     (title sub-block folded into outer callout attribute; title block removed)

  3. Closing ::: lines are left as-is (already valid bare-close syntax).

Usage:
    python3 fix-callouts.py           # in-place, all docs/
    python3 fix-callouts.py --dry-run # show diffs only
    python3 fix-callouts.py path/to/file.md
"""

import difflib, os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), 'docs')

# Types that map directly to callout type= attribute.
_CALLOUT_TYPES = {'note', 'tip', 'warning', 'caution'}

# Pattern: optional leading whitespace + ::: + type name + optional trailing space
_OPEN_RE = re.compile(r'^(\s*):::+\s+(' + '|'.join(_CALLOUT_TYPES) + r')\s*$')

# Pattern: ::: title sub-block within a note
# Matches (with same indentation prefix):
#   indent + ::: title
#   indent + Title text
#   indent + :::
_TITLE_BLOCK_RE = re.compile(
    r'^(\s*):::+\s+title\s*\n'   # ::: title line (capture indent)
    r'\1(.+?)\n'                  # title text (same indent)
    r'\1:::\s*\n',                # ::: close (same indent)
    re.MULTILINE,
)


def _fold_title(content: str) -> tuple[str, str | None]:
    """
    If content starts with a ::: title block, extract the title and return
    (remaining_content, title_string). Otherwise return (content, None).
    """
    m = _TITLE_BLOCK_RE.match(content)
    if not m:
        return content, None
    title = m.group(2).strip()
    remaining = content[m.end():]
    # Strip one leading blank line if present
    remaining = re.sub(r'^\n', '', remaining)
    return remaining, title


def fix_file_content(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    in_fence = False

    while i < len(lines):
        line = lines[i]
        s = line.rstrip()

        # Track fenced code blocks — don't touch content inside
        if re.match(r'^(`{3,}|~{3,})', s):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue

        if in_fence:
            out.append(line)
            i += 1
            continue

        m = _OPEN_RE.match(line)
        if not m:
            out.append(line)
            i += 1
            continue

        indent = m.group(1)
        callout_type = m.group(2)

        # Collect the body of this callout block (up to the closing :::)
        # so we can look for a ::: title sub-block.
        body_lines: list[str] = []
        j = i + 1
        depth = 1
        while j < len(lines):
            bl = lines[j]
            bs = bl.rstrip()
            # Check for nested ::: open
            if re.match(r'^\s*:::+\s+\w', bs):
                depth += 1
            # Check for bare ::: close at same indent level
            elif re.match(r'^' + re.escape(indent) + r':::\s*$', bs) and depth == 1:
                break
            elif re.match(r'^\s*:::\s*$', bs) and depth > 1:
                depth -= 1
            body_lines.append(bl)
            j += 1
        # j is now pointing at the closing ::: line (or end of file)
        close_line = lines[j] if j < len(lines) else indent + ':::\n'

        body_text = ''.join(body_lines)
        remaining_body, title = _fold_title(body_text)

        # Build the new opening line
        if title:
            open_line = f'{indent}:::{{.callout type="{callout_type}" title="{title}"}}\n'
        else:
            open_line = f'{indent}:::{{.callout type="{callout_type}"}}\n'

        out.append(open_line)
        out.extend(remaining_body.splitlines(keepends=True))
        out.append(close_line)
        i = j + 1

    return ''.join(out)


def process(path: str, dry_run: bool = False) -> bool:
    original = open(path).read()
    new_text = fix_file_content(original)
    if original == new_text:
        return False
    if not dry_run:
        with open(path, 'w') as f:
            f.write(new_text)
    return True


def show_diff(path: str) -> None:
    original = open(path).read()
    new_text = fix_file_content(original)
    if original == new_text:
        return
    diff = list(difflib.unified_diff(
        original.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=path, tofile=path + ' (fixed)', n=2,
    ))
    sys.stdout.writelines(diff[:80])
    if len(diff) > 80:
        print(f'  … ({len(diff) - 80} more diff lines)')
    print()


def main() -> None:
    args     = sys.argv[1:]
    dry_run  = '--dry-run' in args
    args     = [a for a in args if a != '--dry-run']

    if args:
        paths = [os.path.abspath(a) for a in args if a.endswith('.md')]
    else:
        paths = sorted(
            os.path.join(root, f)
            for root, _, files in os.walk(DOCS)
            for f in files
            if f.endswith('.md')
        )

    changed = 0
    for path in paths:
        if dry_run:
            show_diff(path)
            if process(path, dry_run=True):
                changed += 1
        else:
            if process(path):
                changed += 1

    verb = 'would change' if dry_run else 'changed'
    print(f'{verb}: {changed}/{len(paths)} files')


if __name__ == '__main__':
    main()
