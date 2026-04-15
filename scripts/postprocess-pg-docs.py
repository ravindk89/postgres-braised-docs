#!/usr/bin/env python3
"""
postprocess-pg-docs.py — clean up pandoc emissions in converted PostgreSQL docs.

Transformations (applied per file in order):
  1. Nested ::: title inside callout → hoist to title= prop
  2. Callout divs (::: note/tip/warning/caution/important) → :::{.callout type="..."}
  3. formalpara-title divs → strip wrapper, keep inner text
  4. Grid tables (+---+) → :::table blocks
  5. Simple (pandoc) tables → :::table blocks
  6. Broken xrefs [???](#id) → resolved title + braised:ref/ link

Xref resolution tiers:
  a. ID in page-level map  → [Title](braised:ref/id)
  b. ID found in XML, ancestor is a known page
     → [Title](braised:ref/page-id#goldmark-anchor)
  c. ID found in XML, no page ancestor
     → [Title](#goldmark-anchor)
  d. ID not in XML → leave unchanged, emit warning

Usage:
    python3 postprocess-pg-docs.py [--docs ./docs] [--xml postgres-full.xml] [--dry-run] [--verbose]
"""

import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

DOCS_DIR = "./docs"
FULL_XML = "./postgres-full.xml"
DRY_RUN  = False
VERBOSE  = False

CALLOUT_TYPES = {"note", "tip", "warning", "caution", "important"}



def log(msg):
    if VERBOSE:
        print(msg, file=sys.stderr)


def warn(msg):
    print(f"WARN  {msg}", file=sys.stderr)


# ── Goldmark heading ID ───────────────────────────────────────────────────────

def goldmark_id(text):
    """Compute the heading ID goldmark's WithAutoHeadingID extension would generate.
    Algorithm: lowercase, replace runs of non-alphanumeric chars with '-', strip edges."""
    t = text.lower()
    t = re.sub(r'[^a-z0-9]+', '-', t)
    return t.strip('-')


# ── Pre-pass 1: Page-level ID map ─────────────────────────────────────────────

def build_page_id_map(docs_dir):
    """Scan all .md files for id: and title: frontmatter.
    Returns {docbook_id: {"path": Path, "title": str}}."""
    page_map = {}
    for f in Path(docs_dir).rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
        if not m:
            continue
        fm = m.group(1)
        id_m   = re.search(r'^id:\s*(.+)$', fm, re.MULTILINE)
        title_m = re.search(r'^title:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
        if id_m:
            doc_id = id_m.group(1).strip()
            title  = title_m.group(1).strip() if title_m else doc_id
            # Strip chapter numbering from titles ("13.3. Explicit Locking" → "Explicit Locking")
            title = re.sub(r'^[\dIVXivx]+[\d.]*\.\s+', '', title)
            page_map[doc_id] = {"path": f, "title": title}
    return page_map


# ── Pre-pass 2: XML ID map ────────────────────────────────────────────────────

def extract_title_from_elem(elem):
    """Extract a human-readable title from any DocBook element."""
    # Try <title> child first
    t = elem.find('title')
    if t is not None:
        return ''.join(t.itertext()).strip()
    # <refname> (refentry)
    rn = elem.find('.//refname')
    if rn is not None:
        return ''.join(rn.itertext()).strip()
    # <term> (varlistentry / GUC params)
    term = elem.find('term')
    if term is not None:
        return ''.join(term.itertext()).strip()
    return None


def build_xml_id_map(xml_root):
    """Walk XML and collect {id: {"title": str, "elem": elem, "tag": str}}.
    Also builds a parent_map for ancestor traversal."""
    parent_map = {}
    for parent in xml_root.iter():
        for child in parent:
            parent_map[child] = parent

    id_map = {}
    for elem in xml_root.iter():
        eid = elem.get('id')
        if not eid:
            continue
        title = extract_title_from_elem(elem)
        id_map[eid] = {"title": title, "elem": elem, "tag": elem.tag}

    return id_map, parent_map


def find_containing_page(elem, page_ids, parent_map):
    """Walk ancestor chain to find the nearest DocBook ID that is a known Braised page."""
    current = parent_map.get(elem)
    while current is not None:
        cid = current.get('id')
        if cid and cid in page_ids:
            return cid
        current = parent_map.get(current)
    return None


# ── Xref resolver ─────────────────────────────────────────────────────────────

class XrefResolver:
    def __init__(self, page_map, xml_id_map, parent_map):
        self.page_map   = page_map    # {id: {"path", "title"}}
        self.xml_id_map = xml_id_map  # {id: {"title", "elem", "tag"}}
        self.parent_map = parent_map
        self.unresolved = defaultdict(list)  # {id: [src_file]}

    def resolve(self, target_id, src_file):
        """Return replacement markdown string for [???](#target_id)."""
        # Tier a: page-level ID
        if target_id in self.page_map:
            title = self.page_map[target_id]["title"]
            return f"[{title}](braised:ref/{target_id})"

        # Tier b/c: in XML
        if target_id in self.xml_id_map:
            entry = self.xml_id_map[target_id]
            title = entry["title"] or target_id
            elem  = entry["elem"]

            # Compute what goldmark will generate for the heading anchor
            anchor = goldmark_id(title) if title else target_id

            # Find containing page
            page_id = find_containing_page(elem, self.page_map, self.parent_map)
            if page_id:
                return f"[{title}](braised:ref/{page_id}#{anchor})"
            else:
                return f"[{title}](#{anchor})"

        # Tier d: unknown
        self.unresolved[target_id].append(str(src_file))
        return f"[???](#{target_id})"  # leave as-is with original fragment

    def report(self):
        if self.unresolved:
            print(f"\nUnresolved xref IDs ({len(self.unresolved)}):", file=sys.stderr)
            for xid, files in sorted(self.unresolved.items())[:20]:
                print(f"  {xid}  ({len(files)} file(s))", file=sys.stderr)
            if len(self.unresolved) > 20:
                print(f"  ... and {len(self.unresolved)-20} more", file=sys.stderr)


# ── Transformation 1–3: Callouts and formalpara ───────────────────────────────

def transform_callouts(lines):
    """
    1. Nested ::: title → hoist into parent callout title= prop
    2. ::: note/tip/etc → :::{.callout type="..."}
    3. ::: formalpara-title wrapper → strip, keep inner text
    """
    # Pass 1: hoist nested titles
    # Pattern: ::: <callout>\n::: title\n<text>\n:::\n
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^:::\s*(note|tip|warning|caution|important)\s*$', line, re.IGNORECASE)
        if m and i + 3 < len(lines):
            ctype = m.group(1).lower()
            if re.match(r'^:::\s*title\s*$', lines[i+1], re.IGNORECASE):
                title_text = lines[i+2].strip()
                if re.match(r'^:::\s*$', lines[i+3]):
                    # Hoist: emit single open line with title prop
                    out.append(f':::{{{".callout"} type="{ctype}" title="{title_text}"}}')
                    i += 4
                    continue
        out.append(line)
        i += 1
    lines = out

    # Pass 2: plain callout divs → :::{.callout type="..."}
    out = []
    for line in lines:
        m = re.match(r'^:::\s*(note|tip|warning|caution|important)\s*$', line, re.IGNORECASE)
        if m:
            ctype = m.group(1).lower()
            out.append(f':::{{{".callout"} type="{ctype}"}}')
        else:
            out.append(line)
    lines = out

    # Pass 3: formalpara-title — remove wrapper, keep inner text only
    out = []
    i = 0
    while i < len(lines):
        if re.match(r'^:::\s*formalpara-title\s*$', lines[i], re.IGNORECASE):
            # Skip the opening line; emit content lines until the closing :::
            i += 1
            while i < len(lines):
                if re.match(r'^:::\s*$', lines[i]):
                    i += 1
                    break
                out.append(lines[i])
                i += 1
        else:
            out.append(lines[i])
            i += 1

    return out


# ── Grid table parser ─────────────────────────────────────────────────────────

def parse_grid_table(lines, start):
    """Parse a grid table. Returns (rows, end_index).
    rows = [{"header": bool, "cells": [str]}]
    Each cell string may contain newlines (multiline content).
    """
    i = start
    # Collect all table lines (separator lines and cell content lines)
    table_lines = []
    while i < len(lines):
        ln = lines[i]
        if re.match(r'^\+[-=+]+\+', ln) or (table_lines and re.match(r'^\|', ln)):
            table_lines.append(ln)
            i += 1
        else:
            break

    if not table_lines:
        return [], start

    # Column positions from the first separator line
    first_sep = table_lines[0]
    col_pos = [j for j, c in enumerate(first_sep) if c == '+']
    if len(col_pos) < 2:
        return [], start  # malformed
    n_cols = len(col_pos) - 1

    # Parse rows
    rows = []
    in_header = True
    cur_cells = [[] for _ in range(n_cols)]  # list of content lines per col

    def flush_row(is_header):
        cells = []
        for col_lines in cur_cells:
            # Strip per-line padding, preserve paragraph structure
            stripped = [ln.rstrip() for ln in col_lines]
            # Remove leading/trailing blank lines
            while stripped and not stripped[0]:
                stripped.pop(0)
            while stripped and not stripped[-1]:
                stripped.pop()
            cells.append('\n'.join(stripped))
        if any(c.strip() for c in cells):
            rows.append({"header": is_header, "cells": cells})

    for ln in table_lines:
        if ln.startswith('+'):
            flush_row(in_header)
            cur_cells = [[] for _ in range(n_cols)]
            if '=' in ln:
                in_header = False
        elif ln.startswith('|'):
            for col_idx in range(n_cols):
                s = col_pos[col_idx] + 1
                e = col_pos[col_idx + 1]
                if s < len(ln):
                    chunk = ln[s:e] if e <= len(ln) else ln[s:]
                    cur_cells[col_idx].append(chunk.rstrip())

    return rows, i


def table_to_braised(rows):
    """Convert parsed rows to :::table block markdown."""
    if not rows:
        return []
    out = [':::{.table}']
    for row in rows:
        header_attr = ' header="true"' if row["header"] else ''
        if row["header"]:
            out.append(f'  :::{{{".row"} header="true"}}')
        else:
            out.append('  :::{.row}')
        for cell in row["cells"]:
            out.append('  :::{.cell}')
            # Indent cell content 2 spaces
            for line in cell.splitlines():
                out.append(f'  {line}' if line.strip() else '')
            out.append('  :::')
        out.append('  :::{/row}')
    out.append(':::{/table}')
    return out


# ── Simple table parser ───────────────────────────────────────────────────────

def parse_simple_table(lines, start):
    """Parse a pandoc simple table.
    Returns (rows, end_index).
    """
    i = start
    # Find the separator line (dashes)
    sep_idx = None
    j = i
    while j < len(lines) and j < i + 5:
        if re.match(r'^  -+(\s+-+)+\s*$', lines[j]) or re.match(r'^  =+(\s+=+)+\s*$', lines[j]):
            sep_idx = j
            break
        j += 1
    if sep_idx is None:
        return [], start

    sep_line = lines[sep_idx]
    # Find column ranges from separator
    # Each column is a run of dashes/equals, separated by spaces
    col_ranges = []
    for m in re.finditer(r'-+|=+', sep_line):
        col_ranges.append((m.start(), m.end()))

    if not col_ranges:
        return [], start

    def extract_cols(line, ranges):
        cells = []
        for s, e in ranges:
            if s < len(line):
                cell = line[s:e].strip() if e <= len(line) else line[s:].strip()
                cells.append(cell)
            else:
                cells.append('')
        return cells

    rows = []
    # Header: lines between start and sep_idx
    for li in range(i, sep_idx):
        cells = extract_cols(lines[li], col_ranges)
        if any(c.strip() for c in cells):
            rows.append({"header": True, "cells": cells})

    # Body: lines after sep_idx until blank line or another separator
    end = sep_idx + 1
    while end < len(lines):
        ln = lines[end]
        if not ln.strip():
            end += 1
            break
        if re.match(r'^  -+(\s+-+)+\s*$', ln) or re.match(r'^  =+(\s+=+)+\s*$', ln):
            end += 1
            break
        cells = extract_cols(ln, col_ranges)
        if any(c.strip() for c in cells):
            rows.append({"header": False, "cells": cells})
        end += 1

    return rows, end


# ── Transformation 4+5: Tables ────────────────────────────────────────────────

def transform_tables(lines):
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        # Grid table: starts with +--
        if re.match(r'^\+[-=+]+\+', ln):
            rows, new_i = parse_grid_table(lines, i)
            if rows:
                out.extend(table_to_braised(rows))
                out.append('')
                i = new_i
                continue
        # Simple table: separator line at this or next line
        if re.match(r'^  -+(\s+-+)+\s*$', ln) or (
            i + 1 < len(lines) and re.match(r'^  -+(\s+-+)+\s*$', lines[i + 1])
        ):
            # Back up one line if the separator is the next line
            table_start = i if re.match(r'^  -+(\s+-+)+\s*$', ln) else i
            if re.match(r'^  -+(\s+-+)+\s*$', lines[i + 1] if i + 1 < len(lines) else ''):
                table_start = i
            rows, new_i = parse_simple_table(lines, table_start)
            if rows:
                out.extend(table_to_braised(rows))
                out.append('')
                i = new_i
                continue
        out.append(ln)
        i += 1
    return out


# ── Transformation 6: Broken xrefs ───────────────────────────────────────────

XREF_RE = re.compile(r'\[\?\?\?\]\(#([^)]+)\)')

def transform_xrefs(lines, resolver, src_file):
    out = []
    for line in lines:
        def replace(m):
            return resolver.resolve(m.group(1), src_file)
        out.append(XREF_RE.sub(replace, line))
    return out


# ── Per-file pipeline ─────────────────────────────────────────────────────────

def process_file(path, resolver):
    text  = path.read_text(encoding='utf-8')
    lines = text.splitlines()

    lines = transform_callouts(lines)
    lines = transform_tables(lines)
    lines = transform_xrefs(lines, resolver, path)

    result = '\n'.join(lines)
    if not result.endswith('\n'):
        result += '\n'
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    global DOCS_DIR, FULL_XML, DRY_RUN, VERBOSE

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--docs' and i + 1 < len(args):
            DOCS_DIR = args[i + 1]; i += 2
        elif a.startswith('--docs='):
            DOCS_DIR = a.split('=', 1)[1]; i += 1
        elif a == '--xml' and i + 1 < len(args):
            FULL_XML = args[i + 1]; i += 2
        elif a.startswith('--xml='):
            FULL_XML = a.split('=', 1)[1]; i += 1
        elif a == '--dry-run':
            DRY_RUN = True; i += 1
        elif a == '--verbose':
            VERBOSE = True; i += 1
        else:
            i += 1

    print("Building page ID map ...", file=sys.stderr)
    page_map = build_page_id_map(DOCS_DIR)
    print(f"  {len(page_map)} page-level IDs", file=sys.stderr)

    print("Parsing XML ...", file=sys.stderr)
    with open(FULL_XML) as f:
        content = f.read()
    content = re.sub(r'<!DOCTYPE[^[>]*(?:\[[^\]]*\])?\s*>', '', content, flags=re.DOTALL)
    xml_root = ET.fromstring(content)
    xml_id_map, parent_map = build_xml_id_map(xml_root)
    print(f"  {len(xml_id_map)} IDs in XML", file=sys.stderr)

    resolver = XrefResolver(page_map, xml_id_map, parent_map)

    md_files = sorted(Path(DOCS_DIR).rglob("*.md"))
    print(f"Processing {len(md_files)} files ...", file=sys.stderr)

    changed = 0
    for path in md_files:
        original = path.read_text(encoding='utf-8')
        result   = process_file(path, resolver)
        if result != original:
            changed += 1
            log(f"  changed: {path}")
            if not DRY_RUN:
                path.write_text(result, encoding='utf-8')

    resolver.report()
    status = "(dry run)" if DRY_RUN else ""
    print(f"\nDone {status}. {changed}/{len(md_files)} files changed.", file=sys.stderr)


if __name__ == "__main__":
    main()
