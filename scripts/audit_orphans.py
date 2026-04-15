#!/usr/bin/env python3
"""
audit_orphans.py — Classify every orphan in orphans.tsv and produce a
human-readable markdown report at orphan-audit.md.

Categories per orphan:
  FIXED        — intro sentence is now present in the file (script applied it)
  WOULD_FIX    — script would still insert/replace (was skipped on original run)
  FALSE_POS    — refpurpose / synopsis / other non-para element
  NO_XML_MATCH — first 55 chars not found anywhere in the XML
  AMBIGUOUS    — multiple XML para hits, couldn't disambiguate
  ALREADY      — duplicate insert point in same file
  OTHER        — any other skip reason

Usage:
    python3 scripts/audit_orphans.py
    # writes orphan-audit.md
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR     = PROJECT_ROOT / 'docs'
XML_FILE     = PROJECT_ROOT / 'postgres-full.xml'
ORPHANS_FILE = PROJECT_ROOT / 'orphans.tsv'
OUT_FILE     = PROJECT_ROOT / 'orphan-audit.md'

# ── reuse helpers from fix_orphans.py ─────────────────────────────────────────

def load_paras(xml_path):
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
    m = re.search(r'<para\b[^>]*>(.*)</para>', raw_para, re.DOTALL)
    return m.group(1) if m else raw_para

def strip_tags(text):
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

_INLINE = [
    (re.compile(r'<emphasis\s+role="bold">(.*?)</emphasis>', re.DOTALL),
     lambda m: f'**{_ws(m.group(1))}**'),
    (re.compile(r'<(?:firstterm|emphasis)>(.*?)</(?:firstterm|emphasis)>', re.DOTALL),
     lambda m: f'_{_ws(m.group(1))}_'),
    (re.compile(r'<(?:replaceable|returnvalue)>(.*?)</(?:replaceable|returnvalue)>', re.DOTALL),
     lambda m: f'_{_ws(m.group(1))}_'),
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
    (re.compile(r'<quote>(.*?)</quote>', re.DOTALL),
     lambda m: f'"{_ws(m.group(1))}"'),
    (re.compile(
        r'<(?:productname|application|acronym|abbrev|trademark|'
        r'package|database|phrase)\b[^>]*>(.*?)'
        r'</(?:productname|application|acronym|abbrev|trademark|'
        r'package|database|phrase)>',
        re.DOTALL),
     lambda m: _ws(m.group(1))),
]

def _ws(s):
    return re.sub(r'\s+', ' ', s).strip()

def convert_inline(xml_text):
    text = xml_text
    text = re.sub(r'<indexterm[^>]*>.*?</indexterm>', '', text, flags=re.DOTALL)
    text = re.sub(r'<footnote[^>]*>.*?</footnote>', '', text, flags=re.DOTALL)
    text = re.sub(r'<lineannotation>(.*?)</lineannotation>', r'-- \1', text, flags=re.DOTALL)
    for pat, repl in _INLINE:
        text = pat.sub(repl, text)
    text = re.sub(r'<[^>]+>', '', text)
    text = (text
            .replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
            .replace('&mdash;', '—').replace('&ndash;', '–')
            .replace('&nbsp;', ' ').replace('&#8203;', '').replace('&hellip;', '…')
            .replace('&ldquo;', '"').replace('&rdquo;', '"')
            .replace('&lsquo;', "'").replace('&rsquo;', "'"))
    return re.sub(r'\s+', ' ', text).strip()

def get_intro_xml(body):
    m = re.search(r'<(?:programlisting|screen)\b', body)
    intro = body[:m.start()] if m else body
    intro = re.sub(r'^\s*(?:<indexterm[^>]*>.*?</indexterm>\s*)+', '', intro, flags=re.DOTALL)
    return intro.strip()

def get_first_code_text(body):
    m = re.search(r'<(?:programlisting|screen)[^>]*>(.*?)</(?:programlisting|screen)>',
                  body, re.DOTALL)
    if not m:
        return None
    content = m.group(1).strip()
    first_line = re.split(r'\n', content)[0].strip()
    return first_line if first_line else content[:60]

def strip_md(text):
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()

def find_code_line(lines, code_text_norm):
    key = code_text_norm[:40].lower()
    for i, line in enumerate(lines):
        if line.startswith('    ') or line.startswith('\t'):
            norm = re.sub(r'\s+', ' ', line.strip()).lower()
            if norm.startswith(key[:30]) or key[:30] in norm:
                return i
    return None

def intro_present(lines, before_idx, intro_plain, window=25):
    start = max(0, before_idx - window)
    context = ' '.join(l.strip() for l in lines[start:before_idx])
    context_norm = strip_md(context).lower()
    key = intro_plain.lower()[:50]
    return key in context_norm


# ── XML element classifier (for false-positive detection) ─────────────────────

def classify_xml_element(raw_xml, pos):
    """
    Return the innermost enclosing element name at pos in raw_xml.
    Looks at the 500 chars before pos for an open tag.
    """
    chunk = raw_xml[max(0, pos - 500):pos]
    tags = re.findall(
        r'<(para|refpurpose|synopsis|term|entry|listitem|title|refname|'
        r'note|programlisting|screen|funcsynopsisinfo)\b',
        chunk)
    return tags[-1] if tags else 'other'


# ── Main ───────────────────────────────────────────────────────────────────────

CATEGORY_ORDER = ['FIXED', 'WOULD_FIX', 'FALSE_POS', 'NO_XML_MATCH', 'AMBIGUOUS', 'ALREADY', 'OTHER']

def main():
    print('Loading XML…', end=' ', flush=True)
    raw_xml_text = XML_FILE.read_text()
    raw_paras = load_paras(XML_FILE)
    paras = []
    for lineno, raw in raw_paras:
        body = para_body(raw)
        plain = strip_tags(body).lower()
        paras.append((lineno, body, plain))
    print(f'{len(paras):,} paras')

    orphans = []
    with open(ORPHANS_FILE) as f:
        for raw in f:
            parts = raw.rstrip('\n').split('\t')
            if len(parts) >= 3:
                orphans.append({'file': parts[0], 'line': int(parts[1]), 'text': parts[2]})
    print(f'{len(orphans)} orphans across {len({o["file"] for o in orphans})} files\n')

    # results[file] = list of (line, orphan_text, category, detail)
    results = defaultdict(list)

    by_file = defaultdict(list)
    for o in orphans:
        by_file[o['file']].append(o)

    counts = defaultdict(int)

    for rel_path, file_orphans in sorted(by_file.items()):
        md_path = DOCS_DIR / rel_path
        if not md_path.exists():
            for o in file_orphans:
                results[rel_path].append((o['line'], o['text'], 'OTHER', 'file missing'))
                counts['OTHER'] += 1
            continue

        lines = md_path.read_text().splitlines(keepends=True)
        handled_para_lines = set()
        used_insert_points = set()

        for orphan in sorted(file_orphans, key=lambda o: o['line'], reverse=True):
            line_idx = orphan['line'] - 1
            if line_idx >= len(lines):
                results[rel_path].append((orphan['line'], orphan['text'], 'OTHER', 'stale lineno'))
                counts['OTHER'] += 1
                continue

            orphan_plain = strip_md(orphan['text']).lower()
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
                results[rel_path].append((orphan['line'], orphan['text'], 'OTHER', 'text not in file'))
                counts['OTHER'] += 1
                continue
            line_idx = actual_idx

            key55 = orphan_plain[:55]
            hits = [(ln, body, plain) for ln, body, plain in paras if key55 in plain]

            if not hits:
                # Check raw XML for element type
                raw_hits = [m.start() for m in re.finditer(re.escape(key55[:20]), raw_xml_text, re.IGNORECASE)]
                if raw_hits:
                    elem = classify_xml_element(raw_xml_text, raw_hits[0])
                    if elem in ('refpurpose', 'synopsis', 'screen', 'programlisting'):
                        results[rel_path].append((orphan['line'], orphan['text'], 'FALSE_POS', elem))
                        counts['FALSE_POS'] += 1
                        continue
                results[rel_path].append((orphan['line'], orphan['text'], 'NO_XML_MATCH', ''))
                counts['NO_XML_MATCH'] += 1
                continue

            # Disambiguate
            if len(hits) > 1:
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
                        prev_code = None
                        for k in range(line_idx - 1, max(0, line_idx - 25), -1):
                            l = lines[k]
                            if l.startswith('    ') or l.startswith('\t'):
                                prev_code = re.sub(r'\s+', ' ', l.strip()).lower()[:35]
                                break
                        if prev_code:
                            filtered2 = [(ln, b, p) for ln, b, p in hits if prev_code[:25] in p]
                            if len(filtered2) == 1:
                                hits = filtered2
                            else:
                                results[rel_path].append((orphan['line'], orphan['text'], 'AMBIGUOUS', f'{len(hits)} hits'))
                                counts['AMBIGUOUS'] += 1
                                continue
                        else:
                            results[rel_path].append((orphan['line'], orphan['text'], 'AMBIGUOUS', f'{len(hits)} hits'))
                            counts['AMBIGUOUS'] += 1
                            continue
                    else:
                        results[rel_path].append((orphan['line'], orphan['text'], 'AMBIGUOUS', f'{len(filtered)} filtered hits'))
                        counts['AMBIGUOUS'] += 1
                        continue
                else:
                    results[rel_path].append((orphan['line'], orphan['text'], 'AMBIGUOUS', f'{len(hits)} hits, no code ctx'))
                    counts['AMBIGUOUS'] += 1
                    continue

            xml_lineno, body, _ = hits[0]

            if xml_lineno in handled_para_lines:
                results[rel_path].append((orphan['line'], orphan['text'], 'ALREADY', 'para already handled'))
                counts['ALREADY'] += 1
                continue

            intro_xml = get_intro_xml(body)
            if not intro_xml:
                results[rel_path].append((orphan['line'], orphan['text'], 'OTHER', 'no intro in para'))
                counts['OTHER'] += 1
                continue

            intro_plain = strip_tags(intro_xml)
            if len(intro_plain) < 8:
                results[rel_path].append((orphan['line'], orphan['text'], 'OTHER', 'trivial intro'))
                counts['OTHER'] += 1
                continue

            intro_md = convert_inline(intro_xml)
            first_code_xml = get_first_code_text(body)

            if first_code_xml:
                code_norm = re.sub(r'\s+', ' ', first_code_xml).strip()
                insert_idx = find_code_line(lines, code_norm)
                if insert_idx is None:
                    for k in range(line_idx - 1, max(0, line_idx - 40), -1):
                        if lines[k].startswith('    ') or lines[k].startswith('\t'):
                            insert_idx = k
                            break

                if insert_idx is None or insert_idx > line_idx:
                    results[rel_path].append((orphan['line'], orphan['text'], 'OTHER', 'bad insert point'))
                    counts['OTHER'] += 1
                    continue

                if insert_idx in used_insert_points:
                    results[rel_path].append((orphan['line'], orphan['text'], 'ALREADY', f'insert point {insert_idx+1} used'))
                    counts['ALREADY'] += 1
                    handled_para_lines.add(xml_lineno)
                    continue

                if intro_present(lines, insert_idx, intro_plain):
                    results[rel_path].append((orphan['line'], orphan['text'], 'FIXED',
                                              f'intro at line ~{insert_idx+1}: {intro_md[:80]}'))
                    counts['FIXED'] += 1
                    handled_para_lines.add(xml_lineno)
                    used_insert_points.add(insert_idx)
                    continue

                intro_norm_lower = intro_plain.lower()
                if orphan_plain[:50] in intro_norm_lower and intro_norm_lower.endswith(orphan_plain[:50]):
                    results[rel_path].append((orphan['line'], orphan['text'], 'OTHER', 'intro is orphan'))
                    counts['OTHER'] += 1
                    continue

                results[rel_path].append((orphan['line'], orphan['text'], 'WOULD_FIX',
                                          f'INSERT before line {insert_idx+1}: {intro_md[:80]}'))
                counts['WOULD_FIX'] += 1
                used_insert_points.add(insert_idx)

            else:
                orphan_norm = orphan_plain
                intro_norm  = intro_plain.lower()

                if intro_norm[:20] in orphan_norm[:30]:
                    results[rel_path].append((orphan['line'], orphan['text'], 'OTHER', 'nothing dropped'))
                    counts['OTHER'] += 1
                    handled_para_lines.add(xml_lineno)
                    continue

                orphan_start25 = orphan_norm[:25]
                intro_tail = intro_norm.rstrip('.').rstrip()[-max(40, len(orphan_norm)):]
                if orphan_start25 not in intro_tail:
                    # Might still be a false positive — check raw element type
                    raw_hits = [m.start() for m in re.finditer(re.escape(key55[:20]), raw_xml_text, re.IGNORECASE)]
                    if raw_hits:
                        elem = classify_xml_element(raw_xml_text, raw_hits[0])
                        if elem in ('refpurpose', 'synopsis', 'screen', 'programlisting'):
                            results[rel_path].append((orphan['line'], orphan['text'], 'FALSE_POS', elem))
                            counts['FALSE_POS'] += 1
                            handled_para_lines.add(xml_lineno)
                            continue
                    results[rel_path].append((orphan['line'], orphan['text'], 'OTHER', 'pattern_a_mismatch'))
                    counts['OTHER'] += 1
                    continue

                # Check current file — if the intro is already there, it was fixed
                if intro_present(lines, line_idx, intro_plain):
                    results[rel_path].append((orphan['line'], orphan['text'], 'FIXED',
                                              f'replaced: {intro_md[:80]}'))
                    counts['FIXED'] += 1
                else:
                    results[rel_path].append((orphan['line'], orphan['text'], 'WOULD_FIX',
                                              f'REPLACE with: {intro_md[:80]}'))
                    counts['WOULD_FIX'] += 1

            handled_para_lines.add(xml_lineno)

    # ── Write markdown report ─────────────────────────────────────────────────
    total = sum(counts.values())
    lines_out = [
        '# Orphan Audit Report\n\n',
        f'**Total orphans classified:** {total}  \n',
        f'**Generated from:** `orphans.tsv` ({len(orphans)} entries)\n\n',
        '## Summary\n\n',
        '| Category | Count | Description |\n',
        '|---|---|---|\n',
        f'| FIXED | {counts["FIXED"]} | Intro sentence confirmed present in file — script applied correctly |\n',
        f'| WOULD_FIX | {counts["WOULD_FIX"]} | Script logic matches but intro not yet in file — check manually |\n',
        f'| FALSE_POS | {counts["FALSE_POS"]} | refpurpose / synopsis / screen — not a dropped prose sentence |\n',
        f'| NO_XML_MATCH | {counts["NO_XML_MATCH"]} | First 55 chars not found in XML — encoding/inline-tag mismatch |\n',
        f'| AMBIGUOUS | {counts["AMBIGUOUS"]} | Multiple XML para hits, couldn\'t disambiguate |\n',
        f'| ALREADY | {counts["ALREADY"]} | Duplicate insert point — sibling orphan already handled this para |\n',
        f'| OTHER | {counts["OTHER"]} | Trivial intro, bad insert point, or file missing |\n',
        '\n',
    ]

    for category in CATEGORY_ORDER:
        # Collect all entries in this category
        entries = []
        for rel_path, file_results in sorted(results.items()):
            file_entries = [(line, text, detail) for line, text, cat, detail in file_results if cat == category]
            if file_entries:
                entries.append((rel_path, file_entries))

        if not entries:
            continue

        desc = {
            'FIXED':        'Script applied correctly — intro is present in file',
            'WOULD_FIX':    'Still needs fixing — intro absent, but repair is known',
            'FALSE_POS':    'Not a dropped sentence — refpurpose / synopsis / screen element',
            'NO_XML_MATCH': 'No XML para match — needs manual review during content pass',
            'AMBIGUOUS':    'Multiple XML hits — skipped by script, review manually',
            'ALREADY':      'Duplicate insert point within file — covered by sibling orphan',
            'OTHER':        'Miscellaneous skip',
        }[category]

        lines_out.append(f'## {category} ({counts[category]})\n\n')
        lines_out.append(f'_{desc}_\n\n')

        for rel_path, file_entries in entries:
            lines_out.append(f'### `{rel_path}`\n\n')
            for line, text, detail in sorted(file_entries, key=lambda x: x[0]):
                lines_out.append(f'- **line {line}:** `{text[:80]}`\n')
                if detail:
                    lines_out.append(f'  - _{detail}_\n')
            lines_out.append('\n')

    OUT_FILE.write_text(''.join(lines_out))
    print(f'\nWrote {OUT_FILE}')
    print('\nSummary:')
    for cat in CATEGORY_ORDER:
        if counts[cat]:
            print(f'  {cat:15s} {counts[cat]:4d}')
    print(f'  {"total":15s} {total:4d}')


if __name__ == '__main__':
    main()
