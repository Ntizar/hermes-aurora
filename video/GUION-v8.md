# GUION v8 — «THE RECIPE» (70 s)

> Reescritura del vídeo de hermes-aurora para el concurso de Nous.
> **Cambio de tesis:** el vídeo ya no dice «Aurora es bonita», dice **«cualquiera puede
> convertir su design system en uno que la IA no pueda romper»**. Aurora es la prueba;
> la receta (censo + juez + skills) es lo que se lleva el espectador.
>
> Base técnica: portal de cristal v7 (refracción real por clon, `feDisplacementMap`),
> HUD de película, cámara con shake en los impactos, contadores y barridos especulares
> calculados por fotograma. Sin `@keyframes`: `rasterizar-v9.py` es el único dueño del tiempo.

## Contrato de aceptación (se comprueba al final, no se supone)

1. **70,0 s ±0,5** de vídeo, 1600×900, 20 fps, h264 yuv420p, **1 stream de vídeo + 1 de audio, 0 subtítulos**.
2. **Las 11 escenas existen**: luma media > 20 en el fotograma central de cada una (ninguna sale negra).
3. **Sin parpadeo**: `qa-brillo` no detecta rebotes > 18 niveles; los fundidos son monótonos.
4. **Voz limpia**: −16 LUFS ±2, true peak < −1 dBFS, música al menos 18 dB por debajo de la voz.
5. **Cero datos inventados**: 2.223 clases, 417 familias, 18 packs, 4 skills, 2 tools, v10.10.0
   (todo sale de `data/censo.json` y de `plugin.yaml`).
6. **Se entiende sin audio**: cada escena lleva su etiqueta de acto y su frase clave en pantalla.

## Tesis en una frase

Un design system para IA no es un tema: es un **contrato** — un censo de lo que existe,
un juez que lo comprueba y skills que enseñan el procedimiento. Cualquiera puede copiar la receta.

## Estructura (70 s)

| # | Escena | Acto | Marca | Idea visual |
|---|--------|------|-------|-------------|
| 00 | cold open | — | ntizar | 6 hojas de cristal entran y se cierran en un portal; dentro, el agente teclea su encargo y la página aparece |
| 01 | la promesa | 01 | ntizar | «Any page. In seconds.» tipografía enorme + landing viva tras el vidrio, cortada por el borde |
| 02 | el hueco | 02 | carmesi | la misma página, anotada en rojo: clase inventada, gradiente prohibido, color a mano; sello **UNVERIFIED** |
| 03 | el contrato | 03 | aurora | «A contract, not a prompt.» Tres filas de cristal: CENSUS / JUDGE / SKILLS con sus cifras |
| 04 | el censo | 04 | aurora | terminal a sangre: la consulta se teclea, el JSON se materializa, contador **2.223** sube |
| 05 | una marca, cualquier marca | 05 | esmeralda | tríptico asimétrico: landing grande + dashboard + login, cada uno con su marca |
| 06 | el juez | 06 | carmesi | las 4 violaciones entran una a una y golpean; sello **BLOCKED** y shake de cámara |
| 07 | el bucle | 07 | esmeralda | contador 4→0, pips rojo→verde, PASSED, el dashboard limpio |
| 08 | un atributo | 08 | violeta | split light/dark con costura de cristal y el atributo tecleándose en la junta |
| 09 | la receta | 09 | indigo | «Steal the recipe.» tres ficheros: census.json / judge.py / SKILL.md → your system |
| 10 | cierre | 10 | ntizar | wordmark multicolor, «Any agent. Any brand. Zero guessing.», comando y enlaces |

## Voz (kokoro `am_michael`, EN — concurso en inglés)

| Escena | Línea |
|---|---|
| 00 | *(voz de máquina, `af_heart`, filtrada)* «Build me a landing page.» |
| 01 | Your AI agent can build a page in seconds. Beautiful, fast, and completely improvised. |
| 02 | It doesn't know your system. So it invents class names, paints gradients nobody approved, and calls it done. |
| 03 | The fix isn't a better prompt. It's a contract. Three pieces: a census, a judge, and skills. |
| 04 | The census is what exists: every object, every class, the real markup. Machine-readable, so the agent looks it up instead of guessing. |
| 05 | One system, four brands, three products: landing, dashboard, login. All audited. |
| 06 | Then the judge checks the page. Invented classes, banned gradients, hand-written colours: caught in milliseconds, before you ever see it. |
| 07 | So the agent fixes it, and runs it again. Zero failures, or it doesn't ship. That's the loop that kills slop. |
| 08 | One attribute, and the whole product re-themes. Light and dark, both designed, nothing improvised. |
| 09 | Aurora is the proof. The recipe is yours: your census, your judge, your skills. |
| 10 | Any agent. Any brand. Zero guessing. Aurora, for Hermes. |

## Timeline real (sale de `manifest-v8.json`)

| Escena | Entra | Dura |
|---|---|---|
| 00 open | 0,00 | 3,80 |
| 01 hook | 3,80 | 6,60 |
| 02 hueco | 10,40 | 7,30 |
| 03 contrato | 17,70 | 5,80 |
| 04 censo | 23,50 | 7,65 |
| 05 marcas | 31,15 | 6,25 |
| 06 juez | 37,40 | 7,55 |
| 07 bucle | 44,95 | 7,45 |
| 08 tema | 52,40 | 6,95 |
| 09 receta | 59,35 | 6,00 |
| 10 cierre | 65,35 | 4,65 |

## Dirección de arte

- **HUD de película** en todas las escenas: wordmark arriba a izquierda, acto `N / 10` arriba a
  derecha, etiqueta de acto abajo a izquierda, barra de progreso de 2 px a sangre. Es lo que
  convierte una presentación en un film.
- **Asimetría editorial**: titular a la izquierda a 96–140 px, panel de cristal a la derecha y
  **cortado por el borde** del encuadre. Nunca tres tarjetas iguales centradas.
- **Cristal con contraste detrás**: las cortinas de aurora suben de saturación (alfa .18–.38) y
  se añaden núcleos finos brillantes; sin eso la refracción no existe y parece un blur.
- **Cristal solo para el chrome**; el dato va sobre chip oscuro o delante, nítido.
- **Impactos**: shake de cámara de 6 px con caída exponencial + flash de marca al 8 %.
- **Contadores** calculados por fotograma (2.223, 4→0) — nunca un número que no se mueva.
- **Grano + viñeta + retícula** en todas las escenas; el negro puro se lee como vacío.

## Pipeline

`slides-v8.py` → `rasterizar-v9.py` (frames8/) → `voz-v8.py` (audio8/) → `musica-v8.py`
(cama + SFX) → `montar-v8.py` (demo8.mp4, audio mezclado con ducking) → `qa-v8.py`.

Atribución: **Hecho con ❤️ por David Antizar**.
