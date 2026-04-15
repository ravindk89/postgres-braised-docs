#!/usr/bin/env python3
"""
fix-broken-anchors.py — Fix local (#fragment) links that don't resolve in HTML.

Strategies:
  STRIP   [text](#anchor-table/fig/example/...)  →  text
          (Tables, figures, examples don't have HTML anchors; keep readable text)

  RELINK  [text](#runtime-config-X-subsection)   →  [text](braised:ref/runtime-config-X)
          (Cross-page runtime-config refs: map to parent section page)
          If the current file IS the target page, strip to plain text instead.

Usage:
    python3 fix-broken-anchors.py           # in-place, all docs/
    python3 fix-broken-anchors.py --dry-run
    python3 fix-broken-anchors.py path/to/file.md
"""

import difflib, os, re, sys, yaml

DOCS = os.path.join(os.path.dirname(__file__), 'docs')

# Anchor suffixes that should always be stripped (no HTML anchor exists).
_STRIP_SUFFIXES = (
    '-table', '-fig', '-example',
    '-levels', '-csvlog', '-jsonlog', '-matrix', '-summary',
)

# Fragment patterns to strip unconditionally (in addition to suffix-based).
_STRIP_FRAGMENT_RE = re.compile(
    r'^(?:'
    r'[a-z][a-z0-9_-]+-table'       # *-table
    r'|[a-z][a-z0-9_-]+-fig'        # *-fig
    r'|[a-z][a-z0-9_-]+-example'    # *-example
    r'|[a-z][a-z0-9_-]+-levels'     # *-levels
    r'|[a-z][a-z0-9_-]+-csvlog'     # *-csvlog
    r'|[a-z][a-z0-9_-]+-jsonlog'    # *-jsonlog
    r'|[a-z][a-z0-9_-]+-matrix'     # *-matrix
    r'|[a-z][a-z0-9_-]+-summary'    # *-summary
    r'|[a-z_]+_title'               # *_title artifact
    r'|typedefs-table'
    r')$'
)

# Ordered list of runtime-config page IDs (longest first for prefix matching).
# Derived from scan of docs/iii-server-administration/19-server-configuration/.
_RUNTIME_CONFIG_PAGES = [
    'runtime-config-compatible',
    'runtime-config-connection',
    'runtime-config-developer',
    'runtime-config-error-handling',
    'runtime-config-file-locations',
    'runtime-config-statistics',
    'runtime-config-resource',
    'runtime-config-replication',
    'runtime-config-logging',
    'runtime-config-locks',
    'runtime-config-client',
    'runtime-config-custom',
    'runtime-config-preset',
    'runtime-config-vacuum',
    'runtime-config-query',
    'runtime-config-short',
    'runtime-config-wal',
]


def _runtime_config_page(frag: str) -> str | None:
    """Return the braised:ref page ID for a runtime-config-* fragment, or None."""
    for page_id in _RUNTIME_CONFIG_PAGES:
        if frag == page_id or frag.startswith(page_id + '-'):
            return page_id
    return None


def _page_id_of(path: str) -> str | None:
    """Return the braised `id:` frontmatter value of a doc file."""
    try:
        with open(path) as f:
            text = f.read(400)
        m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
        if m:
            fm = yaml.safe_load(m.group(1))
            return fm.get('id') if fm else None
    except Exception:
        return None
    return None


# Single regex to find all local fragment links.
_LINK_RE = re.compile(r'\[([^\]]+)\]\(#([a-z][a-z0-9_-]*)\)')


def _fix_line(line: str, current_page_id: str | None) -> str:
    def _replace(m: re.Match) -> str:
        text = m.group(1)
        frag = m.group(2)

        # 1. Strip if suffix matches
        if _STRIP_FRAGMENT_RE.match(frag):
            return text

        # 2. runtime-config-* → braised:ref or strip
        if frag.startswith('runtime-config-'):
            page = _runtime_config_page(frag)
            if page:
                if page == current_page_id:
                    return text          # same page, just strip
                return f'[{text}](braised:ref/{page})'
            return text                 # unknown, strip

        # Not a pattern we handle — leave unchanged
        return m.group(0)

    return _LINK_RE.sub(_replace, line)


def fix_file_lines(lines: list[str], page_id: str | None) -> list[str]:
    out: list[str] = []
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
        out.append(_fix_line(line, page_id))
    return out


def process(path: str, dry_run: bool = False) -> bool:
    page_id = _page_id_of(path)
    original = open(path).readlines()
    new_lines = fix_file_lines(original, page_id)
    if original == new_lines:
        return False
    if not dry_run:
        with open(path, 'w') as f:
            f.writelines(new_lines)
    return True


def show_diff(path: str) -> None:
    page_id = _page_id_of(path)
    original = open(path).readlines()
    new_lines = fix_file_lines(original, page_id)
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
