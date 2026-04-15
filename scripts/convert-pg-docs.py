#!/usr/bin/env python3
"""
convert-pg-docs.py — convert PostgreSQL DocBook to Braised Markdown.

Steps:
  1. Run xmllint --noent to resolve entities → postgres-full.xml (cached)
  2. Parse the XML with ElementTree
  3. Walk pg-docs-tree.json; for each node:
     - container (part/chapter): write stub index.md
     - content (sect1/refentry/appendix): extract XML fragment, strip
       indexterms, convert with pandoc, clean up, write .md
  4. Write nav.yaml alongside the docs

Usage:
    python3 convert-pg-docs.py [--out ./docs] [--force]

    --out   output directory (default: ./docs)
    --force regenerate postgres-full.xml even if cached
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

REPO        = "/home/rkumar/git/postgres"
TAG         = "REL_18_3"
SGML_DIR    = f"{REPO}/doc/src/sgml"
MASTER_SGML = f"{SGML_DIR}/postgres.sgml"
FULL_XML    = "./postgres-full.xml"
TREE_JSON   = "./pg-docs-tree.json"
OUT_DIR     = "./docs"

REFERENCE_FOLDER_MAP = {
    "I. SQL Commands":                     "sql-commands",
    "II. PostgreSQL Client Applications":  "client-apps",
    "III. PostgreSQL Server Applications": "server-apps",
}


# ── Slug ──────────────────────────────────────────────────────────────────────

def slug(title):
    title = re.sub(r'^[IVXivx]+\.\s*', '', title)
    title = re.sub(r'^\d+[\d.]*\.\s*', '', title)
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


# ── XML generation ────────────────────────────────────────────────────────────

def ensure_full_xml(force=False):
    if not force and os.path.exists(FULL_XML):
        print(f"using cached {FULL_XML}", file=sys.stderr)
        return
    print("running xmllint --noent ...", file=sys.stderr)
    result = subprocess.run(
        ["xmllint", "--noent", "--path", SGML_DIR, "--output", FULL_XML, MASTER_SGML],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stderr[:500], file=sys.stderr)
        sys.exit(1)
    print(f"wrote {FULL_XML}", file=sys.stderr)


def load_xml():
    print("parsing XML ...", file=sys.stderr)
    with open(FULL_XML) as f:
        content = f.read()
    # Strip DOCTYPE — ET can't handle it, entities already resolved.
    content = re.sub(r'<!DOCTYPE[^[>]*(?:\[[^\]]*\])?\s*>', '', content, flags=re.DOTALL)
    return ET.fromstring(content)


# ── XML extraction ────────────────────────────────────────────────────────────

def find_by_id(root, doc_id):
    for elem in root.iter():
        if elem.get('id') == doc_id:
            return elem
    return None


def strip_indexterms(elem):
    """Remove all <indexterm> elements in-place."""
    for parent in elem.iter():
        to_remove = [c for c in list(parent) if c.tag == 'indexterm']
        for child in to_remove:
            parent.remove(child)


def to_xml_string(elem):
    return ET.tostring(elem, encoding='unicode')


# ── Pandoc conversion ─────────────────────────────────────────────────────────

# Minimal DocBook wrapper so pandoc recognises the fragment.
# Use <book> directly (no <chapter>) so <sect1> maps to H1, <sect2> to H2, etc.
WRAP = '<book xmlns="http://docbook.org/ns/docbook" version="5.0">{}</book>'
# For <refentry>, wrap in <reference> so pandoc handles it as a reference page.
WRAP_REF = '<book xmlns="http://docbook.org/ns/docbook" version="5.0"><reference>{}</reference></book>'

def to_markdown(elem, is_refentry=False):
    strip_indexterms(elem)
    wrapper = WRAP_REF if is_refentry else WRAP
    xml_str = wrapper.format(to_xml_string(elem))
    result = subprocess.run(
        ["pandoc", "-f", "docbook", "-t", "markdown", "--wrap=none"],
        input=xml_str, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, result.stderr
    return result.stdout, None


# ── Custom refentry converter ─────────────────────────────────────────────────

def iter_text(elem):
    """Concatenate all text content within an element, ignoring tags."""
    return ''.join(elem.itertext())


def convert_synopsis_elem(elem):
    """Render a <synopsis> or <cmdsynopsis> element as plain text for :::synopsis."""
    text = iter_text(elem)
    # Normalise whitespace runs but preserve intentional line breaks.
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text


def refsect_to_markdown(refsect):
    """Convert a single <refsect1> to markdown via pandoc."""
    strip_indexterms(refsect)
    xml_str = WRAP.format(to_xml_string(refsect))
    result = subprocess.run(
        ["pandoc", "-f", "docbook", "-t", "markdown", "--wrap=none"],
        input=xml_str, capture_output=True, text=True
    )
    return result.stdout if result.returncode == 0 else ""


def convert_refentry(elem, title, doc_id):
    """
    Build markdown for a <refentry> element.

    Structure:
      - frontmatter (title, layout, id, description from refpurpose)
      - :::synopsis block from <refsynopsisdiv>
      - H2 sections from each <refsect1>
    """
    # Extract purpose for frontmatter description.
    purpose_elem = elem.find('.//refpurpose')
    purpose = iter_text(purpose_elem).strip() if purpose_elem is not None else ""

    # Build frontmatter.
    fm_lines = ['---', f'title: "{title}"', 'layout: reference', f'id: {doc_id}']
    if purpose:
        fm_lines.append(f'description: "{purpose}"')
    fm_lines.append('---')
    fm = '\n'.join(fm_lines)

    parts = [fm]

    # Synopsis block.
    synopsisdiv = elem.find('refsynopsisdiv')
    if synopsisdiv is not None:
        synopsis_parts = []
        for child in synopsisdiv:
            if child.tag in ('synopsis', 'cmdsynopsis'):
                synopsis_parts.append(convert_synopsis_elem(child))
            elif child.tag == 'refsect2':
                # Named synopsis sub-section (e.g. SELECT's WITH clause)
                sub_title = iter_text(child.find('title')) if child.find('title') is not None else ""
                synopsis_parts.append(f"\n### {sub_title.strip()}")
                for s in child.iter('synopsis'):
                    synopsis_parts.append(convert_synopsis_elem(s))
        if synopsis_parts:
            parts.append('\n:::synopsis\n' + '\n'.join(synopsis_parts).strip() + '\n:::')

    # Refsect1 sections → H2.
    for refsect in elem.findall('refsect1'):
        title_elem = refsect.find('title')
        sect_title = iter_text(title_elem).strip() if title_elem is not None else ""

        md = refsect_to_markdown(refsect)
        md = clean_markdown(md, sect_title)

        if md:
            parts.append(f'## {sect_title}\n\n{md}')

    return '\n\n'.join(parts)


# ── Markdown cleanup ──────────────────────────────────────────────────────────

def clean_markdown(md, title):
    # Fix <replaceable> — pandoc renders as \<text\>, convert to *text* (italic).
    md = re.sub(r'\\<([^>\\]+)\\>', r'*\1*', md)

    lines = md.splitlines()
    out = []
    skip_next_blank = False

    for line in lines:
        # Drop empty headings (e.g. "# " from wrapper with no title).
        if re.match(r'^#+\s*$', line):
            skip_next_blank = True
            continue
        # Remove the auto-generated heading that duplicates the frontmatter title.
        bare = title.split('.')[-1].strip()
        if re.match(r'^#{1,2}\s+' + re.escape(bare) + r'\s*$', line):
            skip_next_blank = True
            continue
        # Drop heading anchor spans {#...} and {.title} suffixes.
        line = re.sub(r'\s*\{[#.][^}]*\}', '', line)
        # Drop empty {#...} id links left by pandoc.
        line = re.sub(r'\[\]\{#[^}]+\}', '', line)
        # Blank line immediately after a removed heading.
        if skip_next_blank and line.strip() == '':
            skip_next_blank = False
            continue
        skip_next_blank = False
        out.append(line)

    return '\n'.join(out).strip()


# ── Frontmatter ───────────────────────────────────────────────────────────────

def frontmatter(title, layout=None, doc_id=None):
    lines = ['---', f'title: "{title}"']
    if layout:
        lines.append(f'layout: {layout}')
    if doc_id:
        lines.append(f'id: {doc_id}')
    lines.append('---')
    return '\n'.join(lines)


def stub(title):
    return frontmatter(title) + '\n'


# ── Nav YAML builder ──────────────────────────────────────────────────────────

nav_lines = ["nav:"]

def nav_entry(indent, title, path=None):
    pad = "  " * indent
    nav_lines.append(f"{pad}- title: \"{title}\"")
    if path:
        nav_lines.append(f"{pad}  path: {path}")


# ── File writing ──────────────────────────────────────────────────────────────

def write_file(path, content):
    p = Path(OUT_DIR) / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content + '\n', encoding='utf-8')


# ── Main walk ─────────────────────────────────────────────────────────────────

def convert_node(xml_root, node, out_path, layout=None):
    """Extract, convert, and write a content node. Returns True on success."""
    raw = node["url"].split("/")[-1].replace(".html", "")
    # Fragment URLs like history.html#HISTORY-BERKELEY → use the fragment id.
    doc_id = raw.split("#")[-1].lower() if "#" in raw else raw
    title  = node["title"]

    elem = find_by_id(xml_root, doc_id)
    if elem is None:
        print(f"  WARN: id '{doc_id}' not found in XML", file=sys.stderr)
        write_file(out_path, stub(title))
        return False

    if elem.tag == 'refentry':
        content = convert_refentry(elem, title, doc_id)
        write_file(out_path, content)
        return True

    md, err = to_markdown(elem)
    if err or not md:
        print(f"  WARN: pandoc error for {doc_id}: {err}", file=sys.stderr)
        write_file(out_path, stub(title))
        return False

    md = clean_markdown(md, title)
    fm = frontmatter(title, layout=layout, doc_id=doc_id)
    write_file(out_path, fm + '\n\n' + md)
    return True


def process_tree(xml_root, tree):
    errors = 0

    for part in tree:
        ptype  = part["type"]
        ptitle = part["title"]
        pslug  = slug(ptitle)
        kids   = part.get("children", [])

        nav_lines.append("")
        nav_entry(1, ptitle, f"{pslug}/index.md")

        # Part-level stub
        write_file(f"{pslug}/index.md", stub(ptitle))

        if ptype in ("bibliography", "index"):
            continue

        if kids:
            nav_lines.append("    children:")

        # ── Reference (Part VI) ────────────────────────────────────────────
        if any(c.get("title") in REFERENCE_FOLDER_MAP for c in kids):
            for ref in kids:
                folder = REFERENCE_FOLDER_MAP.get(ref["title"], slug(ref["title"]))
                ref_path = f"{pslug}/{folder}/index.md"
                write_file(ref_path, stub(ref["title"]))
                nav_entry(2, ref["title"], ref_path)
                cmds = ref.get("children", [])
                if cmds:
                    nav_lines.append("      children:")
                for cmd in cmds:
                    cslug    = slug(cmd["title"])
                    cmd_path = f"{pslug}/{folder}/{cslug}.md"
                    nav_entry(3, cmd["title"], cmd_path)
                    print(f"  ref: {cmd['title']}", file=sys.stderr)
                    if not convert_node(xml_root, cmd, cmd_path, layout="reference"):
                        errors += 1
            continue

        # ── All other parts ────────────────────────────────────────────────
        for chapter in kids:
            cslug    = slug(chapter["title"])
            sections = chapter.get("children", [])

            if not sections:
                # Leaf chapter (some appendixes, preface sections)
                ch_path = f"{pslug}/{cslug}.md"
                nav_entry(2, chapter["title"], ch_path)
                print(f"  chapter-leaf: {chapter['title']}", file=sys.stderr)
                if not convert_node(xml_root, chapter, ch_path):
                    errors += 1
                continue

            ch_path = f"{pslug}/{cslug}/index.md"
            write_file(ch_path, stub(chapter["title"]))
            nav_entry(2, chapter["title"], ch_path)
            nav_lines.append("      children:")

            for sect in sections:
                sslug   = slug(sect["title"])
                s_path  = f"{pslug}/{cslug}/{sslug}.md"
                nav_entry(3, sect["title"], s_path)
                print(f"  sect: {sect['title']}", file=sys.stderr)
                if not convert_node(xml_root, sect, s_path):
                    errors += 1

    return errors


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    force = "--force" in sys.argv
    for i, a in enumerate(sys.argv[1:]):
        if a == "--out":
            global OUT_DIR
            OUT_DIR = sys.argv[i + 2]

    ensure_full_xml(force=force)
    xml_root = load_xml()

    with open(TREE_JSON) as f:
        data = json.load(f)

    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"writing to {OUT_DIR}/", file=sys.stderr)

    errors = process_tree(xml_root, data["tree"])

    nav_path = Path(OUT_DIR).parent / "nav.yaml"
    nav_path.write_text("\n".join(nav_lines) + "\n", encoding="utf-8")
    print(f"wrote {nav_path}", file=sys.stderr)
    print(f"done. {errors} error(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
