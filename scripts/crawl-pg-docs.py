#!/usr/bin/env python3
"""
crawl-pg-docs.py — crawl PostgreSQL docs structure and output a JSON tree.

Usage:
    python3 crawl-pg-docs.py              # full crawl (chapters + reference)
    python3 crawl-pg-docs.py --shallow    # top-level only (no chapter crawl)

Output: pg-docs-tree.json in the same directory.
"""

import json
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from urllib.error import URLError
from html.parser import HTMLParser

BASE = "https://www.postgresql.org/docs/current/"
OUTPUT = "pg-docs-tree.json"
DELAY = 0.5  # seconds between requests

# Node types in the PostgreSQL DocBook HTML output.
KNOWN_TYPES = {"preface", "part", "chapter", "sect1", "sect2",
               "reference", "appendix", "bibliography", "index"}


# ── HTTP ──────────────────────────────────────────────────────────────────────

def fetch(url):
    req = Request(url, headers={"User-Agent": "braised-docs-crawler/1.0"})
    try:
        with urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except URLError as e:
        print(f"  WARN: could not fetch {url}: {e}", file=sys.stderr)
        return ""


# ── TOC parser ────────────────────────────────────────────────────────────────

class TocParser(HTMLParser):
    """Parse a <div class="toc"> from a PostgreSQL docs page into a node list."""

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.in_toc = False
        self.toc_div_depth = 0
        self.result = []
        self.stack = []          # stack of lists; each list = children at that dl depth
        self.last_completed = None  # last dt item completed at current level
        self.current = None      # item being built
        self.in_link = False     # inside <a> inside current dt

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # Enter the TOC div.
        if tag == "div" and "toc" in attrs.get("class", "").split():
            if not self.in_toc:
                self.in_toc = True
                self.toc_div_depth = 1
                self.stack = [self.result]
                return

        if not self.in_toc:
            return

        if tag == "div":
            self.toc_div_depth += 1
        elif tag == "dl":
            # Nested <dl> belongs to the last completed item's children.
            if self.last_completed is not None:
                self.stack.append(self.last_completed["children"])
                self.last_completed = None
        elif tag == "dt":
            self.current = {"type": "unknown", "title": "", "url": "", "children": []}
        elif tag == "span" and self.current and not self.in_link:
            cls = attrs.get("class", "")
            if cls in KNOWN_TYPES:
                self.current["type"] = cls
        elif tag == "a" and self.current:
            href = attrs.get("href", "")
            if href and not href.startswith("#"):
                self.current["url"] = urljoin(self.base_url, href)
            self.in_link = True

    def handle_endtag(self, tag):
        if not self.in_toc:
            return

        if tag == "div":
            self.toc_div_depth -= 1
            if self.toc_div_depth == 0:
                self.in_toc = False
        elif tag == "dl":
            if len(self.stack) > 1:
                self.stack.pop()
        elif tag == "dt":
            if self.current and self.current["url"]:
                self.current["title"] = " ".join(self.current["title"].split())
                self.stack[-1].append(self.current)
                self.last_completed = self.current
            self.current = None
            self.in_link = False
        elif tag == "a":
            self.in_link = False

    def handle_data(self, data):
        if self.current and self.in_link:
            self.current["title"] += data


def parse_toc(html, base_url):
    p = TocParser(base_url)
    p.feed(html)
    return p.result


# ── Crawl ─────────────────────────────────────────────────────────────────────

def crawl_children(item):
    """Fetch item's page and populate item["children"] with its TOC sections."""
    url = item["url"]
    print(f"  fetching {url}", file=sys.stderr)
    time.sleep(DELAY)
    html = fetch(url)
    if not html:
        return
    children = parse_toc(html, url)
    if children:
        item["children"] = children


def crawl(shallow=False):
    print(f"fetching index: {BASE}", file=sys.stderr)
    html = fetch(BASE)
    tree = parse_toc(html, BASE)

    if shallow:
        return tree

    # Second pass: fetch each chapter/reference page for its sections.
    for node in tree:
        for child in node.get("children", []):
            ctype = child.get("type", "")
            if ctype in ("chapter", "reference", "appendix", "preface", "sect1"):
                if not child["children"]:  # only fetch if not already populated
                    crawl_children(child)

    return tree


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    shallow = "--shallow" in sys.argv

    print("crawling PostgreSQL docs...", file=sys.stderr)
    tree = crawl(shallow=shallow)

    output = {
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "source": BASE,
        "shallow": shallow,
        "tree": tree,
    }

    with open(OUTPUT, "w") as f:
        json.dump(output, f, indent=2)

    total = sum(len(n.get("children", [])) for n in tree)
    print(f"done. {len(tree)} top-level nodes, {total} children. written to {OUTPUT}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
