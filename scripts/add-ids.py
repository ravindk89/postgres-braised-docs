#!/usr/bin/env python3
"""
add-ids.py — Add 'id:' frontmatter to part/chapter index.md files.

These stubs were written without a DocBook id, so braised:ref/ links to them
fail. This script adds 'id: <xml_id>' to each index.md whose corresponding
DocBook element has a known id.

Usage:
    python3 add-ids.py [--dry-run]
"""

import json, os, re, sys
import yaml

DOCS    = "/home/rkumar/braised-projects/postgres-braised-docs/docs"
DRY_RUN = "--dry-run" in sys.argv


def slug(title):
    t = re.sub(r'^[IVXivx]+\.\s*', '', title)
    t = re.sub(r'^\d+[\d.]*\.\s*', '', t)
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


REFERENCE_FOLDER_MAP = {
    "I. SQL Commands":                     "sql-commands",
    "II. PostgreSQL Client Applications":  "client-apps",
    "III. PostgreSQL Server Applications": "server-apps",
}


def build_path_map():
    with open("/home/rkumar/braised-projects/postgres-braised-docs/pg-docs-tree.json") as f:
        tree_data = json.load(f)

    path_map = {}  # rel_path → xml_id
    for part in tree_data.get('tree', []):
        ptitle  = part.get('title', '')
        purl    = part.get('url', '')
        ptype   = part.get('type', '')
        pslug   = slug(ptitle)
        pxml_id = purl.rstrip('/').split('/')[-1].replace('.html', '').split('#')[0]
        path_map[f"{pslug}/index.md"] = pxml_id

        for ch in part.get('children', []):
            ctitle  = ch.get('title', '')
            curl    = ch.get('url', '')
            cslug   = slug(ctitle)
            cxml_id = curl.rstrip('/').split('/')[-1].replace('.html', '').split('#')[0]

            if ptype == 'part' and ptitle.startswith('VI.'):
                folder = REFERENCE_FOLDER_MAP.get(ctitle)
                if folder:
                    path_map[f"reference/{folder}/index.md"] = cxml_id
                    continue
            path_map[f"{pslug}/{cslug}/index.md"] = cxml_id

    return path_map


def read_frontmatter(path):
    with open(path) as f:
        content = f.read()
    if not content.startswith('---'):
        return None, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content
    fm = yaml.safe_load(parts[1]) or {}
    return fm, content


def set_id_in_frontmatter(path, xml_id):
    with open(path) as f:
        content = f.read()
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    fm = yaml.safe_load(parts[1]) or {}
    if fm.get('id') == xml_id:
        return False  # already set
    if fm.get('id'):
        print(f"  NOTE: {path} already has id={fm['id']!r}, would set to {xml_id!r}")
        return False
    fm['id'] = xml_id
    new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False,
                       sort_keys=False).rstrip()
    new_content = f"---\n{new_fm}\n---{parts[2]}"
    if not DRY_RUN:
        with open(path, 'w') as f:
            f.write(new_content)
    return True


def main():
    path_map = build_path_map()

    updated = 0
    for rel_path, xml_id in sorted(path_map.items()):
        abs_path = os.path.join(DOCS, rel_path)
        if not os.path.exists(abs_path):
            continue
        action = set_id_in_frontmatter(abs_path, xml_id)
        if action:
            print(f"  {'[dry]' if DRY_RUN else 'SET'} id={xml_id}: {rel_path}")
            updated += 1

    print(f"\nUpdated: {updated}")
    if DRY_RUN:
        print("Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
