#!/usr/bin/env python3
"""
fix-artifacts.py — Fix pandoc conversion artifacts in docs/.

Transforms applied:
  1. [varlistentry_title](#id)  → `funcname` (extract name from fragment)
  2. [DoubledNameDoubledName](braised:ref/…) → `DoubledName`  (doubled link text)
  3. [step_title](#id)          → step title text (from STEP_TITLES map)
  4. ::: formalpara-title / **title:** lines → bold inline title

Usage:
    python3 fix-artifacts.py           # in-place, all docs/
    python3 fix-artifacts.py --dry-run # show what would change
    python3 fix-artifacts.py path/to/file.md
"""

import difflib, os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), 'docs')

# ── Step title lookup (from XML <step id="…"><title>…</title>) ────────────────

STEP_TITLES: dict[str, str] = {
    'configure':          'Configuration',
    'build':              'Build',
    'install':            'Installing the Files',
    'meson-configure':    'Configuration',
    'meson-build':        'Build',
    'meson-install':      'Installing the Files',
    # pg_upgrade steps
    'pgupgrade-step-replicas': 'Upgrade Streaming Replication Standbys',
    'pgupgrade-step-revert':   'Reverting to the Old Cluster',
    # operator resolution substeps (no title in XML — use short descriptor)
    'op-resol-exact-unknown':  'the exact-match rule',
    'op-resol-last-unknown':   'the last-unknown rule',
    'op-resol-exact-domain':   'the exact-match rule',
    # logical replication upgrade steps (no title in XML)
    'two-node-cluster-disable-subscriptions-node2':    'disabling subscriptions on node2',
    'cascaded-cluster-disable-sub-node1-node2':        'disabling subscriptions on node2',
    'cascaded-cluster-disable-sub-node2-node3':        'disabling subscriptions on node3',
    'circular-cluster-disable-sub-node2':              'disabling subscriptions on node2',
    'circular-cluster-disable-sub-node1':              'disabling subscriptions on node1',
}

# ── Regex patterns ─────────────────────────────────────────────────────────────

# [varlistentry_title](#some-id)
_VARLIST_RE = re.compile(r'\[varlistentry_title\]\(#([^)]+)\)')

# [SomeName SomeName](braised:ref/…) — doubled link text with space in between
# Also catches: [PQfoobarPQfoobar](braised:ref/…) — doubled without space
# Also catches: [PQfoobarPQfoobar extra garbage text](braised:ref/…)
_DOUBLED_LINK_RE = re.compile(
    r'\[([A-Za-z][A-Za-z0-9_]+)\1[^\]]*\]\(braised:ref/[^)]+\)'   # doubled + optional trailing garbage
    r'|\[([A-Za-z][A-Za-z0-9_\s]+) \2\]\(braised:ref/[^)]+\)'     # space-separated doubling
)

# [step_title](#some-id)
_STEP_TITLE_RE = re.compile(r'\[step_title\]\(#([^)]+)\)')

# ::: formalpara-title block (on its own line, possibly indented inside a list)
_FORMALPARA_RE = re.compile(r'^\s*:::\s*formalpara-title\s*$')


# ── Transform helpers ──────────────────────────────────────────────────────────

def _varlist_name(fragment: str) -> str:
    """
    Convert a varlistentry fragment to a display name.
    Examples:
      libpq-PQexec            → `PQexec`
      libpq-PQescapeByteaConn → `PQescapeByteaConn`
      create-database-lc-collate   → LC_COLLATE
      app-initdb-option-no-locale  → --no-locale
      pgtypestimestampfmtasc       → PGTYPEStimestamp_fmt_asc (best effort)
    """
    f = fragment
    # libpq functions: libpq-PQfoo → `PQfoo`
    if f.startswith('libpq-PQ') or f.startswith('libpq-pg') or f.startswith('libpq-PG'):
        return f'`{f[len("libpq-"):]}`'
    # create-database-param-name → *param* as inline code
    if f.startswith('create-database-'):
        param = f[len('create-database-'):]
        return f'`{param}`'
    # app-initdb-option-xxx → --xxx
    if f.startswith('app-initdb-option-'):
        opt = f[len('app-initdb-option-'):]
        return f'`--{opt}`'
    # pgtypes functions: just backtick the whole thing
    if f.startswith('pgtypes'):
        return f'`{f}`'
    # Default: backtick the fragment
    return f'`{f}`'


def _fix_doubled(m: re.Match) -> str:
    """Return backtick-wrapped name from a doubled link."""
    name = m.group(1) or m.group(2)
    return f'`{name}`'


def fix_line(line: str) -> str:
    """Apply all artifact fixes to a single line."""
    # 1. varlistentry_title
    line = _VARLIST_RE.sub(lambda m: _varlist_name(m.group(1)), line)

    # 2. Doubled link text  e.g. [PQexecPQexec](braised:ref/…)
    line = _DOUBLED_LINK_RE.sub(_fix_doubled, line)

    # 3. step_title
    def _step_repl(m: re.Match) -> str:
        step_id = m.group(1)
        title = STEP_TITLES.get(step_id)
        if title:
            return title
        # Unknown step: keep readable fragment
        return step_id.replace('-', ' ')
    line = _STEP_TITLE_RE.sub(_step_repl, line)

    return line


# Matches a multi-line link open: [some text without closing ]
_OPEN_LINK_RE = re.compile(r'\[[^\]]*$')
# Matches continuation that closes a link: optional indent + text](url)
_CLOSE_LINK_RE = re.compile(r'^\s*[^\[]*\]\([^)]+\)')


def _join_broken_links(lines: list[str]) -> list[str]:
    """
    Join links that were split across two lines by the sentence normalizer.
    e.g.  [PQerrorMessagePQerrorMessage
               error messagein PGconn](braised:ref/…)
    becomes a single line.
    """
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # If line has an unclosed [ (not inside a code fence / indented block)
        stripped = line.rstrip()
        if (not stripped.startswith('```')
                and _OPEN_LINK_RE.search(stripped)
                and i + 1 < len(lines)):
            next_line = lines[i + 1]
            # Check if next line closes the link
            if _CLOSE_LINK_RE.match(next_line):
                # Join: strip trailing newline from current, strip leading
                # whitespace from continuation, combine into one line
                joined = stripped + ' ' + next_line.lstrip()
                out.append(joined)
                i += 2
                continue
        out.append(line)
        i += 1
    return out


def fix_file_lines(lines: list[str]) -> list[str]:
    """Process a file's lines, applying artifact fixes."""
    # First pass: join any links broken across lines
    lines = _join_broken_links(lines)

    out: list[str] = []
    in_fence      = False
    i             = 0

    while i < len(lines):
        line = lines[i]
        s    = line.rstrip()

        # Track code fences — don't touch content inside
        if re.match(r'^(`{3,}|~{3,})', s):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue

        if in_fence:
            out.append(line)
            i += 1
            continue

        # formalpara-title block:
        #   ::: formalpara-title
        #   **Title text:**
        #   :::
        # → just emit the bold title line (strip the directive wrappers)
        if _FORMALPARA_RE.match(s):
            # Collect lines until closing :::
            block = []
            i += 1
            while i < len(lines):
                ls = lines[i].rstrip()
                if re.match(r'^\s*:::\s*$', ls):
                    i += 1
                    break
                block.append(lines[i])
                i += 1
            # Emit block lines with artifact fixes, no wrapping directives
            for bl in block:
                out.append(fix_line(bl.rstrip()) + '\n')
            continue

        # Normal line
        out.append(fix_line(line))
        i += 1

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
    original  = open(path).readlines()
    new_lines = fix_file_lines(original)
    diff = list(difflib.unified_diff(original, new_lines,
                                     fromfile=path, tofile=path + ' (fixed)', n=2))
    if diff:
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
            original  = open(path).readlines()
            new_lines = fix_file_lines(original)
            if original != new_lines:
                show_diff(path)
                changed += 1
        else:
            if process(path):
                changed += 1

    verb = 'would change' if dry_run else 'changed'
    print(f'{verb}: {changed}/{len(paths)} files')


if __name__ == '__main__':
    main()
