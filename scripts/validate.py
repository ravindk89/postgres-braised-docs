#!/usr/bin/env python3
"""
validate.py — random sample validation of converted markdown against source.

For each sampled page:
  - Frontmatter: title and id present and correct
  - Content: not a stub (has actual prose)
  - Headings: match expected sections from JSON tree
  - No known artifacts: empty headings, loose indexterm words, raw XML tags
  - Cross-check: fetch the live HTML page and compare section titles

Usage:
    python3 validate.py [--pct 20] [--seed 42] [--no-fetch]
"""

import json
import os
import random
import re
import sys
import time
import urllib.request
from pathlib import Path

PCT      = 20
SEED     = 42
OUT_DIR  = "./docs"
TREE     = "./pg-docs-tree.json"
BASE_URL = "https://www.postgresql.org/docs/current/"
DELAY    = 0.3

# ── Slug (must match convert-pg-docs.py) ─────────────────────────────────────

def slug(title):
    title = re.sub(r'^[IVXivx]+\.\s*', '', title)
    title = re.sub(r'^\d+[\d.]*\.\s*', '', title)
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

REFERENCE_FOLDER_MAP = {
    "I. SQL Commands":                     "sql-commands",
    "II. PostgreSQL Client Applications":  "client-apps",
    "III. PostgreSQL Server Applications": "server-apps",
}

# ── Collect all expected content pages from tree ─────────────────────────────

def collect_pages(tree):
    """Return list of {path, title, doc_id, url, type, expected_sections}."""
    pages = []

    for part in tree:
        pslug = slug(part["title"])
        kids  = part.get("children", [])

        is_ref = any(c["title"] in REFERENCE_FOLDER_MAP for c in kids)

        if is_ref:
            for ref in kids:
                folder = REFERENCE_FOLDER_MAP.get(ref["title"], slug(ref["title"]))
                for cmd in ref.get("children", []):
                    cslug  = slug(cmd["title"])
                    raw    = cmd["url"].split("/")[-1].replace(".html", "")
                    doc_id = raw.split("#")[-1].lower() if "#" in raw else raw
                    pages.append({
                        "path":     f"{pslug}/{folder}/{cslug}.md",
                        "title":    cmd["title"],
                        "doc_id":   doc_id,
                        "url":      cmd["url"],
                        "type":     "reference",
                        "expected_sections": [c["title"] for c in cmd.get("children", [])],
                    })
            continue

        for chapter in kids:
            cslug    = slug(chapter["title"])
            sections = chapter.get("children", [])

            if not sections:
                raw    = chapter["url"].split("/")[-1].replace(".html", "")
                doc_id = raw.split("#")[-1].lower() if "#" in raw else raw
                pages.append({
                    "path":     f"{pslug}/{cslug}.md",
                    "title":    chapter["title"],
                    "doc_id":   doc_id,
                    "url":      chapter["url"],
                    "type":     chapter["type"],
                    "expected_sections": [],
                })
                continue

            for sect in sections:
                sslug  = slug(sect["title"])
                raw    = sect["url"].split("/")[-1].replace(".html", "")
                doc_id = raw.split("#")[-1].lower() if "#" in raw else raw
                pages.append({
                    "path":     f"{pslug}/{cslug}/{sslug}.md",
                    "title":    sect["title"],
                    "doc_id":   doc_id,
                    "url":      sect["url"],
                    "type":     "sect1",
                    "expected_sections": [c["title"] for c in sect.get("children", [])],
                })

    return pages


# ── Per-page checks ───────────────────────────────────────────────────────────

ARTIFACTS = [
    (r'^\s*\d+\s*$',            "bare number (manpage section noise)"),
    (r'<[a-z]+[^>]*>',          "raw XML/HTML tag"),
    (r'^#+\s*$',                "empty heading"),
    (r'\bSQL - Language\b',     "refmeta noise"),
]

def check_file(page):
    path = Path(OUT_DIR) / page["path"]
    issues = []

    if not path.exists():
        return ["FILE MISSING"]

    text = path.read_text()
    lines = text.splitlines()

    # Frontmatter checks
    if f'title: "{page["title"]}"' not in text:
        issues.append(f'title mismatch (expected "{page["title"]}")')
    if f'id: {page["doc_id"]}' not in text:
        issues.append(f'id missing/wrong (expected {page["doc_id"]})')

    # Stub check — real content should have >5 non-frontmatter lines
    body_lines = [l for l in lines if l.strip() and not l.startswith('---')]
    if len(body_lines) < 5:
        issues.append("looks like a stub (too short)")

    # Artifact checks
    for line in lines:
        for pattern, label in ARTIFACTS:
            if re.search(pattern, line):
                issues.append(f"artifact: {label} → {line.strip()[:60]!r}")
                break  # one artifact per line is enough

    # Heading check against expected subsections
    if page["expected_sections"]:
        headings = [re.sub(r'^#+\s*', '', l).strip()
                    for l in lines if re.match(r'^#+\s+', l)]
        for sec in page["expected_sections"]:
            bare = sec.split('.')[-1].strip()
            if not any(bare.lower() in h.lower() for h in headings):
                issues.append(f"missing expected section: {bare!r}")

    return issues


def fetch_html_headings(url):
    """Return H2 headings from the live PostgreSQL docs page."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "braised-validator/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None, str(e)

    headings = re.findall(r'<h2[^>]*>.*?</h2>', html, re.DOTALL)
    clean = []
    for h in headings:
        text = re.sub(r'<[^>]+>', '', h).strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) < 120:
            clean.append(text)
    return clean, None


def check_against_html(page):
    """Fetch live HTML and compare H2s to markdown headings."""
    url = page["url"]
    if not url.startswith("http"):
        return []

    html_h2s, err = fetch_html_headings(url)
    if err:
        return [f"fetch error: {err}"]

    path = Path(OUT_DIR) / page["path"]
    if not path.exists():
        return []
    md_lines = path.read_text().splitlines()
    md_h2s = [re.sub(r'^##\s*', '', l).strip()
               for l in md_lines if re.match(r'^##\s+', l)]

    issues = []
    for h in (html_h2s or []):
        h_clean = re.sub(r'\s*#\s*$', '', h).strip()
        if h_clean and not any(h_clean.lower() in m.lower() for m in md_h2s):
            issues.append(f"HTML H2 not in markdown: {h_clean!r}")
    return issues


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    no_fetch = "--no-fetch" in sys.argv
    pct  = PCT
    seed = SEED
    for i, a in enumerate(sys.argv[1:]):
        if a == "--pct":  pct  = int(sys.argv[i+2])
        if a == "--seed": seed = int(sys.argv[i+2])

    with open(TREE) as f:
        data = json.load(f)

    all_pages = collect_pages(data["tree"])
    random.seed(seed)
    sample = random.sample(all_pages, max(1, len(all_pages) * pct // 100))

    # Stratify the report
    by_type = {}
    for p in sample:
        by_type.setdefault(p["type"], []).append(p)

    print(f"Validating {len(sample)}/{len(all_pages)} pages ({pct}%) — seed {seed}\n")

    total_issues = 0
    results = []

    for i, page in enumerate(sample):
        issues = check_file(page)

        if not no_fetch:
            time.sleep(DELAY)
            issues += check_against_html(page)

        status = "PASS" if not issues else "FAIL"
        results.append((status, page, issues))
        total_issues += len(issues)

        symbol = "." if status == "PASS" else "F"
        print(symbol, end="", flush=True)
        if (i + 1) % 60 == 0:
            print(f"  {i+1}/{len(sample)}")

    print(f"\n\n{'─'*70}")
    fails = [(p, iss) for s, p, iss in results if s == "FAIL"]
    passes = sum(1 for s, _, _ in results if s == "PASS")

    if fails:
        print(f"\nFAILURES ({len(fails)}):\n")
        for page, issues in fails:
            print(f"  [{page['type']:12}] {page['path']}")
            for iss in issues:
                print(f"    - {iss}")
        print()

    print(f"Results: {passes} passed, {len(fails)} failed, {total_issues} issues")
    print(f"Types in sample: { {k: len(v) for k, v in by_type.items()} }")


if __name__ == "__main__":
    main()
