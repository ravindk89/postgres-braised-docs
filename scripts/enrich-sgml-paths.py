#!/usr/bin/env python3
"""
enrich-sgml-paths.py — add sgml_file to each node in pg-docs-tree.json.

Reads all SGML files from the postgres repo at a given tag, extracts the
top-level DocBook element id= attribute (which becomes the HTML filename),
and writes the mapping back into pg-docs-tree.json as a new sgml_file field.

Usage:
    python3 enrich-sgml-paths.py [--repo /path/to/postgres] [--tag REL_18_3]
"""

import json
import re
import subprocess
import sys

REPO    = "/home/rkumar/git/postgres"
TAG     = "REL_18_3"
TREE    = "pg-docs-tree.json"
SGML_DIR = "doc/src/sgml"

# DocBook top-level elements that carry the page id.
TOP_ELEMENTS = re.compile(
    r'<(chapter|appendix|sect1|preface|reference|refentry|book|part|index|bibliography)\s[^>]*\bid="([^"]+)"',
    re.IGNORECASE,
)


def git_show(tag, path):
    result = subprocess.run(
        ["git", "show", f"{tag}:{path}"],
        cwd=REPO, capture_output=True, text=True
    )
    return result.stdout if result.returncode == 0 else ""


def build_id_map(tag):
    """Return {html_slug: sgml_relative_path} for all SGML files at tag."""
    ls = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", tag, SGML_DIR],
        cwd=REPO, capture_output=True, text=True
    )
    files = [f for f in ls.stdout.splitlines() if f.endswith(".sgml")
             and "allfiles" not in f and "filelist" not in f]

    id_map = {}
    for path in files:
        # Only read the first 20 lines — the top-level id is always near the top.
        result = subprocess.run(
            ["git", "show", f"{tag}:{path}"],
            cwd=REPO, capture_output=True, text=True
        )
        head = "\n".join(result.stdout.splitlines()[:20])
        m = TOP_ELEMENTS.search(head)
        if m:
            doc_id = m.group(2)
            id_map[doc_id] = path
    return id_map


def enrich(nodes, id_map):
    for node in nodes:
        url = node.get("url", "")
        slug = url.split("/")[-1].replace(".html", "")
        if slug in id_map:
            node["sgml_file"] = id_map[slug]
        enrich(node.get("children", []), id_map)


def main():
    repo = REPO
    tag  = TAG
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--repo": repo = sys.argv[i+2]
        if arg == "--tag":  tag  = sys.argv[i+2]

    print(f"building id→sgml map from {tag}...", file=sys.stderr)
    id_map = build_id_map(tag)
    print(f"  {len(id_map)} SGML ids found", file=sys.stderr)

    with open(TREE) as f:
        data = json.load(f)

    enrich(data["tree"], id_map)
    data["sgml_tag"] = tag
    data["sgml_repo"] = repo

    with open(TREE, "w") as f:
        json.dump(data, f, indent=2)

    # Report coverage
    matched = sum(1 for line in subprocess.run(
        ["grep", "-c", "sgml_file", TREE], capture_output=True, text=True
    ).stdout.splitlines() if line.strip().isdigit() for _ in [None])
    print(f"done. written to {TREE}", file=sys.stderr)


if __name__ == "__main__":
    main()
