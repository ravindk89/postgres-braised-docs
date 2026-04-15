#!/usr/bin/env python3
"""
fix-xrefs.py — Fix [???](#id) cross-reference artifacts in docs/.

Resolution strategies:
  LINK     → [Display Text](braised:ref/page-id)
  ANCHOR   → [Display Text](braised:ref/page-id#anchor)  (anchor on another page)
  GUC      → `param_name`  (GUC config parameters)
  BIBLIO   → plain text citation
  PLAIN    → plain text description

Usage:
    python3 fix-xrefs.py           # in-place, all docs/
    python3 fix-xrefs.py --dry-run # show diffs only
    python3 fix-xrefs.py path/to/file.md
"""

import difflib, os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), 'docs')

# ── Resolution table ──────────────────────────────────────────────────────────
# Keys are the fragment IDs (without leading #).
# Values are the replacement strings to substitute for [???](#id).

RESOLUTIONS: dict[str, str] = {
    # ── SQL commands (ref page titles) ───────────────────────────────────────
    'sql-createtype':             '[CREATE TYPE](braised:ref/sql-createtype)',
    'sql-altertable':             '[ALTER TABLE](braised:ref/sql-altertable)',
    'sql-createextension':        '[CREATE EXTENSION](braised:ref/sql-createextension)',
    'sql-createforeigndatawrapper': '[CREATE FOREIGN DATA WRAPPER](braised:ref/sql-createforeigndatawrapper)',

    # ── Chapter/section refs ─────────────────────────────────────────────────
    'ddl-priv':                   '[Section 5.8](braised:ref/ddl-priv)',
    'routine-vacuuming':          '[Section 24.1](braised:ref/routine-vacuuming)',
    'vacuum-for-statistics':      '[Section 24.1](braised:ref/routine-vacuuming)',
    'logfile-maintenance':        '[Section 24.3](braised:ref/logfile-maintenance)',
    'using-explain':              '[Section 14.1](braised:ref/using-explain)',
    'planner-stats':              '[Section 14.2](braised:ref/planner-stats)',
    'storage-page-layout':        '[Section 66.6](braised:ref/storage-page-layout)',
    'continuous-archiving':       '[Section 25.3](braised:ref/continuous-archiving)',
    'tablesample-support-functions': '[Section 59.1](braised:ref/tablesample-support-functions)',
    'protocol-replication':       '[Section 54.4](braised:ref/protocol-replication)',
    'logicaldecoding-sql':        '[Section 47.4](braised:ref/logicaldecoding-sql)',
    'logicaldecoding-walsender':  '[Section 47.3](braised:ref/logicaldecoding-walsender)',
    'logicaldecoding-writer':     '[Section 47.7](braised:ref/logicaldecoding-writer)',
    'oauth-validator-init':       '[Section 50.2](braised:ref/oauth-validator-init)',
    'oauth-validator-design':     '[Section 50.1](braised:ref/oauth-validator-design)',

    # ── Extending SQL ────────────────────────────────────────────────────────
    'xfunc':                      '[Section 36.3](braised:ref/xfunc)',
    'xaggr':                      '[Section 36.12](braised:ref/xaggr)',
    'xtypes':                     '[Section 36.13](braised:ref/xtypes)',
    'xoper':                      '[Section 36.14](braised:ref/xoper)',
    'xindex':                     '[Section 36.16](braised:ref/xindex)',
    'extend-extensions':          '[Section 36.17](braised:ref/extend-extensions)',

    # ── libpq ────────────────────────────────────────────────────────────────
    'libpq-envars':               '[Section 32.15](braised:ref/libpq-envars)',
    'libpq-pgpass':               '[Section 32.16](braised:ref/libpq-pgpass)',
    'libpq-ssl':                  '[Section 32.19](braised:ref/libpq-ssl)',
    'libpq-example':              '[Section 32.23](braised:ref/libpq-example)',

    # ── Localization ─────────────────────────────────────────────────────────
    'locale':                     '[Section 23.1](braised:ref/locale)',
    'collation':                  '[Section 23.2](braised:ref/collation)',
    'multibyte':                  '[Section 23.3](braised:ref/multibyte)',

    # ── Extensions / appendix F ──────────────────────────────────────────────
    'btree-gin':                  '[btree_gin](braised:ref/btree-gin)',
    'btree-gist':                 '[btree_gist](braised:ref/btree-gist)',
    'citext':                     '[citext](braised:ref/citext)',

    # ── Other tools / apps ───────────────────────────────────────────────────
    'app-pgbasebackup':           '[pg_basebackup](braised:ref/app-pgbasebackup)',

    # ── Monitoring ───────────────────────────────────────────────────────────
    'monitoring-stats':           '[Section 27.2](braised:ref/monitoring-stats)',
    'monitoring-stats-views-table': '[Section 27.2](braised:ref/monitoring-stats)',

    # ── Anchors without their own page (map to parent section) ───────────────
    'backup-archiving-wal':       '[Section 25.3](braised:ref/continuous-archiving)',
    'archive-module-init':        '[Section 49](braised:ref/archive-modules)',
    'archive-module-callbacks':   '[Section 49](braised:ref/archive-modules)',

    # ── Build / installation ─────────────────────────────────────────────────
    'build':                      '[Section 17.3](braised:ref/install-make)',

    # ── GUC config parameters → backtick name ────────────────────────────────
    'guc-archive-command':           '`archive_command`',
    'guc-archive-library':           '`archive_library`',
    'guc-log-error-verbosity':       '`log_error_verbosity`',
    'guc-shared-preload-libraries':  '`shared_preload_libraries`',

    # ── Additional apps ──────────────────────────────────────────────────────
    'app-pgverifybackup':            '[pg_verifybackup](braised:ref/app-pgverifybackup)',

    # ── SQL command anchors (map to parent page) ─────────────────────────────
    'sql-altertable-replica-identity': '[ALTER TABLE](braised:ref/sql-altertable)',

    # ── OAuth callbacks (anchor within section 50.3) ─────────────────────────
    'oauth-validator-callback-validate': '[Section 50.3](braised:ref/oauth-validator-callbacks)',

    # ── Appendix F extensions ────────────────────────────────────────────────
    'cube':            '[cube](braised:ref/cube)',
    'dict-int':        '[dict_int](braised:ref/dict-int)',
    'fuzzystrmatch':   '[fuzzystrmatch](braised:ref/fuzzystrmatch)',
    'hstore':          '[hstore](braised:ref/hstore)',
    'intarray':        '[intarray](braised:ref/intarray)',
    'isn':             '[isn](braised:ref/isn)',
    'lo':              '[lo](braised:ref/lo)',
    'ltree':           '[ltree](braised:ref/ltree)',
    'pgcrypto':        '[pgcrypto](braised:ref/pgcrypto)',
    'pgtrgm':          '[pg_trgm](braised:ref/pgtrgm)',
    'seg':             '[seg](braised:ref/seg)',
    'tablefunc':       '[tablefunc](braised:ref/tablefunc)',
    'tcn':             '[tcn](braised:ref/tcn)',
    'tsm-system-rows': '[tsm_system_rows](braised:ref/tsm-system-rows)',
    'tsm-system-time': '[tsm_system_time](braised:ref/tsm-system-time)',
    'unaccent':        '[unaccent](braised:ref/unaccent)',
    'uuid-ossp':       '[uuid-ossp](braised:ref/uuid-ossp)',

    # ── Bibliography refs → plain text ───────────────────────────────────────
    'ong90':   'Ong and Goh [1990]',
    'sim98':   'Simkovics [1998]',
    'ston90b': 'Stonebraker et al. [1990]',

    # ── Figure/table refs → plain text ───────────────────────────────────────
    'view-table': 'The following table',
}

# ── Regex: [???](#fragment-id) ────────────────────────────────────────────────
_XREF_RE = re.compile(r'\[\?\?\?\]\(#([A-Za-z0-9_-]+)\)')


def fix_line(line: str) -> tuple[str, list[str]]:
    """Replace [???](#id) tokens. Returns (fixed_line, list_of_unresolved_ids)."""
    unresolved: list[str] = []

    def _replace(m: re.Match) -> str:
        frag = m.group(1)
        if frag in RESOLUTIONS:
            return RESOLUTIONS[frag]
        unresolved.append(frag)
        return m.group(0)   # leave unchanged

    return _XREF_RE.sub(_replace, line), unresolved


def fix_file_lines(lines: list[str]) -> tuple[list[str], list[tuple[int, str]]]:
    """Process file lines. Returns (new_lines, [(lineno, unresolved_id), ...])."""
    out: list[str] = []
    unresolved: list[tuple[int, str]] = []
    in_fence = False

    for i, line in enumerate(lines, 1):
        s = line.rstrip()
        if re.match(r'^(`{3,}|~{3,})', s):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        new_line, ids = fix_line(line)
        out.append(new_line)
        for fid in ids:
            unresolved.append((i, fid))

    return out, unresolved


def process(path: str, dry_run: bool = False) -> tuple[bool, list[tuple[int, str]]]:
    original = open(path).readlines()
    new_lines, unresolved = fix_file_lines(original)
    changed = original != new_lines
    if changed and not dry_run:
        with open(path, 'w') as f:
            f.writelines(new_lines)
    return changed, unresolved


def show_diff(path: str) -> None:
    original = open(path).readlines()
    new_lines, _ = fix_file_lines(original)
    diff = list(difflib.unified_diff(original, new_lines,
                                     fromfile=path, tofile=path + ' (fixed)', n=2))
    if diff:
        sys.stdout.writelines(diff[:60])
        if len(diff) > 60:
            print(f'  … ({len(diff) - 60} more diff lines)')
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

    changed   = 0
    all_unres: list[tuple[str, int, str]] = []   # (rel_path, lineno, id)

    for path in paths:
        rel = os.path.relpath(path, DOCS)
        if dry_run:
            show_diff(path)
            original = open(path).readlines()
            _, unresolved = fix_file_lines(original)
            original2 = open(path).readlines()
            new_lines, _ = fix_file_lines(original2)
            if original2 != new_lines:
                changed += 1
        else:
            did_change, unresolved = process(path, dry_run=False)
            if did_change:
                changed += 1
        for lineno, fid in ([] if 'unresolved' not in dir() else unresolved):
            all_unres.append((rel, lineno, fid))

    verb = 'would change' if dry_run else 'changed'
    print(f'{verb}: {changed}/{len(paths)} files')

    if all_unres:
        print(f'\nUnresolved XREFs ({len(all_unres)}):')
        for rel, lineno, fid in sorted(all_unres):
            print(f'  {rel}:{lineno}  #{fid}')


if __name__ == '__main__':
    main()
