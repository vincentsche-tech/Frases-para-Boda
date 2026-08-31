import re
FILES = [
    'index.html',
    'dedicatorias-para-bodas.html',
    'frases-cortas-para-felicitar-bodas.html',
    'frases-graciosas-para-bodas.html',
    'frases-para-aniversario-de-bodas.html',
    'frases-para-bodas-de-oro.html',
    'frases-para-bodas-originales.html',
    'frases-para-invitaciones-de-boda.html',
    'frases-para-invitados-de-boda.html',
    'frases-para-los-novios.html',
    'frases-para-tarjetas-de-boda.html',
    'frases-religiosas-para-bodas.html',
]
EMOJI = {
    'RING': chr(0x1f48d),
    'ENVELOPE': chr(0x2709)+chr(0xfe0f),
    'JOY': chr(0x1f923),
    'PARTY': chr(0x1f389),
    'FIRST': chr(0x1f947),
    'BULB': chr(0x1f4a1),
    'LOVELETTER': chr(0x1f48c),
    'BRIDE': chr(0x1f470),
    'TWOHEART': chr(0x1f495),
    'CHURCH': chr(0x26ea),
}
T = {
    'index.html':                                  f"Frases para Boda {EMOJI['RING']} +200 Originales y Graciosas (2026)",
    'dedicatorias-para-bodas.html':                f"Dedicatorias para Bodas {EMOJI['RING']} +50 Mensajes Emotivos (2026)",
    'frases-cortas-para-felicitar-bodas.html':     f"Frases Cortas para Bodas {EMOJI['ENVELOPE']} +80 Breves y Bonitas (2026)",
    'frases-graciosas-para-bodas.html':            f"Frases Graciosas para Bodas {EMOJI['JOY']} +60 Divertidas (2026)",
    'frases-para-aniversario-de-bodas.html':        f"Frases para Aniversario de Bodas {EMOJI['PARTY']} +70 (2026)",
    'frases-para-bodas-de-oro.html':               f"Frases para Bodas de Oro {EMOJI['FIRST']} +50 para 50 Anos (2026)",
    'frases-para-bodas-originales.html':           f"Frases para Bodas Originales {EMOJI['BULB']} +70 Unicas (2026)",
    'frases-para-invitaciones-de-boda.html':        f"Frases para Invitaciones de Boda {EMOJI['LOVELETTER']} +60 (2026)",
    'frases-para-invitados-de-boda.html':           f"Frases para Invitados de Boda {EMOJI['BRIDE']} +50 (2026)",
    'frases-para-los-novios.html':                 f"Frases para los Novios {EMOJI['TWOHEART']} +80 Romanticas (2026)",
    'frases-para-tarjetas-de-boda.html':           f"Frases para Tarjetas de Boda {EMOJI['LOVELETTER']} +70 Ideas (2026)",
    'frases-religiosas-para-bodas.html':           f"Frases Religiosas para Bodas {EMOJI['CHURCH']} +50 con Fe (2026)",
}
BASE = r'D:\workbuddy-出海web\Frases-para-Boda'
for fn in FILES:
    p = BASE + "\\" + fn
    s = open(p, encoding='utf-8').read()
    new_t = T[fn]
    assert len(new_t) <= 60, f"{fn} OVER: {len(new_t)} {new_t}"
    s = re.sub(r'<title>[^<]+</title>', '<title>' + new_t + '</title>', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]+">', f'<meta property="og:title" content="{new_t}">', s, count=1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]+">', f'<meta name="twitter:title" content="{new_t}">', s, count=1)
    open(p, 'w', encoding='utf-8').write(s)
    print(f"[{fn}] {len(new_t)} chars OK")
