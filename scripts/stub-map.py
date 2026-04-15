#!/usr/bin/env python3
"""
stub-map.py — List all stub index pages (no body content) with their subsection counts.

A stub is an index.md with only frontmatter and no body text.
Output is a markdown table sorted by path.

Usage:
    python3 stub-map.py
    python3 stub-map.py > stubs.md
"""

import os, re

DOCS = "/home/rkumar/braised-projects/postgres-braised-docs/docs"


def is_stub(path):
    with open(path) as f:
        content = f.read()
    parts = content.split('---', 2)
    if len(parts) < 3:
        return True
    return parts[2].strip() == ''


def get_title(path):
    with open(path) as f:
        content = f.read()
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    return m.group(1) if m else os.path.basename(os.path.dirname(path))


def count_children(dirpath):
    """Count direct child sections (subdirs with index.md) and leaf .md files."""
    sections = 0
    leaves   = 0
    for name in os.listdir(dirpath):
        if name == 'index.md':
            continue
        child = os.path.join(dirpath, name)
        if os.path.isdir(child) and os.path.exists(os.path.join(child, 'index.md')):
            sections += 1
        elif name.endswith('.md'):
            leaves += 1
    return sections, leaves


def main():
    rows = []

    for root, dirs, files in os.walk(DOCS):
        if 'index.md' not in files:
            continue
        idx = os.path.join(root, 'index.md')
        if not is_stub(idx):
            continue
        rel      = os.path.relpath(root, DOCS)
        title    = get_title(idx)
        sects, leaves = count_children(root)
        total    = sects + leaves
        rows.append((rel, title, sects, leaves, total))

    rows.sort(key=lambda r: r[0])

    print(f"# Stub Pages ({len(rows)} total)\n")
    print(f"| Path | Title | Sub-sections | Leaf pages | Total children |")
    print(f"|------|-------|:---:|:---:|:---:|")
    for rel, title, sects, leaves, total in rows:
        print(f"| `{rel}/` | {title} | {sects} | {leaves} | {total} |")

    print(f"\n{len(rows)} stub pages.")


if __name__ == "__main__":
    main()
