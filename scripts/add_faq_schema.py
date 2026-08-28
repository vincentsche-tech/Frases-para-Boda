#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add FAQPage JSON-LD to Frases-para-Boda pages that have a visible FAQ card
but no structured data (same situation as the anniversary site).

Hard rule: the JSON-LD Q/A must match the visible FAQ text VERBATIM, otherwise
Google treats it as spam. So we EXTRACT the existing Q/A from the visible card
(heading is Spanish: "Preguntas Frecuentes") and emit matching JSON-LD. We never
overwrite or regenerate the card itself.

- Idempotent: skips pages that already contain a FAQPage JSON-LD.
- Insertion: JSON-LD before </head>. CSS is already present site-wide, so it is
  only added if `.faq-item{` is somehow missing.
- Spanish text (accents, ¿, ") is preserved with ensure_ascii=False + UTF-8.
"""
import re, os, json, sys, html

ROOT = "."
FAQ_HEADING = "Preguntas Frecuentes"
TARGETS = [
    'index.html',
    'frases-cortas-para-felicitar-bodas.html',
    'frases-graciosas-para-bodas.html',
    'frases-para-aniversario-de-bodas.html',
    'frases-para-bodas-de-oro.html',
    'frases-para-bodas-originales.html',
    'frases-para-invitaciones-de-boda.html',
    'frases-para-invitados-de-boda.html',
    'frases-para-los-novios.html',
    'frases-religiosas-para-bodas.html',
]
# Legal/info pages intentionally excluded: about / contact / privacy-policy / terms


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(strip_tags(s))).strip()


def extract_visible_faq(c):
    """Return list of (question, answer) from the visible FAQ card, or None."""
    m = re.search(r'<h2>%s</h2>(.*?)</main>' % FAQ_HEADING, c, re.S)
    if not m:
        return None
    section = m.group(1)
    items = re.findall(
        r'<div class="faq-item"><b>(.*?)</b><p>(.*?)</p></div>', section, re.S
    )
    if not items:
        return None
    return [(clean(q), clean(a)) for q, a in items]


def build_json(items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def process(fn, dry):
    path = os.path.join(ROOT, fn)
    if not os.path.exists(path):
        print("MISSING: %s" % fn)
        return False
    c = open(path, encoding='utf-8').read()
    if '"@type": "FAQPage"' in c:
        print("SKIP (has FAQPage JSON-LD): %s" % fn)
        return False
    items = extract_visible_faq(c)
    if not items:
        print("WARN no visible FAQ card in %s — skipping" % fn)
        return False
    json_block = ('  <script type="application/ld+json">\n%s\n  </script>\n'
                  % build_json(items))
    new = c.replace('</head>', json_block + '</head>', 1)
    if dry:
        print("[dry] %s: extract %d Q/A from visible card" % (fn, len(items)))
        return False
    open(path, 'w', encoding='utf-8').write(new)
    print("ADDED FAQ JSON-LD: %s (%d Q/A)" % (fn, len(items)))
    return True


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    changed = 0
    for fn in TARGETS:
        if process(fn, dry):
            changed += 1
    print("\nDone. %sPages changed: %d/%d" % ('[dry-run] ' if dry else '', changed, len(TARGETS)))
