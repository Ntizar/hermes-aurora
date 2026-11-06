# GUION v7 — "PORTAL DE CRISTAL" para el concurso (69 s)

> Dirección elegida por David: **liquid glass de verdad** (Apple-vision). El código del
> agente viaja por portales de vidrio y la página final emerge **refractada** (feDisplacementMap,
> no blur). Mantiene: color por marca, voz am_michael, cero subtítulos, cero parpadeo.

## Doctrina visual (de la skill nivel-premio, citando la técnica)

- **Refracción**: el fondo de cada escena (luces de marca + retícula de medidas) se **clona**
  dentro de cada portal vía `background-position` negativo y se le aplica `filter:url(#lg)`
  (feTurbulence seed fijo → feGaussianBlur 1.2 → feDisplacementMap scale 24). Clon y no
  `backdrop-filter` porque el url() de backdrop se ignora en silencio según motor: el clon
  refringe SIEMPRE y es determinista. La sonda `qa-refraccion-v7.py` lo mide (MAD lente vs
  blur-puro > 10).
- **Especular**: `inset 0 1px 0 rgba(255,255,255,.8)` + edge lightening por gradiente 150°.
- **Cristal solo en el chrome** (la regla que casi todos incumplen): el texto/dato va sobre
  chip sólido dentro del cristal, nunca flotando en el vidrio.
- **Reflejo**: `-webkit-box-reflect` bajo los portales héroe.
- **Fondo con luz + grano + viñeta**: el negro puro parece vacío.
- Grano: feTurbulence en data-uri, `mix-blend-mode: overlay`, 5%.

## Estructura (11 escenas — mismas duraciones y voces que v6)

| # | Escena | Cristal | Marca |
|---|--------|---------|-------|
| 00 | Portal héroe: cortinas de luz de marca tras el vidrio; AURORA emerge nítido delante | portal central gigante | ntizar |
| 01 | Beat «Every agent can build a page» + barra de cristal | píldora chrome | ntizar |
| 02 | Beat «…can prove it's real» | píldora chrome | indigo |
| 03 | AURORA en la vitrina de cristal, reflejo bajo el marco | portal 1200×600 | ntizar (light) |
| 04 | aurora_search: terminal tras el vidrio, JSON emerge refractado | portal-terminal | aurora (light) |
| 05 | Tríptico en tres vitrinas con sus marcas | 3 portales | triple |
| 06 | aurora_validate: el fracaso tras el rojo | portal-terminal | carmesi |
| 07 | Limpio: ok:true + dashboard en vitrina verde | portal | esmeralda (light) |
| 08 | Light/dark: dos portales, mismo markup | 2 portales | aurora |
| 09 | Instalar: consola de vidrio violeta | portal-terminal | violeta |
| 10 | Cierre: AURORA multicolor + comando en píldora de cristal | píldora | ntizar |

## AUDIOS — sin cambios (audio5/, `GUION-v6.md`); la dirección es visual.

## Pipeline v7

`slides-v7.py` → `rasterizar-v8.py` (frames7/, determinista igual que v7 del rasterizador:
un solo dueño del tiempo) → `montar-v7.py` (demo7.mp4, sin subtítulos) → QA brillo
(rebotes) + QA refracción (MAD lente).
