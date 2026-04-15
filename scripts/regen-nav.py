#!/usr/bin/env python3
"""
regen-nav.py — Regenerate nav-braised.yaml directly from pg-docs-tree.json.

Uses the numbered folder scheme (i-tutorial/01-getting-started/) that
matches the renamed docs/ directory structure. Top-level parts get
collapsed: true. Sections with own pages get kind: section.
"""

import json, os, re, sys, yaml

TREE     = "pg-docs-tree.json"
DOCS     = "docs"
OUT      = "nav-braised.yaml"
DRY_RUN  = "--dry-run" in sys.argv

ROMAN_MAP = {"I":"i","II":"ii","III":"iii","IV":"iv","V":"v",
             "VI":"vi","VII":"vii","VIII":"viii","IX":"ix"}

REFERENCE_FOLDER_MAP = {
    "I. SQL Commands":                     "sql-commands",
    "II. PostgreSQL Client Applications":  "client-apps",
    "III. PostgreSQL Server Applications": "server-apps",
}

def slug(title):
    t = re.sub(r'^[IVXivx]+\.\s*', '', title)
    t = re.sub(r'^\d+[\d.]*\.\s*', '', t)
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

def roman_prefix(title):
    m = re.match(r'^([IVXivx]+)\.', title)
    return ROMAN_MAP.get(m.group(1).upper()) if m else None

def read_nav_collapsed(rel_index_path):
    """Return True if the index.md for this path has nav_collapsed: true."""
    abs_path = os.path.join(DOCS, rel_index_path)
    if not os.path.exists(abs_path):
        return False
    with open(abs_path) as f:
        content = f.read()
    if not content.startswith('---'):
        return False
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    fm = yaml.safe_load(parts[1]) or {}
    return bool(fm.get('nav_collapsed', False))

def num_prefix(title):
    m = re.match(r'^(\d+)\.', title)
    return f"{int(m.group(1)):02d}" if m else None

def quote(s):
    if any(c in s for c in ':{}[]|>&*!,#?@`\'"') or s.startswith(' '):
        return f'"{s.replace(chr(92), chr(92)*2).replace(chr(34), chr(92)+chr(34))}"'
    return s

def emit(nodes, indent=0, top_level=False):
    lines = []
    p = "  " * indent
    for node in nodes:
        title    = node.get("title", "")
        path     = node.get("path", "")        # new numbered path
        children = node.get("children", [])
        q        = quote(title)
        collapsed = node.get("collapsed", False)

        if children:
            if path:
                lines.append(f"{p}- label: {q}")
                if collapsed:
                    lines.append(f"{p}  collapsed: true")
                lines.append(f"{p}  kind: section")
                lines.append(f"{p}  url: {path}")
                lines.append(f"{p}  items:")
                lines.extend(emit(children, indent + 2))
            else:
                lines.append(f"{p}- {q}:")
                lines.extend(emit(children, indent + 1))
        else:
            lines.append(f"{p}- {q}: {path}")
    return lines


def build_tree():
    with open(TREE) as f:
        tree_data = json.load(f)

    top_nodes = []
    for part in tree_data.get("tree", []):
        ptitle = part.get("title", "")
        ptype  = part.get("type", "")
        pslug  = slug(ptitle)
        roman  = roman_prefix(ptitle)
        new_pslug = f"{roman}-{pslug}" if roman else pslug
        has_roman = roman is not None

        ch_nodes = []
        for ch in part.get("children", []):
            ctitle  = ch.get("title", "")
            curl    = ch.get("url", "")
            cslug   = slug(ctitle)
            num     = num_prefix(ctitle)
            cxml_id = curl.rstrip("/").split("/")[-1].replace(".html","").split("#")[0]

            # Reference part — special folder mapping
            if ptype == "part" and ptitle.startswith("VI."):
                folder = REFERENCE_FOLDER_MAP.get(ctitle)
                if folder:
                    ch_path = f"{new_pslug}/{folder}/index.md"
                    sect_nodes = build_sections(ch, f"{new_pslug}/{folder}")
                    ch_nodes.append({"title": ctitle, "path": ch_path, "children": sect_nodes})
                continue

            new_cslug = f"{num}-{cslug}" if num else cslug
            ch_dir    = f"{new_pslug}/{new_cslug}"
            sects     = ch.get("children", [])

            if sects:
                ch_path   = f"{ch_dir}/index.md"
                sect_nodes = build_sections(ch, ch_dir)
                ch_nodes.append({"title": ctitle, "path": ch_path, "children": sect_nodes})
            else:
                # Leaf chapter — single .md file
                ch_path = f"{ch_dir}.md" if not sects else f"{ch_dir}/index.md"
                ch_nodes.append({"title": ctitle, "path": ch_path, "children": []})

        part_path = f"{new_pslug}/index.md"
        top_nodes.append({
            "title":     ptitle,
            "path":      part_path,
            "children":  ch_nodes,
            "collapsed": read_nav_collapsed(part_path),
        })

    return top_nodes


def build_sections(ch_node, ch_dir):
    """Build section nodes under a chapter directory.
    Only includes entries for files that actually exist on disk."""
    nodes = []
    for sect in ch_node.get("children", []):
        stitle = sect.get("title", "")
        sslug  = slug(stitle)
        sect_path = f"{ch_dir}/{sslug}.md"
        abs_path  = os.path.join(DOCS, sect_path)
        if not os.path.exists(abs_path):
            continue  # sect2 sub-sections don't have their own files
        nodes.append({"title": stitle, "path": sect_path, "children": []})
    return nodes


def main():
    tree = build_tree()
    lines = emit(tree)
    output = "\n".join(lines) + "\n"

    if DRY_RUN:
        print(output[:2000])
        print(f"\n({len(lines)} lines total)")
    else:
        with open(OUT, "w") as f:
            f.write(output)
        print(f"Written {len(lines)} lines to {OUT}")


if __name__ == "__main__":
    main()
