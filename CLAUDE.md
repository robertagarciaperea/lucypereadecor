# Lucy Perea Decor — cómo editar y publicar la página

Página de lucypereadecor.com (catálogo de Navidad, Querétaro). Cliente: Lucy Perea / Roberta García. Responder en español, tono cálido y sencillo; la persona no es técnica.

## Cómo está hecha
- `index.html` (raíz) es la página publicada. **No editarlo a mano**: se genera.
- `fuente/template.html`: diseño (HTML + CSS + JS en un solo archivo).
- `fuente/data.py`: datos (colecciones, precios, `INCLUDES` qué incluye venta/renta, `PIECES` piezas por colección con `*` = agotada, catálogo: ARBOLES, ESFERAS, FOLLAJE, LISTONES, DECORACIONES, INSTALACION).
- `fuente/build.py`: genera `index.html`. `NEW` = colecciones destacadas como Nuevas 2026.
- `fuente/images.txt`: nombres de las fotos (se resuelven por prefijo de 8 caracteres). Las fotos del catálogo se cargan desde el sitio de Canva (`robertagarciabook.my.canva.site/lucypereadecor-catalogo/_assets/media/`), que debe seguir publicado.
- `img/`: fotos propias (aromatizantes Bruma Scent, PNG/WebP con fondo transparente).

## Flujo para cualquier cambio
1. Editar `fuente/data.py` o `fuente/template.html`.
2. `python3 fuente/build.py` (regenera `index.html` en la raíz).
3. Revisar (Playwright con Chromium preinstalado; las fotos de Canva no cargan desde el sandbox, es normal).
4. `git commit` + `git push` a `main` → Cloudflare Pages publica solo en ~1 min.
5. Verificar en https://lucypereadecor.com/?v=<algo> (o lucypereadecor.pages.dev).

## Estilo (no cambiar sin que lo pidan)
Revista navideña de los 2000: papel crema, rojo y verde. Títulos Bodoni Moda, texto Libre Caslon Text, etiquetas Jost. Precios en Caslon negrita. Versión celular con reglas en `@media (max-width:640px)`.
WhatsApp: 52 55 6969 5206. Instalan en Querétaro, CDMX y parte del Edo. Méx.; envíos a toda la República.

## Pendientes conocidos
- Cascanueces rojo de terciopelo: falta foto, tamaño y precio.
- "3 bolas de…" (nota incompleta) y "Ramas: diámetro, no alto" (¿ramas de abedul?).
- Precio de los aromatizantes Bruma Scent.
