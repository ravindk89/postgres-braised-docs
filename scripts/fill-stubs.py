#!/usr/bin/env python3
"""
fill-stubs.py — Populate stub index.md files with intro content from postgres-full.xml.

For each stub index.md (≤4 lines of frontmatter only), finds the corresponding
part or chapter element in the DocBook XML, extracts its partintro / intro paras,
converts them to Markdown via pandoc, and writes them into the file.

Usage:
    python3 fill-stubs.py [--dry-run]
"""

import glob
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

DOCS    = "/home/rkumar/braised-projects/postgres-braised-docs/docs"
XML     = "/home/rkumar/braised-projects/postgres-braised-docs/postgres-full.xml"
DRY_RUN = "--dry-run" in sys.argv

# ── XML loading ───────────────────────────────────────────────────────────────

def load_xml():
    print("parsing XML...", file=sys.stderr)
    with open(XML) as f:
        content = f.read()
    content = re.sub(r'<!DOCTYPE[^[>]*(?:\[[\s\S]*?\])?\s*>', '', content)
    return ET.fromstring(content)


def find_by_id(root, doc_id):
    for elem in root.iter():
        if elem.get('id') == doc_id:
            return elem
    return None


# ── Pandoc helpers (same approach as convert-pg-docs.py) ─────────────────────

WRAP = '<book xmlns="http://docbook.org/ns/docbook" version="5.0">{}</book>'

def strip_indexterms(elem):
    for parent in elem.iter():
        to_remove = [c for c in list(parent) if c.tag == 'indexterm']
        for child in to_remove:
            parent.remove(child)


def to_markdown(elem):
    strip_indexterms(elem)
    xml_str = WRAP.format(ET.tostring(elem, encoding='unicode'))
    result = subprocess.run(
        ["pandoc", "-f", "docbook", "-t", "markdown", "--wrap=none"],
        input=xml_str, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, result.stderr
    return result.stdout.strip(), None


_XREF_MAP = None  # built lazily

def _build_xref_map():
    """Build id → (title, braised_rel_path) from pg-docs-tree.json."""
    import json
    global _XREF_MAP
    if _XREF_MAP is not None:
        return _XREF_MAP

    with open("/home/rkumar/braised-projects/postgres-braised-docs/pg-docs-tree.json") as f:
        tree_data = json.load(f)

    def s(title):
        t = re.sub(r'^[IVXivx]+\.\s*', '', title)
        t = re.sub(r'^\d+[\d.]*\.\s*', '', t)
        return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

    REFERENCE_FOLDER_MAP = {
        "I. SQL Commands":                     "sql-commands",
        "II. PostgreSQL Client Applications":  "client-apps",
        "III. PostgreSQL Server Applications": "server-apps",
    }

    m = {}
    for part in tree_data.get('tree', []):
        purl   = part.get('url', '')
        ptitle = part.get('title', '')
        ptype  = part.get('type', '')
        pslug  = s(ptitle)
        pid    = purl.rstrip('/').split('/')[-1].replace('.html', '').split('#')[0]
        m[pid] = (ptitle, f"{pslug}/index.md")
        for ch in part.get('children', []):
            curl   = ch.get('url', '')
            ctitle = ch.get('title', '')
            cslug  = s(ctitle)
            cid    = curl.rstrip('/').split('/')[-1].replace('.html', '').split('#')[0]
            if ptype == 'part' and ptitle.startswith('VI.'):
                folder = REFERENCE_FOLDER_MAP.get(ctitle)
                if folder:
                    m[cid] = (ctitle, f"reference/{folder}/index.md")
                    continue
            m[cid] = (ctitle, f"{pslug}/{cslug}/index.md")
    _XREF_MAP = m
    return m


def clean_markdown(md):
    # Fix <replaceable> rendered as \<text\> → *text*
    md = re.sub(r'\\<([^\\>]+)\\>', r'*\1*', md)
    # Fix `` `text` {.replaceable} `` → *text*
    md = re.sub(r'`([^`]+)`\s*\{\.replaceable\}', r'*\1*', md)
    # Remove empty anchor links like []{#...}
    md = re.sub(r'\[\]\{#[^}]+\}', '', md)
    # Clean up productname / application wrapping
    md = re.sub(r'`([^`]+)`\{\.(?:productname|application|command|filename|literal)\}', r'`\1`', md)
    # Resolve [???](#id) xref links from DocBook <xref linkend="..."/>
    xmap = _build_xref_map()
    def resolve_xref(m):
        xid = m.group(1)
        if xid in xmap:
            title, path = xmap[xid]
            return f"[{title}](braised:ref/{xid})"
        # Unknown id — likely a bibliography citation or anchor-only ref; drop the link
        return ""
    md = re.sub(r'\[\?\?\?\]\(#([^)]+)\)', resolve_xref, md)
    # Drop empty headings (pandoc artifact: "## " with no title text)
    md = re.sub(r'^#{1,6}\s*$', '', md, flags=re.MULTILINE)
    # Drop any remaining empty attribute spans
    md = re.sub(r'\[\]\{[^}]*\}', '', md)
    # Collapse multiple blank lines left by removals
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


# ── Intro extraction ──────────────────────────────────────────────────────────

def get_intro_xml(elem):
    """Return an XML element containing intro content, or None."""
    tag = elem.tag

    # Parts have <partintro>
    if tag == 'part':
        pi = elem.find('partintro')
        if pi is not None and len(list(pi)) > 0:
            return pi
        return None

    # Chapters / appendixes / preface: look for direct <para> children
    # before the first <sect1>/<section>/<refentry>
    intro_kids = []
    for child in elem:
        if child.tag in ('title', 'titleabbrev', 'indexterm', 'toc'):
            continue
        if child.tag in ('sect1', 'section', 'refentry', 'simplesect'):
            break
        intro_kids.append(child)

    if not intro_kids:
        return None

    # Wrap in a <section> for pandoc
    wrapper = ET.Element('section')
    for k in intro_kids:
        wrapper.append(k)
    return wrapper


# ── Frontmatter helpers ───────────────────────────────────────────────────────

def is_stub(path):
    with open(path) as f:
        content = f.read()
    lines = [l for l in content.splitlines() if l.strip()]
    # A stub has only frontmatter (---, title, ---) and nothing else
    if '---' not in content:
        return True
    # Remove frontmatter block and check what's left
    parts = content.split('---')
    if len(parts) < 3:
        return True
    body = '---'.join(parts[2:]).strip()
    return len(body) == 0


def append_content(path, md_body):
    with open(path) as f:
        existing = f.read().rstrip()
    with open(path, 'w') as f:
        f.write(existing + '\n\n' + md_body + '\n')


# ── Doc-id derivation ─────────────────────────────────────────────────────────
# We derive the XML id from the nav.yaml path field, which was originally
# the postgres.org URL slug (e.g. "tutorial.html" → id "tutorial").
# For index.md files we need to look at the parent nav entry.

def build_path_to_id_map():
    """Parse nav.yaml to build {rel_path → xml_id} for container nodes."""
    import yaml
    with open("/home/rkumar/braised-projects/postgres-braised-docs/nav.yaml") as f:
        data = yaml.safe_load(f)
    mapping = {}

    def walk(nodes):
        for node in nodes:
            path = node.get('path', '')
            # The original URL was stored in pg-docs-tree.json; nav.yaml was
            # generated from it.  The xml id is the slug part of the original URL.
            # We stored it as the path; derive id from children or title.
            # Actually: the original convert-pg-docs.py used the URL fragment as id.
            # We'll derive it separately via the XML scan.
            if path:
                mapping[path] = None  # placeholder; we'll match by title below
            for child in node.get('children', []):
                walk([child])

    walk(data.get('nav', data))
    return mapping


def build_title_to_elem(root):
    """Build {lower_title → elem} for all part/chapter/appendix/preface elements."""
    result = {}
    for elem in root.iter():
        if elem.tag not in ('part', 'chapter', 'appendix', 'preface', 'bibliography',
                             'colophon', 'index'):
            continue
        title_el = elem.find('title')
        if title_el is None:
            continue
        # Full text of title (may have productname etc.)
        title_text = ''.join(title_el.itertext()).strip()
        result[title_text.lower()] = elem
        # Also store by id
        eid = elem.get('id', '')
        if eid:
            result[f'__id__{eid}'] = elem
    return result


def path_to_xml_id(rel_path):
    """
    Derive the expected DocBook xml:id from the directory path.
    e.g. "tutorial/index.md"           → "tutorial"
         "the-sql-language/index.md"   → "sql"
         "server-administration/..."   → "admin"

    These were set during the original crawl. We use the pg-docs-tree.json
    to get the canonical URL and strip the .html suffix for the id.
    """
    import json
    with open("/home/rkumar/braised-projects/postgres-braised-docs/pg-docs-tree.json") as f:
        tree_data = json.load(f)

    # Build slug → url map from the tree
    def collect(nodes, depth=0):
        for node in nodes:
            yield node, depth
            for child in node.get('children', []):
                yield from collect([child], depth + 1)

    # Derive the "braised path" for each node the same way convert-pg-docs.py does
    def slug(title):
        t = re.sub(r'^[IVXivx]+\.\s*', '', title)
        t = re.sub(r'^\d+[\d.]*\.\s*', '', t)
        return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

    # Build a mapping: braised_path → xml_id
    path_map = {}

    parts = tree_data.get('tree', [])
    for part_node in parts:
        ptype = part_node.get('type', '')
        ptitle = part_node.get('title', '')
        purl = part_node.get('url', '')
        pslug = slug(ptitle)
        xml_id = purl.rstrip('/').split('/')[-1].replace('.html', '').split('#')[0]

        path_map[f"{pslug}/index.md"] = xml_id

        for chapter in part_node.get('children', []):
            ctype = chapter.get('type', '')
            ctitle = chapter.get('title', '')
            curl = chapter.get('url', '')
            cslug = slug(ctitle)
            cxml_id = curl.rstrip('/').split('/')[-1].replace('.html', '').split('#')[0]

            # Handle reference folder remapping
            from convert_pg_docs_helper import REFERENCE_FOLDER_MAP
            # Actually just use the slug approach
            if ptype in ('part',) and ptitle.startswith('VI.'):
                # Reference sections live in reference/sql-commands etc.
                pass

            path_map[f"{pslug}/{cslug}/index.md"] = cxml_id

    return path_map


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    import json, yaml

    xml_root = load_xml()

    # Build path → xml_id map from the tree
    with open("/home/rkumar/braised-projects/postgres-braised-docs/pg-docs-tree.json") as f:
        tree_data = json.load(f)

    def slug(title):
        t = re.sub(r'^[IVXivx]+\.\s*', '', title)
        t = re.sub(r'^\d+[\d.]*\.\s*', '', t)
        return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

    REFERENCE_FOLDER_MAP = {
        "I. SQL Commands":                     "sql-commands",
        "II. PostgreSQL Client Applications":  "client-apps",
        "III. PostgreSQL Server Applications": "server-apps",
    }

    path_map = {}  # rel_path → xml_id

    parts = tree_data.get('tree', [])
    for part_node in parts:
        ptitle = part_node.get('title', '')
        purl   = part_node.get('url', '')
        pslug  = slug(ptitle)
        ptype  = part_node.get('type', '')
        pxml_id = purl.rstrip('/').split('/')[-1].replace('.html', '').split('#')[0]

        path_map[f"{pslug}/index.md"] = pxml_id

        for chapter in part_node.get('children', []):
            ctitle = chapter.get('title', '')
            curl   = chapter.get('url', '')
            cslug  = slug(ctitle)
            cxml_id = curl.rstrip('/').split('/')[-1].replace('.html', '').split('#')[0]

            # Reference part uses special folder structure
            if ptype == 'part' and ptitle.startswith('VI.'):
                folder = REFERENCE_FOLDER_MAP.get(ctitle)
                if folder:
                    path_map[f"reference/{folder}/index.md"] = cxml_id
                    continue

            path_map[f"{pslug}/{cslug}/index.md"] = cxml_id

    # Find all stub index.md files
    stubs = []
    for root_dir, dirs, files in os.walk(DOCS):
        if "index.md" not in files:
            continue
        idx = os.path.join(root_dir, "index.md")
        if is_stub(idx):
            rel = os.path.relpath(idx, DOCS)
            stubs.append(rel)

    print(f"Found {len(stubs)} stub index files")
    filled = 0
    skipped = 0

    # Preface index.md is intentionally a stub (children are separate pages)
    stubs = [s for s in stubs if s != "preface/index.md"]

    for rel_path in sorted(stubs):
        xml_id = path_map.get(rel_path)
        if not xml_id:
            print(f"  SKIP (no xml_id): {rel_path}")
            skipped += 1
            continue

        elem = find_by_id(xml_root, xml_id)
        if elem is None:
            print(f"  SKIP (elem not found, id={xml_id}): {rel_path}")
            skipped += 1
            continue

        intro_elem = get_intro_xml(elem)
        if intro_elem is None:
            print(f"  SKIP (no intro content, id={xml_id}): {rel_path}")
            skipped += 1
            continue

        md, err = to_markdown(intro_elem)
        if err or not md:
            print(f"  SKIP (pandoc error, id={xml_id}): {err}")
            skipped += 1
            continue

        md = clean_markdown(md)
        if not md:
            print(f"  SKIP (empty after clean, id={xml_id}): {rel_path}")
            skipped += 1
            continue

        abs_path = os.path.join(DOCS, rel_path)
        print(f"  FILL ({xml_id}): {rel_path} [{len(md)} chars]")

        if not DRY_RUN:
            append_content(abs_path, md)
        filled += 1

    print(f"\nFilled: {filled}  Skipped: {skipped}")
    if DRY_RUN:
        print("Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
