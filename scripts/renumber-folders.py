#!/usr/bin/env python3
"""
renumber-folders.py — Add section number prefixes to docs folder names.

Part-level dirs get Roman numeral prefixes:  tutorial → i-tutorial
Chapter-level dirs get zero-padded numbers:  sql-syntax → 04-sql-syntax

Usage:
    python3 renumber-folders.py [--dry-run]

Updates docs/, nav.yaml, and nav-braised.yaml in place.
"""

import json, os, re, sys
import yaml

DOCS        = "/home/rkumar/braised-projects/postgres-braised-docs/docs"
NAV_YAML    = "/home/rkumar/braised-projects/postgres-braised-docs/nav.yaml"
NAV_BRAISED = "/home/rkumar/braised-projects/postgres-braised-docs/nav-braised.yaml"
DRY_RUN     = "--dry-run" in sys.argv

ROMAN = {"I": "i", "II": "ii", "III": "iii", "IV": "iv", "V": "v",
         "VI": "vi", "VII": "vii", "VIII": "viii", "IX": "ix", "X": "x"}


def slug(title):
    t = re.sub(r'^[IVXivx]+\.\s*', '', title)
    t = re.sub(r'^\d+[\d.]*\.\s*', '', t)
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def roman_prefix(title):
    """Extract Roman numeral from 'III. Server Administration' → 'iii'."""
    m = re.match(r'^([IVXivx]+)\.', title)
    if m:
        return ROMAN.get(m.group(1).upper(), m.group(1).lower())
    return None


def chapter_number(title):
    """Extract chapter number from '4. SQL Syntax' → '04'."""
    m = re.match(r'^(\d+)\.', title)
    if m:
        return f"{int(m.group(1)):02d}"
    return None


def letter_prefix(title):
    """Extract appendix letter from 'A. Error Codes' → 'a'."""
    m = re.match(r'^([A-Za-z])\.', title)
    if m:
        return m.group(1).lower()
    return None


def build_rename_map():
    """Returns {old_rel_path: new_rel_path} for all dirs that need renaming."""
    with open("/home/rkumar/braised-projects/postgres-braised-docs/pg-docs-tree.json") as f:
        tree_data = json.load(f)

    REFERENCE_FOLDER_MAP = {
        "I. SQL Commands":                     "sql-commands",
        "II. PostgreSQL Client Applications":  "client-apps",
        "III. PostgreSQL Server Applications": "server-apps",
    }

    renames = {}  # old_rel → new_rel

    parts = tree_data.get('tree', [])
    for part in parts:
        ptitle = part.get('title', '')
        ptype  = part.get('type', '')
        pslug  = slug(ptitle)
        roman  = roman_prefix(ptitle)

        # Compute new part dir name
        if roman:
            new_pslug = f"{roman}-{pslug}"
        else:
            new_pslug = pslug  # Preface, Bibliography, Index stay as-is

        if new_pslug != pslug:
            renames[pslug] = new_pslug

        # Chapter-level renames
        for ch in part.get('children', []):
            ctitle = ch.get('title', '')
            cslug  = slug(ctitle)
            num    = chapter_number(ctitle)
            letter = letter_prefix(ctitle)

            if ptype == 'part' and ptitle.startswith('VI.'):
                # Reference sub-sections: sql-commands, client-apps, server-apps
                folder = REFERENCE_FOLDER_MAP.get(ctitle)
                if folder:
                    old_rel = f"reference/{folder}"
                    new_rel = f"vi-reference/{folder}"
                    renames[old_rel] = new_rel
                continue

            if num:
                new_cslug = f"{num}-{cslug}"
            elif letter:
                # Appendix letters: slug already has letter prefix from original conversion
                # e.g. "b-date-time-support" — keep as is, just under new parent
                new_cslug = cslug  # already lettered
            else:
                new_cslug = cslug

            old_rel = f"{pslug}/{cslug}"
            new_rel = f"{new_pslug}/{new_cslug}"

            if old_rel != new_rel:
                renames[old_rel] = new_rel

    return renames


def apply_renames(renames):
    """Rename directories in docs/. Process deepest paths first."""
    # Sort by depth descending so we don't rename parent before children
    sorted_renames = sorted(renames.items(), key=lambda x: x[0].count('/'), reverse=True)

    for old_rel, new_rel in sorted_renames:
        old_abs = os.path.join(DOCS, old_rel)
        new_abs = os.path.join(DOCS, new_rel)

        if not os.path.exists(old_abs):
            print(f"  SKIP (not found): {old_rel}")
            continue

        if os.path.exists(new_abs):
            print(f"  SKIP (dest exists): {new_rel}")
            continue

        # Ensure parent of new path exists
        new_parent = os.path.dirname(new_abs)
        if not os.path.exists(new_parent):
            if not DRY_RUN:
                os.makedirs(new_parent, exist_ok=True)

        print(f"  MV {old_rel} → {new_rel}")
        if not DRY_RUN:
            os.rename(old_abs, new_abs)


def update_text_paths(text, renames):
    """Replace all old paths with new paths in a text string."""
    # Sort by length descending to replace most specific paths first
    for old, new in sorted(renames.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(old, new)
    return text


def update_nav_file(path, renames):
    with open(path) as f:
        content = f.read()
    new_content = update_text_paths(content, renames)
    if new_content != content:
        print(f"  Updated: {os.path.basename(path)}")
        if not DRY_RUN:
            with open(path, 'w') as f:
                f.write(new_content)
    else:
        print(f"  Unchanged: {os.path.basename(path)}")


def main():
    renames = build_rename_map()

    print(f"{'DRY RUN — ' if DRY_RUN else ''}Renaming {len(renames)} directories:\n")

    # Show what will be renamed
    for old, new in sorted(renames.items()):
        print(f"  {old} → {new}")

    if DRY_RUN:
        print("\nRun without --dry-run to apply.")
        return

    print("\nApplying renames...")
    apply_renames(renames)

    print("\nUpdating nav files...")
    update_nav_file(NAV_YAML, renames)
    update_nav_file(NAV_BRAISED, renames)

    print("\nDone. Rebuild to verify.")


if __name__ == "__main__":
    main()
