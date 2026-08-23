# Frases para Boda — Sitio Web

**Sitio:** https://frasesparaboda.com
**Idioma:** Español
**Tema:** Frases y mensajes para bodas (originales, cortas, graciosas, religiosas, invitaciones, aniversarios, bodas de oro)

## 📁 Estructura de archivos

| Archivo | Descripción |
|---|---|
| `index.html` | Página principal: frases destacadas + navegación por categorías |
| `frases-para-bodas-originales.html` | Frases originales y creativas |
| `frases-cortas-para-felicitar-bodas.html` | Frases cortas para tarjetas y mensajes |
| `frases-graciosas-para-bodas.html` | Frases con humor |
| `frases-religiosas-para-bodas.html` | Frases con bendiciones |
| `frases-para-invitaciones-de-boda.html` | Textos para invitaciones |
| `frases-para-aniversario-de-bodas.html` | Mensajes de aniversario |
| `frases-para-bodas-de-oro.html` | Frases para 50 años de matrimonio |
| `frases-para-los-novios.html` | Mensajes dedicados a los novios |
| `frases-para-invitados-de-boda.html` | Frases para libro de firmas y brindis |
| `about.html` / `contact.html` / `privacy-policy.html` / `terms.html` | Páginas de confianza |
| `wordbank.json` | Base de datos de frases (para generar más páginas) |
| `generate_pages.py` | Script para generar páginas desde el wordbank |
| `sitemap.xml` | Mapa del sitio (14 URLs) |
| `robots.txt` | Reglas para buscadores |

## 🚀 Pasos de despliegue

1. **GA4**: Crear nueva propiedad en Google Analytics → "frases-paraboda" → copiar Measurement ID (formato `G-XXXX...`)
2. **Reemplazar ID**: Buscar `G-XXXXXXXXXX` en los 10 archivos HTML y reemplazar por el ID real
3. **GitHub**: Crear repositorio `frases-paraboda` → subir todos los archivos
4. **Vercel**: Importar el repositorio → añadir dominio `frasesparaboda.com` → DNS CNAME en Cloudflare
5. **GSC**: Añadir propiedad de dominio `frasesparaboda.com` → verificar → enviar sitemap: `https://www.frasesparaboda.com/sitemap.xml`
6. **Email**: Configurar Email Routing en Cloudflare → `hola@frasesparaboda.com` → reenviar a Gmail

## 📊 Eventos GA4

- `frase_copiada` — cuando un usuario copia una frase (evento clave)

## 📌 Notas

- El sitio está en español, orientado al mercado de España + hispanohablantes de EE.UU.
- KD promedio del nicho: 16% (competencia baja)
- Volumen total del nicho: ~27,000 búsquedas/mes en España
