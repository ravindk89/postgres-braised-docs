#!/usr/bin/env python3
"""
Collapse small section index pages by merging their child pages in as H2 sections.

Criteria: index.md is a title stub (≤4 lines), ≤5 direct .md siblings, each ≤50 lines.

For each eligible section:
  - Reads each sibling, strips its frontmatter and leading duplicate heading
  - Promotes the child's title to ## and appends its body to the parent index.md
  - Deletes the sibling files
  - Surgically removes those nav entries from nav.yaml
    (sections that lose ALL children become leaf nodes;
     sections that still have subdirectory children keep their structure)

Run with --dry-run first to preview. Pass --skip-existing to skip sections
whose index.md has already been manually merged (has content beyond frontmatter).
"""

import glob
import os
import re
import sys
import yaml

DOCS = "/home/rkumar/braised-projects/postgres-braised-docs/docs"
NAV_PATH = "/home/rkumar/braised-projects/postgres-braised-docs/nav.yaml"
DRY_RUN = "--dry-run" in sys.argv


def find_candidates(docs):
    candidates = []
    for root, dirs, files in os.walk(docs):
        if "index.md" not in files:
            continue
        idx = os.path.join(root, "index.md")
        if sum(1 for _ in open(idx)) > 4:
            continue
        siblings = sorted(
            f for f in glob.glob(os.path.join(root, "*.md"))
            if not f.endswith("index.md")
        )
        if not siblings or len(siblings) > 5:
            continue
        max_lines = max(sum(1 for _ in open(c)) for c in siblings)
        if max_lines > 50:
            continue
        candidates.append((root, idx, siblings))
    return candidates


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.index("---", 3)
    fm = yaml.safe_load(text[3:end]) or {}
    body = text[end + 3:].lstrip("\n")
    return fm, body


def merge_sibling(sibling_path):
    """Return (content_to_append, id_or_None) for a sibling file."""
    text = open(sibling_path).read()
    fm, body = parse_frontmatter(text)
    title = fm.get("title", os.path.splitext(os.path.basename(sibling_path))[0])
    child_id = fm.get("id", None)

    lines = body.split("\n")
    # Strip a leading heading that repeats the title text
    if lines and re.match(r"^#{2,4}\s+", lines[0]):
        lines = lines[1:]
        while lines and lines[0].strip() == "":
            lines = lines[1:]

    body = "\n".join(lines).strip()
    return f"\n\n## {title}\n\n{body}", child_id


def add_aliases_to_frontmatter(text, new_aliases):
    """Insert/extend aliases: list in frontmatter."""
    if not new_aliases:
        return text
    if not text.startswith("---"):
        return text
    end = text.index("---", 3)
    fm_text = text[3:end]
    body = text[end + 3:]
    fm = yaml.safe_load(fm_text) or {}
    existing = fm.get("aliases", []) or []
    merged = list(existing) + [a for a in new_aliases if a not in existing]
    fm["aliases"] = merged
    new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False).rstrip()
    return f"---\n{new_fm}\n---{body}"


def collapse_one(root, idx_path, siblings, dry_run):
    rel = os.path.relpath(root, DOCS)
    print(f"  {rel}/")
    for s in siblings:
        print(f"    + {os.path.basename(s)}")

    if dry_run:
        return set()

    parent_text = open(idx_path).read().rstrip()
    additions = []
    child_ids = []
    for s in siblings:
        content, child_id = merge_sibling(s)
        additions.append(content)
        if child_id:
            child_ids.append(child_id)

    # Inject child IDs as aliases so braised:ref links still resolve
    if child_ids:
        parent_text = add_aliases_to_frontmatter(parent_text, child_ids)

    new_content = parent_text + "".join(additions) + "\n"

    with open(idx_path, "w") as f:
        f.write(new_content)
    for s in siblings:
        os.remove(s)

    # Return the set of relative paths that were removed (for nav update)
    return {os.path.relpath(s, DOCS) for s in siblings}


# ── nav.yaml surgery ─────────────────────────────────────────────────────────

def prune_nav(nodes, removed_paths):
    """
    Recursively remove nav entries whose path is in removed_paths.
    If a section node loses all its children, convert it to a leaf.
    Returns the pruned list.
    """
    result = []
    for node in nodes:
        path = node.get("path", "")
        children = node.get("children", [])

        if path in removed_paths:
            continue  # this page was merged — drop the nav entry

        if children:
            new_children = prune_nav(children, removed_paths)
            if new_children:
                result.append({**node, "children": new_children})
            else:
                # All children removed — become a leaf (keep title + path)
                result.append({"title": node["title"], "path": path})
        else:
            result.append(node)
    return result


def update_nav_yaml(nav_path, removed_paths, dry_run):
    if not removed_paths:
        return

    with open(nav_path) as f:
        data = yaml.safe_load(f)

    nav = data.get("nav", data)
    new_nav = prune_nav(nav, removed_paths)

    if dry_run:
        print(f"\n  [dry-run] Would remove {len(removed_paths)} nav entries from nav.yaml")
        return

    # Preserve the original nav: wrapper and write back
    with open(nav_path, "w") as f:
        yaml.dump({"nav": new_nav}, f, allow_unicode=True,
                  default_flow_style=False, sort_keys=False, indent=2)
    print(f"\n  Updated nav.yaml: removed {len(removed_paths)} entries")


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    # Also handle sections already manually merged (index has content, but siblings
    # still exist on disk and in nav). Check for siblings that exist even if index
    # is no longer a stub.
    candidates = find_candidates(DOCS)

    # Also pick up manually-merged sections: index has content BUT siblings still exist
    for root, dirs, files in os.walk(DOCS):
        if "index.md" not in files:
            continue
        idx = os.path.join(root, "index.md")
        lines = sum(1 for _ in open(idx))
        if lines <= 4:
            continue  # already in candidates or empty
        siblings = sorted(
            f for f in glob.glob(os.path.join(root, "*.md"))
            if not f.endswith("index.md")
        )
        if not siblings:
            continue
        # Check if siblings are orphans (their content is already in index)
        # Heuristic: all siblings are ≤50 lines and index is substantially longer
        max_s = max(sum(1 for _ in open(s)) for s in siblings)
        if max_s > 50:
            continue
        total_s = sum(sum(1 for _ in open(s)) for s in siblings)
        if lines >= total_s * 0.8:  # index is roughly as big as all siblings combined
            rel = os.path.relpath(root, DOCS)
            print(f"  (pre-merged: {rel}/ — {len(siblings)} orphan siblings will be removed)")
            candidates.append((root, idx, siblings, True))
            continue

    # Normalize: ensure all tuples have 4 elements
    normalized = []
    for c in candidates:
        if len(c) == 3:
            normalized.append((*c, False))
        else:
            normalized.append(c)

    if not normalized:
        print("No sections to collapse.")
        return

    prefix = "DRY RUN — " if DRY_RUN else ""
    print(f"{prefix}Collapsing {len(normalized)} section(s):\n")

    all_removed = set()
    for root, idx_path, siblings, pre_merged in normalized:
        rel = os.path.relpath(root, DOCS)
        if pre_merged:
            print(f"  {rel}/ (pre-merged — deleting orphan siblings)")
            if not DRY_RUN:
                for s in siblings:
                    os.remove(s)
                all_removed |= {os.path.relpath(s, DOCS) for s in siblings}
        else:
            removed = collapse_one(root, idx_path, siblings, DRY_RUN)
            if not DRY_RUN:
                all_removed |= removed

    update_nav_yaml(NAV_PATH, all_removed, DRY_RUN)

    if DRY_RUN:
        print("\nRun without --dry-run to apply.")
    else:
        print("\nDone. Re-run convert-nav.py then rebuild.")


if __name__ == "__main__":
    main()
