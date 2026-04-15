#!/usr/bin/env python3
"""
sketch-nav.py — generate a nav.yaml skeleton from pg-docs-tree.json.

Folder/slug rules:
  - part title  → slugified folder name (e.g. "I. Tutorial" → tutorial)
  - chapter     → slugified folder under part (e.g. "4. SQL Syntax" → sql-syntax)
  - sect1       → slugified .md file under chapter
  - reference commands → flat under reference/sql-commands/, reference/client-apps/, reference/server-apps/
  - preface/appendix/bibliography/index → top-level folder
"""

import json, re, sys

def slug(title):
    # Strip leading roman numeral + number prefixes: "I.", "4.", "1.1." etc.
    title = re.sub(r'^[IVXivx]+\.\s*', '', title)
    title = re.sub(r'^\d+[\d.]*\.\s*', '', title)
    # Lowercase, replace non-alphanumeric runs with hyphens
    title = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return title

REFERENCE_FOLDER_MAP = {
    "I. SQL Commands":                    "sql-commands",
    "II. PostgreSQL Client Applications": "client-apps",
    "III. PostgreSQL Server Applications":"server-apps",
}

def nav_entry(indent, label, path=None):
    pad = "  " * indent
    if path:
        return f"{pad}- title: {label}\n{pad}  path: {path}"
    else:
        return f"{pad}- title: {label}"

lines = ["# nav.yaml — PostgreSQL docs structure (generated sketch)", "nav:"]

with open("pg-docs-tree.json") as f:
    data = json.load(f)

for part in data["tree"]:
    ptype = part["type"]
    ptitle = part["title"]
    pslug = slug(ptitle)

    # Top-level group entry
    lines.append(f"")
    lines.append(f"  - title: {ptitle}")

    children = part.get("children", [])

    if ptype in ("bibliography", "index"):
        # Single stub page, no children
        lines.append(f"    path: {pslug}/index.md")
        continue

    lines.append(f"    path: {pslug}/index.md")
    lines.append(f"    children:")

    if ptype == "part" and ptitle.startswith("VI"):
        # Reference — special flat structure per sub-group
        for ref in children:
            folder = REFERENCE_FOLDER_MAP.get(ref["title"], slug(ref["title"]))
            lines.append(f"      - title: {ref['title']}")
            lines.append(f"        path: {pslug}/{folder}/index.md")
            lines.append(f"        children:")
            for cmd in ref.get("children", []):
                cslug = slug(cmd["title"])
                lines.append(f"          - title: {cmd['title']}")
                lines.append(f"            path: {pslug}/{folder}/{cslug}.md")
        continue

    # All other parts: chapters → sections
    for chapter in children:
        cslug = slug(chapter["title"])
        sections = chapter.get("children", [])

        if not sections:
            # Leaf chapter (e.g. preface sections, some appendixes)
            lines.append(f"      - title: {chapter['title']}")
            lines.append(f"        path: {pslug}/{cslug}.md")
            continue

        lines.append(f"      - title: {chapter['title']}")
        lines.append(f"        path: {pslug}/{cslug}/index.md")
        lines.append(f"        children:")
        for sect in sections:
            sslug = slug(sect["title"])
            lines.append(f"          - title: {sect['title']}")
            lines.append(f"            path: {pslug}/{cslug}/{sslug}.md")

print("\n".join(lines))
