#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frases-para-Boda · P1 加厚 top imp 页（西语）
目标页（GSC imp）：bodas-de-oro(14) / invitaciones(7) / graciosas(6)
每块内容页面感知，避免三页互判近重复。
插入点：短语卡片(.card) 与 "Más Categorías de Frases" 卡片之间（阅读顺序 wishes->guide->more->faq）。
CSS：在 </style> 前补 .guide p/ul/li（幂等）。
"""
import re, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GUIDE_CSS = """  .guide p{font-size:15px;line-height:1.7;margin-top:12px;color:var(--ink);}
  .guide ul{margin:12px 0 0 22px;}
  .guide li{font-size:15px;line-height:1.7;margin-bottom:7px;}
"""

# 每页 3 个 guide 卡，每个 3 段（页面感知，避免近重复）
CONTENT = {
    "frases-para-bodas-de-oro.html": [
        ("🎯 Cómo elegir la frase adecuada para bodas de oro",
         ["El tono de tu mensaje para unas bodas de oro depende sobre todo de quién lo vaya a recibir. Para los abuelos o los padres, una frase cálida y emotiva que reconozca su trayectoria funciona mucho mejor que cualquier broma. En cambio, si la escriben amigos de toda la vida, pueden permitirse un toque más cercano, personal e incluso divertido, porque conocen de sobra la historia de la pareja y sus anécdotas compartidas.",
          "Antes de copiar una frase, pregúntate qué han significado esos cincuenta años para ellos: superación, complicidad, una familia construida día a día. Una sola línea que refleje eso será mucho más recordada que un texto largo y genérico. Añade el nombre de la pareja y un recuerdo concreto para que la frase sea única, personal y difícil de olvidar.",
          "Si dudas entre varias opciones, quédate con la que mejor resuma lo que sientes al verlos juntos tras tanto tiempo. En una fecha que se celebra tan pocas veces, la sinceridad siempre gana al ingenio y se recuerda mucho más años después de la fiesta."]),
        ("🎁 Acompaña la frase con un detalle de oro",
         ["El oro es el regalo tradicional de las bodas de oro por su valor y su durabilidad, exactamente como un matrimonio de cinco décadas. Un marco dorado con su foto de boda, una joya sencilla o un álbum encuadernado en oro son gestos que acompañan perfectamente tu mensaje escrito y refuerzan el símbolo de la fecha que se celebra.",
          "No hace falta gastar mucho para evocar la tradición: una tarjeta con bordes dorados o un sobre metálico ya recuerdan el significado de la celebración. Lo importante es que la frase y el detalle cuenten la misma historia de amor que ha resistido, con paciencia y cariño, el paso de cincuenta años juntos.",
          "Otra idea sencilla y barata es imprimir la frase en una lámina pequeña junto a una foto de ellos el día de su boda y otra de hoy: el contraste de cincuenta años en la misma sonrisa dice más que cualquier discurso preparado de memoria."]),
        ("✍️ Cómo entregar tu mensaje de bodas de oro",
         ["Una tarjeta escrita a mano transmite mucho más que un mensaje de texto, sobre todo en una fecha tan simbólica como esta. Si vas a la celebración, entrégala en persona; si la pareja te lo pide, léela en voz alta durante el brindis para que todos los invitados puedan compartir contigo la emoción del homenaje.",
          "También puedes publicarla en una red social etiquetando a los homenajeados, o enviarla por correo si no puedes asistir. En cualquier formato, firma siempre con tu nombre y, si los conoces desde hace tiempo, menciona un momento concreto de su historia que explique por qué te alegras de verdad por ellos.",
          "Si no puedes asistir, una videollamada con la frase leída en voz alta vale casi tanto como estar presente. Lo que de verdad cuenta no es el formato del mensaje, sino que ellos sepan que alguien ha pensado en su aniversario con cariño y sin prisa."]),
    ],
    "frases-para-invitaciones-de-boda.html": [
        ("✍️ Cómo redactar una invitación con tu propio estilo",
         ["Una invitación debe responder a tres preguntas en pocos segundos: ¿quién se casa?, ¿cuándo y dónde?, ¿qué se espera del invitado? Mantén el tono acorde a la pareja: cercano y relajado si la boda es íntima, más formal y cuidado si se trata de una ceremonia tradicional con familia extensa sentada a la mesa.",
          "Empieza con una frase de bienvenida cálida y deja los datos prácticos para el centro del texto. Evita rellenar con frases hechas que no aportan nada útil; una invitación honesta, clara y bien organizada invita mejor que otra llena de adornos que terminan confundiendo a quien la lee con prisas.",
          "Un truco útil es leer la invitación en voz alta antes de enviarla: si suena natural y responde las dudas de un invitado real, está lista para salir. Si te trabas o suena forzada, acórtala un poco y vuelve a probar hasta que fluya sin esfuerzo."]),
        ("📋 Tipos de invitación según la celebración",
         ["No todas las bodas piden el mismo texto. Una invitación religiosa suele incluir una bendición o una cita de fe; una civil, un tono neutro y alegre; una íntima, palabras cercanas dirigidas a pocos invitados muy queridos. Si hay código de vestuario o niños, conviene aclararlo desde el primer momento para evitar malentendidos.",
          "Adelántate a las dudas más frecuentes: el lugar exacto, si hay aparcamiento, la hora de la ceremonia y la de la fiesta. Una invitación que responde estas preguntas por adelantado reduce las llamadas y los mensajes de última hora, y demuestra que los novios han cuidado cada detalle de su día.",
          "Recuerda que la invitación también marca el tono de toda la celebración: si es divertida, los invitados llegarán relajados; si es solemne, entenderán que se espera un trato más respetuoso. Elige el registro según la boda que de verdad queréis celebrar."]),
        ("📨 Cómo y cuándo enviar la invitación",
         ["La invitación digital por correo o WhatsApp llega al instante y permite confirmar la asistencia con un solo clic, ideal para bodas informales y para invitados que viven lejos. La tarjeta impresa sigue siendo la opción preferida en ceremonias formales y, además, queda como un recuerdo físico que muchos guardan con cariño.",
          "Envía las invitaciones entre dos y tres meses antes de la fecha, y confirma la asistencia unas semanas después para cerrar el aforo con calma. Si usas una frase copiable de esta página, pégalas en tu diseño, añade los datos de contacto de los novios y revisa que la hora y el lugar sean exactos.",
          "Guarda una copia de la invitación ya enviada por si alguien la borra o necesita que se la reenvíes. Un archivo compartido con los datos de la boda ahorra contestar lo mismo una y otra vez en el grupo de la familia y evita equívocos de última hora."]),
    ],
    "frases-graciosas-para-bodas.html": [
        ("😄 Cuándo funciona el humor en una boda",
         ["El humor encaja cuando conoces bien a la pareja y sabes que lo agradecen. Entre amigos cercanos, una frase divertida rompe el hielo y hace la felicitación mucho más memorable que el típico texto serio que todos esperan y que nadie recuerda al día siguiente de la celebración.",
          "Evita el humor en bodas muy formales o religiosas, y nunca te burles de nadie: ni de los novios ni de los invitados. La regla es siempre la misma y muy simple: celebra con una sonrisa, nunca a costa de alguien, por muy buena intención que creas tener al soltar la broma.",
          "Cuando aciertas con la pareja, una frase graciosa se vuelve su favorita y la repiten entre risas durante años. Por eso vale la pena conocerlos bien antes de escribir, en vez de lanzar la primera broma que encuentres por ahí sin pensar en a quién va dirigida."]),
        ("🎭 Tipos de humor para felicitar a los novios",
         ["El juego de palabras sobre el matrimonio, la pareja o el amor suele funcionar porque es ligero y fácil de entender para cualquiera. El humor autoirónico, como las pequeñas locuras de convivir juntos, hace reír sin apuntar a nadie en concreto y resulta especialmente cercano a quien lleva años de relación.",
          "Puedes jugar con temas universales como el baile, la suegra o las discusiones por llegar tarde, siempre desde el cariño y la complicidad. Una buena frase graciosa se queda en la memoria tanto como una emotiva, y además da pie a una conversación divertida durante la propia celebración.",
          "Si no estás seguro del estilo que les gusta, prueba con algo suave y cercano antes que con una broma fuerte. Mejor una sonrisa segura que una carcajada que deje a alguien incómodo en medio del banquete o durante el primer baile de los novios."]),
        ("📲 Dónde usar tus frases graciosas",
         ["El brindis es el escenario perfecto para una frase divertida, sobre todo si hablas en nombre de un grupo de amigos. En la tarjeta de felicitación, una línea graciosa al final equilibra el mensaje cariñoso y evita que la tarjeta parezca demasiado solemne o distante frente a una pareja que prefiere reírse.",
          "También funcionan muy bien en redes sociales o en un WhatsApp al grupo de la boda, donde el tono relajado encaja sin problemas. Eso sí, si la pareja es reservada o muy formal, mejor una sonrisa en privado que un chiste a voz en público que pueda incomodarlos delante de todos los invitados.",
          "Una vez elegida la frase, no la fuerces en todos lados: una broma repetida una y otra vez pierde toda su gracia. Úsala donde encaje de forma natural y deja que el resto del mensaje lleve el cariño que la pareja se merece en su gran día."]),
    ],
}

def build_guide_html(cards):
    parts = []
    for h2, paras in cards:
        block = f'  <div class="card guide">\n    <h2>{h2}</h2>\n'
        for p in paras:
            block += f'    <p>{p}</p>\n'
        block += '  </div>\n'
        parts.append(block)
    return '\n'.join(parts)

def visible_words(c):
    t = re.sub(r'<style.*?</style>', '', c, flags=re.S)
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'&[a-z]+;', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return len(t.split())

def process(fn, dry=False):
    path = os.path.join(BASE, fn)
    c = open(path, encoding='utf-8').read()
    before = visible_words(c)
    if 'class="guide"' in c:
        print(f"[SKIP] {fn} 已有 guide 区块")
        return
    if '.guide p{' not in c:
        c = c.replace('</style>', GUIDE_CSS + '</style>', 1)
    anchor = '<h2>Más Categorías de Frases</h2>'
    if anchor not in c:
        print(f"[ERR] {fn} 找不到插入锚点"); return
    idx = c.index(anchor)
    start = c.rindex('<div class="card">', 0, idx)
    guide = build_guide_html(CONTENT[fn])
    new_c = c[:start] + guide + '\n' + c[start:]
    after = visible_words(new_c)
    flag = 'UNDER 800' if after < 800 else 'OK'
    print(f"{fn}: {before} -> {after} words  [{flag}]")
    if dry:
        return
    open(path, 'w', encoding='utf-8').write(new_c)

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    for fn in CONTENT:
        process(fn, dry=dry)
