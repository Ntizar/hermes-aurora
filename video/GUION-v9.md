# GUION v9 — «CATALOGUE & INSPECTOR» (70 s)

> Reorganización completa del film. Cambios que pidió David:
> 1. **Logo azul + naranja** (AURORA en azul, punto naranja). Fuera el arcoíris.
> 2. **Explicarlo para técnicos y no técnicos**: primero en palabras llanas (catálogo + inspector),
>    después en términos de ingeniería (censo + validador + skills).
> 3. **Ejemplos de webs pre-hechas**: seis esqueletos de página reales (landing, dashboard, login,
>    shop, chat, app) — el agente rellena, no reinventa.
> 4. **Sin sonido entre escenas**: cero música, cero risers, cero impactos. Solo voz.
> 5. El orden cambia: problema → qué es (dos veces) → qué puedes construir → prueba → receta.

## Contrato de aceptación

1. 70,0 s ±0,5 · 1600×900 · 20 fps · 1 vídeo + 1 audio · **0 subtítulos** · **audio = solo voz**.
2. Las 11 escenas existen y tienen movimiento; 0 rebotes de parpadeo.
3. Voz: −16 LUFS ±2 · true peak < −1 dBFS · sin música ni SFX (se comprueba comparando el
   audio final con la suma de las voces: diferencia < 1 dB RMS en los tramos sin voz).
4. Logo: solo `#3a7aff` + `#ff6a00` en la marca (AURORA azul, punto naranja).
5. Cero datos inventados: 2.223 clases, 417 familias, 18 packs, 4 skills, 2 tools, v10.10.0.
6. Se entiende sin audio: cada escena lleva su frase clave escrita.

## Estructura

| # | Escena | Acto | Qué se ve |
|---|--------|------|-----------|
| 00 | open | — | 6 hojas de cristal se cierran; el agente teclea «build me a pricing page» y la página aparece |
| 01 | looks finished | 01 | página limpia + tres faltas que no se ven; «Looks finished. It isn't.» |
| 02 | guessing | 02 | muro de clases inventadas cruza la pantalla, tachadas en rojo |
| 03 | plain words | 03 | dos tarjetas: **CATALOGUE** (lo que existe) y **INSPECTOR** (lo que se prueba) |
| 04 | engineers | 04 | `census.json` / `validator.ts` / `SKILL.md ×4` y el resultado real del validador |
| 05 | archetypes | 05 | seis planos de página: landing, dashboard, login, shop, chat, app |
| 06 | inspector | 06 | 4 faltas, sello BLOCKED, «caught in milliseconds» |
| 07 | loop | 07 | 4 → 0, PASSED, el bucle que mata el slop |
| 08 | one attribute | 08 | light/dark del mismo dashboard |
| 09 | recipe | 09 | «Steal the recipe»: tu catálogo, tu inspector, tus skills |
| 10 | close | 10 | AURORA azul + punto naranja, comando, enlaces |

## Voz (kokoro `am_michael`; la 00 en `af_heart`, filtrada como altavoz)

| Escena | Línea |
|---|---|
| 00 | *Build me a pricing page.* |
| 01 | This page looks finished. It isn't. Three things are wrong, and you can't see them. |
| 02 | Your agent doesn't know your system, so it invents classes, gradients and colours nobody approved. |
| 03 | In plain words: a parts catalogue and a building inspector. The catalogue says what exists; the inspector proves what you built. |
| 04 | For engineers: a census, a validator that fails the build, and skills that teach the procedure. |
| 05 | You start from pages that already work: landing, dashboard, login, shop, chat, app. The agent fills them in. |
| 06 | The inspector runs: unknown class, banned gradient, hand-written colour. Caught in milliseconds. |
| 07 | The agent fixes them, runs it again. Zero failures, or it doesn't ship. |
| 08 | One attribute re-themes everything. Light and dark, both designed. |
| 09 | Aurora is the proof. The recipe is yours: your catalogue, your inspector, your skills. |
| 10 | Any agent. Any brand. Zero guessing. Aurora, for Hermes. |

## Dirección

- **Marca**: `#3a7aff` azul + `#ff6a00` naranja. El wordmark es `AURORA` azul con punto naranja;
  el HUD repite ese lockup. Nada de letras multicolor.
- **Doble registro**: la escena 03 habla en objetos cotidianos (catálogo, inspector); la 04 traduce
  los mismos tres objetos a ficheros y comandos. Misma estructura visual en ambas: tres piezas.
- **Planos de página** (05): tarjetas con wireframe dibujado (barra, hero, rejilla, formulario)
  + nombre de fichero real (`landing.html`, `dashboard.html`…). No capturas rotas.
- **Audio**: solo voz. Silencio entre frases; el ritmo lo lleva el montaje, no la música.
- HUD, grano, viñeta y cristal por clon como en v8 (refracción real, no blur).

## Pipeline

`voz-v9.py` → `plan-v9.py` (70,0 s) → `slides-v9.py` → `rasterizar-v9.py` (frames9/)
→ `montar-v9.py` (solo voz) → `qa-v9.py`.

Atribución: **Hecho con ❤️ por David Antizar**.
