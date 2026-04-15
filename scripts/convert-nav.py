#!/usr/bin/env python3
"""
Convert postgres nav.yaml (title/path/children format) to braised nav format.

Sections with their own page (path + children) become kind: section nodes —
clickable header link + expand chevron. Sections without a page become
kind: group (expand-only). Leaves remain compact scalar entries.

Input:
  nav:
    - title: "Section"
      path: section/index.md
      children:
        - title: "Page"
          path: section/page.md

Output:
  # section with own page → rich format
  - label: "Section"
    kind: section
    url: section/index.md
    items:
      - Page: section/page.md

  # section without own page → compact group
  - "Group":
    - Page: section/page.md

  # leaf → compact scalar
  - "Page": section/page.md
"""

import yaml
import sys
import io


def quote_if_needed(s):
    """Quote a string if it contains special YAML characters."""
    needs_quote = any(c in s for c in ':{}[]|>&*!,#?@`\'"')
    needs_quote = needs_quote or s.startswith(' ') or s.endswith(' ')
    if needs_quote:
        escaped = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return s


def emit_nodes(nodes, indent=0):
    """Recursively emit braised nav format lines."""
    lines = []
    prefix = "  " * indent

    for node in nodes:
        title = node.get("title", "")
        path = node.get("path", "")
        children = node.get("children", [])

        quoted_title = quote_if_needed(title)

        if children:
            if path:
                # kind: section — has its own page AND children
                lines.append(f"{prefix}- label: {quoted_title}")
                lines.append(f"{prefix}  kind: section")
                lines.append(f"{prefix}  url: {path}")
                lines.append(f"{prefix}  items:")
                lines.extend(emit_nodes(children, indent + 2))
            else:
                # kind: group — expandable container, no own page
                lines.append(f"{prefix}- {quoted_title}:")
                lines.extend(emit_nodes(children, indent + 1))
        else:
            # Leaf node
            lines.append(f"{prefix}- {quoted_title}: {path}")

    return lines


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "nav.yaml"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "nav-braised.yaml"

    with open(input_path) as f:
        data = yaml.safe_load(f)

    nav = data.get("nav", data)

    lines = emit_nodes(nav)
    output = "\n".join(lines) + "\n"

    if output_path == "-":
        print(output, end="")
    else:
        with open(output_path, "w") as f:
            f.write(output)
        print(f"Written {len(lines)} lines to {output_path}")


if __name__ == "__main__":
    main()
