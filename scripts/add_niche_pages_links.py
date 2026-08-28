# -*- coding: utf-8 -*-
"""
Frases-para-Boda: 把两个新 niche 页挂进全站 grid 内链 + sitemap。
- 对每个含 <div class="grid"> 的页，在 grid 内最后一个 </a> 之后，注入该页尚缺的新 card（幂等）
- sitemap.xml 在 </urlset> 前追加两个新 <url>（lastmod = 今天）
"""
import os, re, sys

ROOT = '.'
TODAY = '2026-08-28'
NEW_CARDS = {
    'dedicatorias-para-bodas.html':
        '      <a class="scene-card" href="/dedicatorias-para-bodas.html"><b>\u2728 Dedicatorias</b><span>Mensajes emotivos para felicitar a los novios con todo el cari\u00f1o.</span></a>\n',
    'frases-para-tarjetas-de-boda.html':
        '      <a class="scene-card" href="/frases-para-tarjetas-de-boda.html"><b>\u2709\ufe0f Tarjetas</b><span>Frases cortas y bonitas para tarjetas de boda e invitaciones.</span></a>\n',
}
SITEMAP_URLS = (
    '<url><loc>https://www.frasesparaboda.com/dedicatorias-para-bodas.html</loc>'
    '<lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
    '<url><loc>https://www.frasesparaboda.com/frases-para-tarjetas-de-boda.html</loc>'
    '<lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
    '</urlset>' % (TODAY, TODAY)
)


def inject_into(path, dry=False):
    c = open(path, encoding='utf-8').read()
    if '<div class="grid">' not in c:
        return False
    grid_start = c.index('<div class="grid">')
    grid_end = c.index('</div>', grid_start)
    last_a = c.rfind('</a>', grid_start, grid_end)
    if last_a == -1:
        return False
    added = [card for href, card in NEW_CARDS.items() if ('/' + href) not in c]
    if not added:
        return False
    if dry:
        print('  [dry] %s -> would add %d card(s)' % (path, len(added)))
        return True
    new_c = c[:last_a + 4] + ''.join(added) + c[last_a + 4:]
    open(path, 'w', encoding='utf-8').write(new_c)
    return True


def update_sitemap(dry=False):
    sm = 'sitemap.xml'
    c = open(sm, encoding='utf-8').read()
    if 'dedicatorias-para-bodas.html' in c:
        print('  sitemap already has new urls')
        return
    if dry:
        print('  [dry] sitemap.xml -> would add 2 urls')
        return
    c = c.replace('</urlset>', SITEMAP_URLS)
    open(sm, 'w', encoding='utf-8').write(c)
    print('  sitemap.xml updated (+2 urls)')


def main():
    dry = '--dry' in sys.argv
    print('=== %s MODE ===' % ('DRY' if dry else 'APPLY'))
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
    injected = 0
    for fn in pages:
        if inject_into(fn, dry=dry):
            injected += 1
    print('pages touched: %d' % injected)
    update_sitemap(dry=dry)


if __name__ == '__main__':
    main()
