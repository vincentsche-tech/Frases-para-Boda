"""
frases-para-boda P0 修复脚本
A. 全站 17 页补 hreflang="es" + "x-default"（追加到 canonical 后）
B. index + 11 子页 title 加 emoji + 年份(2026) + 数字升级（同步 og/twitter）
C. 不动 FAQPage（11 子页 + index 已有，固守事实）/ 不动 WebApplication / 不动 sitemap
"""
import re, sys

BASE = "https://www.frasesparaboda.com"
FILES = [
    "index.html",
    "about.html", "contact.html", "privacy-policy.html", "terms.html",
    "dedicatorias-para-bodas.html",
    "frases-cortas-para-felicitar-bodas.html",
    "frases-graciosas-para-bodas.html",
    "frases-para-aniversario-de-bodas.html",
    "frases-para-bodas-de-oro.html",
    "frases-para-bodas-originales.html",
    "frases-para-invitaciones-de-boda.html",
    "frases-para-invitados-de-boda.html",
    "frases-para-los-novios.html",
    "frases-para-tarjetas-de-boda.html",
    "frases-religiosas-para-bodas.html",
]

# 子页 title 重写表（em dash / emoji + 数字升级）
TITLE_REWRITE = {
    "index.html": "Frases para Boda — 💍 +200 Mensajes Originales, Graciosos y de Amor (2026)",
    "about.html": None,
    "contact.html": None,
    "privacy-policy.html": None,
    "terms.html": None,
    "dedicatorias-para-bodas.html": "Dedicatorias para Bodas — 💍 +50 Mensajes Emotivos para los Novios (2026)",
    "frases-cortas-para-felicitar-bodas.html": "Frases Cortas para Bodas — ✉️ +80 Mensajes Breves y Bonitos (2026)",
    "frases-graciosas-para-bodas.html": "Frases Graciosas para Bodas — 😂 +60 Mensajes Divertidos e Originales (2026)",
    "frases-para-aniversario-de-bodas.html": "Frases para Aniversario de Bodas — 🎉 +70 Mensajes para Celebrar (2026)",
    "frases-para-bodas-de-oro.html": "Frases para Bodas de Oro — 🥇 +50 Mensajes para 50 Años (2026)",
    "frases-para-bodas-originales.html": "Frases para Bodas Originales — 💡 +70 Mensajes Únicos (2026)",
    "frases-para-invitaciones-de-boda.html": "Frases para Invitaciones de Boda — 💌 +60 Mensajes para Tarjetas (2026)",
    "frases-para-invitados-de-boda.html": "Frases para Invitados de Boda — 👰 +50 Mensajes para Invitados (2026)",
    "frases-para-los-novios.html": "Frases para los Novios — 💕 +80 Mensajes Románticos y Bonitos (2026)",
    "frases-para-tarjetas-de-boda.html": "Frases para Tarjetas de Boda — 💌 +70 Mensajes para Felicitar (2026)",
    "frases-religiosas-para-bodas.html": "Frases Religiosas para Bodas — ⛪ +50 Mensajes con Bendición (2026)",
}

DRY = "--dry" in sys.argv

for fn in FILES:
    p = r'D:\workbuddy-出海web\Frases-para-Boda' + "\\" + fn
    s = open(p, encoding="utf-8").read()

    # 1) hreflang 锚点：canonical link
    can = re.search(r'<link rel="canonical" href="([^"]+)">', s)
    if not can:
        print(f"[{fn}] ✗ NO canonical - skip")
        continue
    can_url = can.group(1)
    # 期望 hreflang 锚点：当前 canonical 那一行
    anchor = can.group(0)
    if 'hreflang="es"' in s:
        print(f"[{fn}] hreflang already present - skip hreflang step")
        hreflang_done = True
    else:
        hreflang_block = (
            anchor + '\n<link rel="alternate" hreflang="es" href="' + can_url + '">'
            + '\n<link rel="alternate" hreflang="x-default" href="' + can_url + '">'
        )
        if DRY:
            print(f"[{fn}] +hreflang → " + can_url)
        else:
            s = s.replace(anchor, hreflang_block, 1)
            hreflang_done = True

    # 2) title 升级
    new_title = TITLE_REWRITE.get(fn)
    if new_title:
        # 检查是否已含 (2026)
        cur = re.search(r'<title>([^<]+)</title>', s)
        if cur and "(2026)" in cur.group(1):
            print(f"[{fn}] title already (2026) - skip title step")
            title_done = True
        else:
            old_title = cur.group(1) if cur else "?"
            new_og = new_title
            # title
            s = re.sub(r'<title>[^<]+</title>', '<title>' + new_title + '</title>', s, count=1)
            # og:title
            s = re.sub(
                r'<meta property="og:title" content="[^"]+">',
                f'<meta property="og:title" content="{new_og}">',
                s, count=1
            )
            # twitter:title
            s = re.sub(
                r'<meta name="twitter:title" content="[^"]+">',
                f'<meta name="twitter:title" content="{new_og}">',
                s, count=1
            )
            if DRY:
                print(f"[{fn}] title: {old_title!r} → {new_title!r}")
            else:
                title_done = True
    else:
        if DRY:
            print(f"[{fn}] no title rewrite planned (content page)")
        title_done = True

    # 写入
    if not DRY and (hreflang_done or title_done):
        open(p, "w", encoding="utf-8").write(s)
        print(f"[{fn}] WRITE OK (hreflang={hreflang_done}, title={title_done})")
