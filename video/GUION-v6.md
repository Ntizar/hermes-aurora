# GUION v6 — vídeo de hermes-aurora para el concurso (69 s)

> Cambios sobre v5: SIN subtítulos (el audio ya narra), COLOR por escena (una marca de
> Aurora cada tramo: ntizar, indigo, aurora, esmeralda, carmesi, violeta), intro three.js
> con partículas multicolor y SEMILLA fija, y revelados deterministas (el rasterizador
> calcula la opacidad por fotograma: nada de CSS-anim peleándose con inline → cero parpadeo).
> Base: cada escena renderizada está en su estado FINAL (el dato nunca depende del JS).

## Estructura (11 escenas)

| # | Escena | Marca | Tema | Duración |
|---|--------|-------|------|----------|
| 00 | Intro: campo de partículas arcoíris-Aurora converge en el anillo; aparece AURORA | — (seis marcas) | negro azulado | 4.8 (muda) |
| 01 | Beat: «Every agent can build a page» | ntizar | dark | 3.8 |
| 02 | Beat: «Almost none can prove it's real» | indigo | dark | 3.6 |
| 03 | Nombre: AURORA. gigante azul, subtítulo | ntizar | light | 4.4 |
| 04 | aurora_search: terminal teclea, JSON con markup real | aurora | light | 9.2 |
| 05 | Tríptico: landing (ntizar) + dashboard (esmeralda) + login (violeta) | triple | light | 8.3 |
| 06 | aurora_validate: el auditor tachando inventos | carmesi | dark | 8.0 |
| 07 | Limpio: ok:true + dashboard esmeralda | esmeralda | light | 6.9 |
| 08 | Light/dark del mismo dashboard, un atributo | aurora | dark | 8.2 |
| 09 | Instalar: `hermes plugins install…` ✓ | violeta | dark | 5.4 |
| 10 | Cierre multicolor: marca + comando + enlaces | las seis | ntizar | 6.4 |

## AUDIOS (voz am_michael, EN — las frases exactas de `voz-v5.py`)

1. 01: "Every AI agent can build you a page."
2. 02: "Almost none can prove the page is real."
3. 03: "Aurora. A design system your agent cannot fake."
4. 04: "It never guesses. It asks the census: two thousand two hundred twenty three real objects, real markup, every class."
5. 05: "The same system behind a landing, a dashboard, a login. Four brands. Light and dark. All of it audited."
6. 06: "Then the auditor strikes. Invented classes. Fake gradients. Hand written colors. Caught in milliseconds."
7. 07: "The agent fixes. The agent iterates. Until the report is spotless: zero failures."
8. 08: "And here's the magic trick. One attribute. The whole product, re-themed. Both designed, nothing improvised."
9. 09: "Aurora for Hermes. Two tools. Four skills. Zero network."
10. 10: "Stop admiring screenshots. Start shipping proof. Aurora, for Hermes."

(00 es instrumental muda: la música no — solo el campo three.js.)

## Reglas de producción v6

- Nada de `<script>` ni `@keyframes` en las escenas: tiping, reveals y ken-burns los
  calcula `rasterizar-v7.py` por fotograma e inyecta `style` inline. Mismo t ⇒ mismo frame.
- 00-three: PRNG con semilla (mulberry32) — cada carga dibuja EXACTAMENTE el mismo campo.
- Imágenes de producto a color: `video/slides/img/*.png` (capturar-colores.py), una marca
  distinta en cada captura (ntizar / aurora / esmeralda / violeta).
- Sin subtítulos en el montaje: sale `demo6.mp4` directo de `montar-v6.py`.
