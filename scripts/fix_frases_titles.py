#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0 title CTR tune for Frases-para-Boda (Spanish site).

Chosen from the real GSC query report, not guesswork:

  index.html
    old: Frases para Boda – 60+ Frases Originales, Cortas y Bonitas
    new: Frases para Boda – 60+ Mensajes, Tarjetas y Dedicatorias
    why: swaps style adjectives for the SCENARIO words users actually search
         ("mensajes", "tarjetas", "dedicatorias" all appear in the query report).
         The dropped style words are already covered by the dedicated pages
         (frases-para-bodas-originales / frases-cortas-para-felicitar-bodas),
         so keeping them on the homepage only caused internal competition.

  frases-para-bodas-de-oro.html
    old: Frases para Bodas de Oro – 30+ Mensajes para 50 Años
    new: Frases para Bodas de Oro – 50+ Mensajes y Citas para 50 Años
    why: 14 of the site's impressions cluster on the "bodas de oro" cluster
         (frases/citas/textos). Bumps 30+ -> 50+ and adds the "Citas" synonym,
         while keeping "50 Años" which carries the real search volume.

Keeps title / og:title / twitter:title in sync. Idempotent. Supports --dry.
"""
import os, sys

ROOT = "."
TITLE_FIX = {
    'index.html': (
        'Frases para Boda – 60+ Frases Originales, Cortas y Bonitas',
        'Frases para Boda – 60+ Mensajes, Tarjetas y Dedicatorias',
    ),
    'frases-para-bodas-de-oro.html': (
        'Frases para Bodas de Oro – 30+ Mensajes para 50 Años',
        'Frases para Bodas de Oro – 50+ Mensajes y Citas para 50 Años',
    ),
}


def process(fn, dry):
    path = os.path.join(ROOT, fn)
    if not os.path.exists(path):
        print("MISSING: %s" % fn)
        return False
    c = open(path, encoding='utf-8').read()
    old, new = TITLE_FIX[fn]
    if new in c:
        print("SKIP (already applied): %s" % fn)
        return False
    if old not in c:
        print("WARN old title NOT FOUND in %s — skipping" % fn)
        return False
    new_c = c
    new_c = new_c.replace('<title>%s</title>' % old, '<title>%s</title>' % new, 1)
    new_c = new_c.replace(
        '<meta property="og:title" content="%s">' % old,
        '<meta property="og:title" content="%s">' % new, 1)
    new_c = new_c.replace(
        '<meta name="twitter:title" content="%s">' % old,
        '<meta name="twitter:title" content="%s">' % new, 1)
    if dry:
        print("[dry] %s: %s  ->  %s" % (fn, old, new))
        return False
    open(path, 'w', encoding='utf-8').write(new_c)
    print("FIXED %s: %s  ->  %s" % (fn, old, new))
    return True


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    changed = 0
    for fn in TITLE_FIX:
        if process(fn, dry):
            changed += 1
    print("\nDone. %sPages changed: %d/%d" % ('[dry-run] ' if dry else '', changed, len(TITLE_FIX)))
