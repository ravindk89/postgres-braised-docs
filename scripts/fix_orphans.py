#!/usr/bin/env python3
"""
fix_orphans.py — Restore dropped intro sentences in pandoc-converted markdown
by correlating orphans.tsv entries against the DocBook XML source.

Two patterns handled:
  A (italic-drop): Para opens with prose + italic span; pandoc dropped the
     non-italic prefix, leaving "_term_ rest of sentence" as the orphan.
     Fix: replace the orphan line with the full converted para opening.

  B (code-block continuation): A <para> embeds a <programlisting>; pandoc
     split the para at the code block. The pre-code intro sentence was dropped.
     Orphan is the continuation phrase ("which returns:", "but this will not
     work...", etc.) after the code block.
     Fix: insert the missing intro sentence before the relevant code block.

Usage:
    python3 scripts/fix_orphans.py [--dry-run]
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR     = PROJECT_ROOT / 'docs'
XML_FILE     = PROJECT_ROOT / 'postgres-full.xml'
ORPHANS_FILE = PROJECT_ROOT / 'orphans.tsv'


# ── XML helpers ────────────────────────────────────────────────────────────────

def load_paras(xml_path):
    """
    Scan the XML line-by-line and return list of (line_no, para_body_str).
    <para> does not nest in DocBook, so first </para> closes it.
    """
    paras = []
    buf = []
    start_line = 0
    inside = False

    with open(xml_path) as f:
        for lineno, raw in enumerate(f, 1):
            if not inside:
                if '<para' in raw:
                    inside = True
                    start_line = lineno
                    buf = [raw]
                    # Single-line para?
                    if '</para>' in raw:
                        paras.append((start_line, ''.join(buf)))
                        inside = False
                        buf = []
            else:
                buf.append(raw)
                if '</para>' in raw:
                    paras.append((start_line, ''.join(buf)))
                    inside = False
                    buf = []

    return paras


def para_body(raw_para):
    """Strip the outer <para>...</para> tags, return inner text."""
    m = re.search(r'<para\b[^>]*>(.*)</para>', raw_para, re.DOTALL)
    return m.group(1) if m else raw_para


def strip_tags(text):
    """Remove all XML tags and decode basic entities; normalize whitespace."""
    text = re.sub(r'<indexterm[^>]*>.*?</indexterm>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<footnote[^>]*>.*?</footnote>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = (text
            .replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
            .replace('&mdash;', '—').replace('&ndash;', '–')
            .replace('&nbsp;', ' ').replace('&#8203;', '').replace('&hellip;', '…')
            .replace('&ldquo;', '"').replace('&rdquo;', '"')
            .replace('&lsquo;', "'").replace('&rsquo;', "'"))
    return re.sub(r'\s+', ' ', text).strip()


# Ordered list: more specific patterns first
_INLINE = [
    # bold emphasis first
    (re.compile(r'<emphasis\s+role="bold">(.*?)</emphasis>', re.DOTALL),
     lambda m: f'**{_ws(m.group(1))}**'),
    # italic / term
    (re.compile(r'<(?:firstterm|emphasis)>(.*?)</(?:firstterm|emphasis)>', re.DOTALL),
     lambda m: f'_{_ws(m.group(1))}_'),
    # replaceable / returnvalue
    (re.compile(r'<(?:replaceable|returnvalue)>(.*?)</(?:replaceable|returnvalue)>', re.DOTALL),
     lambda m: f'_{_ws(m.group(1))}_'),
    # monospace family
    (re.compile(
        r'<(?:literal|function|command|structfield|parameter|type|varname|'
        r'option|filename|classname|envar|structname|symbol|refentrytitle|'
        r'methodname|interfacename|constant|property|code)\b[^>]*>'
        r'(.*?)'
        r'</(?:literal|function|command|structfield|parameter|type|varname|'
        r'option|filename|classname|envar|structname|symbol|refentrytitle|'
        r'methodname|interfacename|constant|property|code)>',
        re.DOTALL),
     lambda m: f'`{_ws(m.group(1))}`'),
    # quotes
    (re.compile(r'<quote>(.*?)</quote>', re.DOTALL),
     lambda m: f'"{_ws(m.group(1))}"'),
    # plain-text wrappers
    (re.compile(
        r'<(?:productname|application|acronym|abbrev|trademark|'
        r'package|database|phrase)\b[^>]*>(.*?)'
        r'</(?:productname|application|acronym|abbrev|trademark|'
        r'package|database|phrase)>',
        re.DOTALL),
     lambda m: _ws(m.group(1))),
]

def _ws(s):
    """Normalize internal whitespace of a matched group."""
    return re.sub(r'\s+', ' ', s).strip()

def convert_inline(xml_text):
    """Convert DocBook inline markup to Markdown, strip remaining tags."""
    text = xml_text
    # Strip noise elements
    text = re.sub(r'<indexterm[^>]*>.*?</indexterm>', '', text, flags=re.DOTALL)
    text = re.sub(r'<footnote[^>]*>.*?</footnote>', '', text, flags=re.DOTALL)
    text = re.sub(r'<lineannotation>(.*?)</lineannotation>', r'-- \1', text, flags=re.DOTALL)
    # Apply inline conversions
    for pat, repl in _INLINE:
        text = pat.sub(repl, text)
    # Strip remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    # Entities
    text = (text
            .replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
            .replace('&mdash;', '—').replace('&ndash;', '–')
            .replace('&nbsp;', ' ').replace('&#8203;', '').replace('&hellip;', '…')
            .replace('&ldquo;', '"').replace('&rdquo;', '"')
            .replace('&lsquo;', "'").replace('&rsquo;', "'"))
    return re.sub(r'\s+', ' ', text).strip()


def get_intro_xml(body):
    """Return para body text before the first <programlisting>/<screen>."""
    m = re.search(r'<(?:programlisting|screen)\b', body)
    intro = body[:m.start()] if m else body
    # Strip leading indexterms / whitespace
    intro = re.sub(r'^\s*(?:<indexterm[^>]*>.*?</indexterm>\s*)+', '', intro,
                   flags=re.DOTALL)
    return intro.strip()


def get_first_code_text(body):
    """Return the first LINE of the first <programlisting>/<screen> (for code-block matching).
    Using only the first line avoids false matches on multi-line listings whose
    full normalized text accidentally matches a different code block.
    """
    m = re.search(r'<(?:programlisting|screen)[^>]*>(.*?)</(?:programlisting|screen)>',
                  body, re.DOTALL)
    if not m:
        return None
    content = m.group(1).strip()
    first_line = re.split(r'\n', content)[0].strip()
    return first_line if first_line else content[:60]


# ── Markdown helpers ───────────────────────────────────────────────────────────

def strip_md(text):
    """Strip markdown formatting for plain-text comparison."""
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()


def find_code_line(lines, code_text_norm):
    """
    Find the 0-based line index of a 4-space-indented code block whose first
    non-empty line matches code_text_norm (first 40 chars, normalized).
    """
    key = code_text_norm[:40].lower()
    for i, line in enumerate(lines):
        if line.startswith('    ') or line.startswith('\t'):
            norm = re.sub(r'\s+', ' ', line.strip()).lower()
            if norm.startswith(key[:30]) or key[:30] in norm:
                return i
    return None


def intro_present(lines, before_idx, intro_plain, window=25):
    """True if intro_plain already appears in the markdown just before before_idx."""
    start = max(0, before_idx - window)
    context = ' '.join(l.strip() for l in lines[start:before_idx])
    context_norm = strip_md(context).lower()
    key = intro_plain.lower()[:50]
    return key in context_norm


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    dry_run = '--dry-run' in sys.argv

    # ── Load XML paras ─────────────────────────────────────────────────────────
    print('Loading XML paras…', end=' ', flush=True)
    raw_paras = load_paras(XML_FILE)
    # Pre-compute plain text for each para
    paras = []  # (lineno, body, plain_text)
    for lineno, raw in raw_paras:
        body = para_body(raw)
        plain = strip_tags(body).lower()
        paras.append((lineno, body, plain))
    print(f'{len(paras):,} paras extracted')

    # ── Load orphans ───────────────────────────────────────────────────────────
    orphans = []
    with open(ORPHANS_FILE) as f:
        for raw in f:
            parts = raw.rstrip('\n').split('\t')
            if len(parts) >= 3:
                orphans.append({'file': parts[0], 'line': int(parts[1]), 'text': parts[2]})
    print(f'Orphans: {len(orphans)} across {len({o["file"] for o in orphans})} files\n')

    stats = defaultdict(int)
    by_file = defaultdict(list)
    for o in orphans:
        by_file[o['file']].append(o)

    for rel_path, file_orphans in sorted(by_file.items()):
        md_path = DOCS_DIR / rel_path
        if not md_path.exists():
            stats['missing_file'] += len(file_orphans)
            continue

        with open(md_path) as f:
            lines = f.readlines()

        handled_para_lines = set()  # xml para lineno already processed
        used_insert_points = set()  # 0-based insert positions used this file
        modified = False

        # Process highest line numbers first so insertions don't shift later indices
        for orphan in sorted(file_orphans, key=lambda o: o['line'], reverse=True):
            line_idx = orphan['line'] - 1  # 0-based
            if line_idx >= len(lines):
                stats['stale_lineno'] += 1
                continue

            orphan_plain = strip_md(orphan['text']).lower()

            # Verify the orphan text is actually near the recorded line number.
            # The TSV can be off by a few lines; search ±5 lines and adjust.
            search_key = orphan_plain[:40]
            actual_idx = None
            for delta in range(0, 6):
                for sign in (0, 1, -1):
                    candidate = line_idx + sign * delta
                    if 0 <= candidate < len(lines):
                        if search_key in strip_md(lines[candidate]).lower():
                            actual_idx = candidate
                            break
                if actual_idx is not None:
                    break
            if actual_idx is None:
                stats['text_not_found'] += 1
                continue
            line_idx = actual_idx

            # Short key for initial XML matching (first 55 plain chars)
            key55 = orphan_plain[:55]

            # ── Find matching XML para(s) ──────────────────────────────────────
            hits = [(ln, body, plain)
                    for ln, body, plain in paras
                    if key55 in plain]

            if not hits:
                stats['no_xml_match'] += 1
                continue

            # ── Disambiguate when multiple hits ───────────────────────────────
            if len(hits) > 1:
                # Try secondary key: the code block immediately after the orphan
                # (which would appear in the same XML para)
                next_code = None
                for k in range(line_idx + 1, min(line_idx + 25, len(lines))):
                    l = lines[k]
                    if l.startswith('    ') or l.startswith('\t'):
                        next_code = re.sub(r'\s+', ' ', l.strip()).lower()[:35]
                        break

                if next_code:
                    filtered = [(ln, b, p) for ln, b, p in hits if next_code[:25] in p]
                    if len(filtered) == 1:
                        hits = filtered
                    elif len(filtered) == 0:
                        # Try the code block immediately BEFORE the orphan
                        prev_code = None
                        for k in range(line_idx - 1, max(0, line_idx - 25), -1):
                            l = lines[k]
                            if l.startswith('    ') or l.startswith('\t'):
                                prev_code = re.sub(r'\s+', ' ', l.strip()).lower()[:35]
                                break
                        if prev_code:
                            filtered2 = [(ln, b, p) for ln, b, p in hits
                                         if prev_code[:25] in p]
                            if len(filtered2) == 1:
                                hits = filtered2
                            else:
                                stats['ambiguous'] += 1
                                continue
                        else:
                            stats['ambiguous'] += 1
                            continue
                    else:
                        stats['ambiguous'] += 1
                        continue
                else:
                    stats['ambiguous'] += 1
                    continue

            xml_lineno, body, _ = hits[0]

            if xml_lineno in handled_para_lines:
                stats['already_handled'] += 1
                continue

            # ── Extract intro text ─────────────────────────────────────────────
            intro_xml = get_intro_xml(body)
            if not intro_xml:
                stats['no_intro'] += 1
                continue

            intro_plain = strip_tags(intro_xml)
            if len(intro_plain) < 8:
                stats['trivial_intro'] += 1
                continue

            intro_md = convert_inline(intro_xml)
            if not intro_md:
                stats['empty_intro'] += 1
                continue

            # ── Determine pattern and insertion point ─────────────────────────
            first_code_xml = get_first_code_text(body)

            if first_code_xml:
                # Pattern B: find the code block in the markdown and insert before it
                code_norm = re.sub(r'\s+', ' ', first_code_xml).strip()
                insert_idx = find_code_line(lines, code_norm)

                if insert_idx is None:
                    # Fall back: closest code block before the orphan
                    for k in range(line_idx - 1, max(0, line_idx - 40), -1):
                        if lines[k].startswith('    ') or lines[k].startswith('\t'):
                            insert_idx = k
                            break

                if insert_idx is None or insert_idx > line_idx:
                    # Code block is after the orphan — something unexpected; skip
                    stats['bad_insert_point'] += 1
                    continue

                # Guard: don't insert twice at the same position in this file
                if insert_idx in used_insert_points:
                    stats['already_handled'] += 1
                    continue

                # Check if intro is already present before that code block
                if intro_present(lines, insert_idx, intro_plain):
                    stats['already_present'] += 1
                    handled_para_lines.add(xml_lineno)
                    used_insert_points.add(insert_idx)
                    continue

                # Check if the intro IS the same as or ends with the orphan text
                # (would mean we'd be inserting the orphan text before itself)
                intro_norm_lower = intro_plain.lower()
                if orphan_plain[:50] in intro_norm_lower and \
                        intro_norm_lower.endswith(orphan_plain[:50]):
                    stats['intro_is_orphan'] += 1
                    continue

                if dry_run:
                    print(f'  INSERT {rel_path}:{insert_idx + 1}')
                    print(f'    +++ {intro_md[:90]}')
                    used_insert_points.add(insert_idx)
                else:
                    # Insert: ensure blank line before, intro text, blank line after
                    block = []
                    if insert_idx > 0 and lines[insert_idx - 1].strip():
                        block.append('\n')
                    block.append(intro_md + '\n')
                    if not lines[insert_idx].strip() == '':
                        block.append('\n')
                    for k, ins in enumerate(block):
                        lines.insert(insert_idx + k, ins)
                    modified = True
                    stats['inserted'] += 1
                    used_insert_points.add(insert_idx)

            else:
                # Pattern A: no code block in para — the orphan line IS the broken
                # first sentence. Replace it with the full intro.
                orphan_norm = orphan_plain
                intro_norm  = intro_plain.lower()

                # Only replace if the intro contains material that's not in the orphan
                # (i.e., there's a real prefix that was dropped)
                if intro_norm[:20] in orphan_norm[:30]:
                    # Intro starts with what the orphan has — nothing was dropped
                    stats['nothing_dropped'] += 1
                    handled_para_lines.add(xml_lineno)
                    continue

                # Verify the orphan is a SUFFIX of the intro (the dropped part was
                # the opening; what remains = the orphan). If the orphan text appears
                # in the middle of the intro rather than at the end, it's a different
                # para entirely (e.g. a <refpurpose> matched against a description para).
                orphan_start25 = orphan_norm[:25]
                intro_tail = intro_norm.rstrip('.').rstrip()[-max(40, len(orphan_norm)):]
                if orphan_start25 not in intro_tail:
                    stats['pattern_a_mismatch'] += 1
                    continue

                if dry_run:
                    print(f'  REPLACE {rel_path}:{orphan["line"]}')
                    print(f'    --- {lines[line_idx].rstrip()[:80]}')
                    print(f'    +++ {intro_md[:90]}')
                else:
                    lines[line_idx] = intro_md + '\n'
                    modified = True
                    stats['replaced'] += 1

            handled_para_lines.add(xml_lineno)

        if modified and not dry_run:
            with open(md_path, 'w') as f:
                f.writelines(lines)
            n_fixed = stats['inserted'] + stats['replaced']  # rough count
            print(f'  wrote {rel_path}')

    print()
    print('── Results ──────────────────────────────────────')
    total = sum(stats.values())
    for k in ['inserted', 'replaced', 'already_present', 'already_handled',
              'ambiguous', 'no_xml_match', 'text_not_found', 'stale_lineno',
              'missing_file', 'no_intro', 'trivial_intro', 'bad_insert_point',
              'nothing_dropped', 'intro_is_orphan', 'empty_intro',
              'pattern_a_mismatch']:
        if stats[k]:
            print(f'  {k:25s} {stats[k]:4d}')
    print(f'  {"total accounted":25s} {total:4d}')


if __name__ == '__main__':
    main()
