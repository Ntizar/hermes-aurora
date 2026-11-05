---
name: aurora-generative
description: "Use when a model must generate Aurora UI at runtime: openui-lang prompt, spec, runtime and static baking."
version: 1.0.0
license: MIT
tags: [design-system, css, openui, generative, aurora]
---

# Aurora — generative layer (openui-lang)

When the HTML is written **by a model at runtime**, do not hand it this skill and do not ask it
for HTML. Give it the language and the library: both live in the repo.

```
LLM → OpenUI Lang (8–20 lines) → parser → vanilla runtime → .nz-* census markup
```

| Need | Where (repo) |
|---|---|
| System prompt for the model | `openui/PROMPT.md` (component signatures + design rules + 3 examples) |
| Machine-readable library | `openui/aurora.spec.json` (signatures + JSON Schema for the parser) |
| Paint the result | `openui/aurora-openui.js` → `AuroraOpenUI.iniciar()` + `.stream(text, "#lienzo")` |
| Add an object to the language | `openui/componentes.json` (by hand) → `python3 scripts/generar-openui.py` |
| Live playground | `openui/index.html` (tester + templates) |
| Start from an archetype | `openui/plantillas/` + `scripts/plantilla.py` (panel, report, landing, settings, agent, deck) |
| Brief → page | `scripts/generar-web.py --brief encargo.json` (model + validation + lint) |
| Program → static HTML | `scripts/programa-a-html.py page.openui --salida out.html --marca X --tema light --canal vivo` |
| Program → baked static page (no JS) | `scripts/hornear.py page.openui --salida out.html --plantilla-base` |
| An agent asks the system directly | `scripts/mcp-aurora.py` (stdio MCP, stdlib only) |

## Rules of the layer

1. **OpenUI supplies the language; Aurora supplies visual truth.** Never link OpenUI's React
   library or its CSS (3.2 MB + 320 KB that would fight the system). Only the parser
   (`@openuidev/lang-core`) is used.
2. **Every component emits census markup.** `scripts/auditar-openui.py` fails if the runtime
   emits a class that does not exist, if a renderer is missing, or if spec/prompt drifted.
3. **Spanish enum ≠ modifier.** `tendencia: "sube"` → `nz-kpi__delta--up`. A blind concatenation
   produces phantom classes.
4. **`Fila` is `nz-cluster`, not `nz-row`.** An action group measures what it measures; `nz-row`
   stretches children to 100 % on mobile and 50 % from 640, turning a button into a block.
5. **Compact figures by default.** `Barras` emits only the bars (5 rem), not a
   `<figure class="nz-chart">`: inside a card that is two nested surfaces and a wall in a 4-up
   grid. `lg` is for the protagonist chart only.
6. **Short button labels**; the button wraps (`white-space: normal`). With `nowrap`, a long label
   inside a grid overflows.
7. **Start from a template, not from zero.** If the brief matches an archetype, fill its
   template: the structure is already audited and the model only changes data.
8. **Validate arguments before compiling.** The runtime does not check them: a boolean where an
   enum belongs paints `.nz-btn--true` (an invented class) and a string where a list belongs is
   printed as visible content. Validate against `spec.schema.$defs`.
9. **Bake, don't paste.** If the page must speak to SEO or must not depend on JS, `hornear.py`
   compiles, serves the repo over local HTTP, paints in headless Chrome and extracts the
   rendered `<main>`. Never write that HTML by hand from the program — that is how a page once
   promised "the program is shown below" with nothing below.

## Variant ≠ decoration

If the request asks for *different* layouts, variety is paid with **structure** (which
components, in what order, at what density), never with more shadows or colour. Measure: N
styles must produce N distinct component sets and block sequences, all passing the lint with
zero findings. If surfaces, shadows or brand moments go up when you diversify, you understood
the request backwards.

## Pitfall: a compiled page paints on the client

The compiler leaves `<main>` empty and embeds the program plus the runtime. The first paint
right after load shows Times New Roman and 0 components — it is not broken, the runtime is
still resolving the spec. Wait ~3 s, then measure computed styles, `.nz-*` selectors and
overflow before concluding anything. `probar-producto.py` and the baking path exist precisely
so you don't depend on that wait.
