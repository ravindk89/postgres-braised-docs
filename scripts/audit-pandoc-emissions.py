#!/usr/bin/env python3
"""
audit-pandoc-emissions.py — scan converted markdown for pandoc-specific constructs.

Catalogs every non-standard pattern that needs transformation before the docs
will render correctly in Braised, with counts, file counts, and examples.

Usage:
    python3 audit-pandoc-emissions.py [--docs ./docs] [--examples N]
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

DOCS_DIR  = "./docs"
N_EXAMPLES = 3  # examples to show per pattern

# ── Patterns ──────────────────────────────────────────────────────────────────

# Each entry: (name, description, fn(lines, path) -> list of Match)
# Match = {"line": int, "text": str, "context": str}

class Match:
    def __init__(self, lineno, text, context=""):
        self.lineno  = lineno
        self.text    = text.rstrip()
        self.context = context  # a few lines of surrounding text


# ── 1. Fenced divs (::: word) ─────────────────────────────────────────────────

KNOWN_BRAISED_DIVS = {"synopsis"}  # these are fine as-is

CALLOUT_DIVS = {"note", "tip", "warning", "caution", "important"}

def scan_fenced_divs(lines, path):
    """Find :::word fenced div openings that are NOT Braised-native."""
    results = defaultdict(list)
    for i, line in enumerate(lines):
        m = re.match(r'^:::\s*(\w[\w-]*)\s*$', line)
        if not m:
            continue
        name = m.group(1).lower()
        if name in KNOWN_BRAISED_DIVS:
            continue
        ctx = "\n".join(lines[i:min(i+4, len(lines))])
        results[name].append(Match(i+1, line, ctx))
    return results  # {div_name: [Match]}


# ── 2. Nested :::title inside callouts ───────────────────────────────────────

def scan_nested_title(lines, path):
    matches = []
    for i, line in enumerate(lines):
        if re.match(r'^::: title\s*$', line):
            ctx = "\n".join(lines[max(0,i-1):min(i+4, len(lines))])
            matches.append(Match(i+1, line, ctx))
    return matches


# ── 3. Broken xrefs [???](#id) ────────────────────────────────────────────────

XREF_RE = re.compile(r'\[\?\?\?\]\(#([^)]+)\)')

def scan_xrefs(lines, path):
    by_target = defaultdict(list)
    for i, line in enumerate(lines):
        for m in XREF_RE.finditer(line):
            by_target[m.group(1)].append(Match(i+1, line.strip()))
    return by_target  # {target_id: [Match]}


# ── 4. Grid tables (+---+) ────────────────────────────────────────────────────

def scan_grid_tables(lines, path):
    matches = []
    i = 0
    while i < len(lines):
        if re.match(r'^\+[-=+]+\+', lines[i]):
            ctx = "\n".join(lines[i:min(i+5, len(lines))])
            matches.append(Match(i+1, lines[i], ctx))
            # skip to end of table
            while i < len(lines) and re.match(r'^\+[-=|+]', lines[i]):
                i += 1
        else:
            i += 1
    return matches


# ── 5. Simple (pandoc) tables (  ---- style) ─────────────────────────────────

def scan_simple_tables(lines, path):
    matches = []
    i = 0
    while i < len(lines):
        if re.match(r'^  -+(\s+-+)+\s*$', lines[i]):
            ctx = "\n".join(lines[max(0,i-1):min(i+4, len(lines))])
            matches.append(Match(i+1, lines[i], ctx))
            while i < len(lines) and re.match(r'^  -', lines[i]):
                i += 1
        else:
            i += 1
    return matches


# ── 6. Pipe tables with caption (: Caption) ───────────────────────────────────

def scan_table_captions(lines, path):
    matches = []
    for i, line in enumerate(lines):
        if re.match(r'^:\s+\S', line) and i > 0 and re.match(r'^\|', lines[i-1]):
            matches.append(Match(i+1, line.strip()))
    return matches


# ── Aggregate and report ──────────────────────────────────────────────────────

def scan_file(path, all_stats):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    relpath = str(path)

    # Fenced divs
    divs = scan_fenced_divs(lines, path)
    for name, matches in divs.items():
        key = f"fenced-div:::{name}"
        all_stats[key]["files"].add(relpath)
        all_stats[key]["count"] += len(matches)
        all_stats[key]["examples"].extend(
            (relpath, m) for m in matches[:N_EXAMPLES]
            if len(all_stats[key]["examples"]) < N_EXAMPLES
        )

    # Nested titles
    nt = scan_nested_title(lines, path)
    if nt:
        key = "nested-title-div"
        all_stats[key]["files"].add(relpath)
        all_stats[key]["count"] += len(nt)
        if len(all_stats[key]["examples"]) < N_EXAMPLES:
            all_stats[key]["examples"].append((relpath, nt[0]))

    # Broken xrefs
    xrefs = scan_xrefs(lines, path)
    total_xrefs = sum(len(v) for v in xrefs.values())
    if total_xrefs:
        key = "broken-xref"
        all_stats[key]["files"].add(relpath)
        all_stats[key]["count"] += total_xrefs
        all_stats[key]["xref_targets"].update(xrefs.keys())
        if len(all_stats[key]["examples"]) < N_EXAMPLES:
            for target, matches in list(xrefs.items())[:1]:
                all_stats[key]["examples"].append((relpath, matches[0]))

    # Grid tables
    gt = scan_grid_tables(lines, path)
    if gt:
        key = "grid-table"
        all_stats[key]["files"].add(relpath)
        all_stats[key]["count"] += len(gt)
        if len(all_stats[key]["examples"]) < N_EXAMPLES:
            all_stats[key]["examples"].append((relpath, gt[0]))

    # Simple tables
    st = scan_simple_tables(lines, path)
    if st:
        key = "simple-table"
        all_stats[key]["files"].add(relpath)
        all_stats[key]["count"] += len(st)
        if len(all_stats[key]["examples"]) < N_EXAMPLES:
            all_stats[key]["examples"].append((relpath, st[0]))

    # Table captions
    tc = scan_table_captions(lines, path)
    if tc:
        key = "table-caption"
        all_stats[key]["files"].add(relpath)
        all_stats[key]["count"] += len(tc)
        if len(all_stats[key]["examples"]) < N_EXAMPLES:
            all_stats[key]["examples"].append((relpath, tc[0]))


def new_stat():
    return {"files": set(), "count": 0, "examples": [], "xref_targets": set()}


def main():
    docs = DOCS_DIR
    for a in sys.argv[1:]:
        if a.startswith("--docs="):
            docs = a.split("=", 1)[1]
        elif a == "--docs":
            idx = sys.argv.index("--docs")
            docs = sys.argv[idx+1]

    all_stats = defaultdict(new_stat)

    md_files = list(Path(docs).rglob("*.md"))
    print(f"Scanning {len(md_files)} files in {docs}/\n", file=sys.stderr)

    for path in md_files:
        scan_file(path, all_stats)

    # Sort by count descending
    sorted_keys = sorted(all_stats.keys(), key=lambda k: -all_stats[k]["count"])

    print(f"{'='*70}")
    print(f"PANDOC EMISSION AUDIT — {len(md_files)} files")
    print(f"{'='*70}\n")

    for key in sorted_keys:
        s = all_stats[key]
        print(f"[ {key} ]")
        print(f"  occurrences : {s['count']}")
        print(f"  files       : {len(s['files'])}")

        if s.get("xref_targets"):
            top = sorted(s["xref_targets"])[:8]
            print(f"  top targets : {', '.join(top)}" +
                  (" ..." if len(s["xref_targets"]) > 8 else ""))

        if s["examples"]:
            print(f"  examples:")
            seen = set()
            for fpath, m in s["examples"]:
                if fpath in seen:
                    continue
                seen.add(fpath)
                short = fpath.replace(docs + "/", "")
                print(f"    {short}:{m.lineno}")
                if m.context:
                    for ctx_line in m.context.splitlines()[:4]:
                        print(f"      | {ctx_line}")
                elif m.text:
                    print(f"      | {m.text[:100]}")
        print()

    # Summary table
    print(f"{'─'*70}")
    print(f"{'Pattern':<30} {'Count':>8}  {'Files':>6}  Action")
    print(f"{'─'*70}")

    actions = {
        "fenced-div:::note":          "→ :::{.callout type=\"note\"}",
        "fenced-div:::tip":           "→ :::{.callout type=\"tip\"}",
        "fenced-div:::warning":       "→ :::{.callout type=\"warning\"}",
        "fenced-div:::caution":       "→ :::{.callout type=\"caution\"}",
        "fenced-div:::important":     "→ :::{.callout type=\"important\"}",
        "fenced-div:::formalpara-title": "→ strip wrapper, keep bold text",
        "nested-title-div":           "→ hoist title into callout prop",
        "broken-xref":                "→ resolve from id→title map or strip",
        "grid-table":                 "→ convert to pipe table",
        "simple-table":               "→ convert to pipe table",
        "table-caption":              "→ strip or convert to HTML caption",
    }

    for key in sorted_keys:
        s = all_stats[key]
        action = actions.get(key, "→ investigate")
        print(f"  {key:<28} {s['count']:>8}  {len(s['files']):>6}  {action}")

    print()


if __name__ == "__main__":
    main()
