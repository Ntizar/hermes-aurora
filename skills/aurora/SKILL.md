---
name: aurora
description: "Use when building or editing any web UI with Aurora (Ntizar). Resolve the live version from the repo first, then compose with census objects only."
version: 1.0.0
license: MIT
tags: [design-system, css, frontend, aurora, tokens]
---

# Aurora — core doctrine

Aurora is a **pure CSS design system**: no build step, no JavaScript, no dependencies.
Everything public is namespaced under `.nz-`. It ships ~18 packs (layout, navigation,
typography, actions, forms, feedback, overlays, data, media, commerce, social, system,
charts, AI, apps, crystal, patterns, stage), a token layer, ~2.200 documented objects and a
numbered icon repository.

**`Ntizar/Aurora` is the source of truth, and this skill is a pointer.** If what you read
here disagrees with the repo, the repo wins — always, without asking.

## Step 0 — resolve the version. Never from memory.

Versions move. What does not move is the procedure.

```bash
# a) from a local clone (fetch first: the clone can be behind origin)
git -C ~/Projects/Aurora fetch --tags -q
V=$(git -C ~/Projects/Aurora describe --tags --abbrev=0)   # e.g. v10.10.0

# b) no clone — ask GitHub
curl -s https://api.github.com/repos/Ntizar/Aurora/tags | grep -m1 '"name"'
```

Then read the generated docs (the repo builds them; never hand-write them):

```bash
curl -s https://cdn.jsdelivr.net/gh/Ntizar/Aurora@master/LLM.md            # ~20 KB, decision guide
curl -s https://cdn.jsdelivr.net/gh/Ntizar/Aurora@master/components.json   # full machine API
```

- **Read from `@master`** (living truth, no cache story needed).
- **Ship a pinned tag.** `@v10` is the *living channel* (moves with each 10.x, good for your
  own sites); an exact tag (`@v10.10.0`) is a *frozen delivery* for a client.
- **Never `@master` in a `<link>`.** jsDelivr caches per edge and a production page must not
  follow an unreviewed commit.
- Before trusting a tag, check it is published and serving:
  `git ls-remote --tags origin | grep vX.Y.Z` and
  `curl -o /dev/null -w "%{http_code}" https://cdn.jsdelivr.net/gh/Ntizar/Aurora@$V/tokens.css`.

## Linking

```html
<html lang="es" data-nz-theme="light" data-nz-marca="monocromo">
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/tokens.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/marcas/monocromo.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p1-layout.css">
  <!-- only the packs you actually use: 12–40 KB each -->
</head>
<body class="nz">
```

- `packs/all.css` is for prototypes only; in production link the 3–7 packs the page needs.
- `tokens.css` **must come before any `marcas/*.css`**: `[data-nz-marca="x"]` and `:root` have
  the same specificity (0,1,0), so the later file wins. Swap the order and the brand silently
  disappears.
- Dark mode is `data-nz-theme="dark"` on `<html>`. Light is the default and the one to design
  first.
- `monocromo` is the standard brand: white canvas, black data, grey only for affordance, with
  one signal colour for the data that matters.

## The hard rules (the repo's CI enforces them)

1. Every public class is `.nz-*`. No global class names.
2. Every value is a `var(--nz-*)` token. No `#2563eb`, no `16px` design values by hand.
3. **0 gradients, 0 `backdrop-filter`, 0 `!important`** — the only exceptions are the crystal
   layer (`p16-cristal.css`, `.nz-cristal`, `data-nz-estilo="cristal"`) and the hiding helpers
   (`.nz-visually-hidden`, `.nz-print-hide`).
4. BEM: `.nz-thing`, `.nz-thing__part`, `.nz-thing--modifier`; state via `.is-x` or `[aria-*]`.
5. Responsive first from the **container** (container queries) and then the viewport: 1 column
   on mobile, grow at 640 / 960 / 1200 / 1440. `max-width` is never the page strategy, and
   "mobile only" is a bug: desktop is a target too.
6. 44 px touch target on anything clickable.
7. One class, one owner: a class is declared in exactly one pack.
8. Footer, verbatim: `Hecho con ❤️ por David Antizar`.
9. Everything in Spanish — copy, and class names when they read better (`nz-arbol`, `nz-filezona`).
10. **Typography with judgement**: 13 px is the interface minimum; 12 px is data only (axes,
    counters, footnotes). Weight is a token (`--nz-peso-normal/medio/fuerte/titulo` = 400/500/
    600/700); **800 does not exist** and nothing under 16 px carries 700. Never load Google
    Fonts: `tokens.css` already serves Inter variable.
11. **Desktop for real**: the canvas grows (72 → 84 rem ≥1200 → 96 rem ≥1440) but type does not.
    A tool (panel, board, table, map, editor) uses `.nz-container--app` to fill the screen.
12. **The accent has a job**: the brand builds structure; the accent marks *the data that
    matters* and the secondary action. Every page has at least one accent moment, and the
    brand never takes more than two thirds of the page.

## Need → object (verified against the census)

| Need | Use |
|---|---|
| Button (p4) | `.nz-btn` + `--primary/--accent/--ghost/--soft/--outline/--danger` + `--sm/--lg/--icon` |
| Surface (p1) | `.nz-article`, `.nz-bento`, `.nz-thirds`, `.nz-hero-bleed` — **`.nz-card` does not exist** |
| Form (p5) | `.nz-field` > `__label` + `.nz-input` + `__help`, `.nz-formgrid`, `.nz-fieldset__leyenda` |
| Choices (p5) | `.nz-checkbox`, `.nz-radio`, `.nz-switch`, `.nz-segmented` |
| Notice (p6) | `.nz-alert--info/--success/--warning/--danger`, `.nz-callout`, `.nz-badge--*` |
| Wide table (p8) | `.nz-table-wrap` > `.nz-table` (+ `--striped`, `__num`, `__status`) |
| Table that must fit (p8) | `.nz-table-wrap--apilable` > `.nz-table--apilable` + `data-etiqueta` per `<td>` |
| KPI (p8) | `.nz-kpi` (`__label/__value/__delta`) |
| Chart (p13) | `.nz-chart` + `.nz-chart-bar/-line/-donut/-gauge`, `.nz-heatmap`, `.nz-sparkline` |
| Mismatched magnitudes (p13) | `.nz-chart-tablebar` — never one scale for 29.262 and 109 |
| Budget vs target (p13) | `.nz-bullet` |
| Dialog (p7) | `.nz-modal` (no JS), `.nz-drawer`, `.nz-sheet` |
| Layout (p1) | `.nz-appshell`, `.nz-with-sidebar`, `.nz-split`, `.nz-dash-grid`, `.nz-container` |
| Nav (p2) | `.nz-navbar`, `.nz-tabs` (`--scroll`, `--pill`), `.nz-breadcrumb`, `.nz-stepper` |
| AI chat (p14) | `.nz-chat`, `.nz-msg`, `.nz-prompt`, `.nz-toolcall`, `.nz-taskplan`, `.nz-approval` |
| Desktop shell (p15) | `.nz-window`, `.nz-appnav`, `.nz-kanban`, `.nz-actbar`, `.nz-statusbar` |
| Slide / talk (p18) | `.nz-escenario` with `.nz-esc-titular/editorial/numeral/etiqueta/dato` |
| Text | body `.nz-prose`, label `.nz-lbl`, lead `.nz-lead`, mute `.nz-text--muted` |
| An icon (p9) | `.nz-icon` + `<svg class="nz-icon"><use href="iconos/sprite.svg#nz-i-042"/></svg>` |

Modifier lexicon (same in all 18 packs): size `--2xs/--xs/--sm/--lg/--xl`; tone
`--brand/--accent/--success/--warning/--danger/--info/--neutral`; emphasis
`--solid/--soft/--outline/--ghost`; disposition
`--vertical/--horizontal/--inline/--compact/--spacious/--center/--between/--end`; shape
`--square/--rounded/--pill`; elevation `--flat/--raised`; state
`.is-active/.is-disabled/.is-loading/.is-done/.is-error/.is-empty/.is-selected`.

## Workflow for any page

1. **Resolve** the version (Step 0) and read `LLM.md`; query `components.json` for the family
   you need (`objetos[<familia>].markup.markup` is the real markup, extracted from its demo).
2. **Start from a canonical file**, don't invent: `bloques/recetas/` (per page type),
   `bloques/ejemplos/` (complete pages: landing, login, dashboard, chat, forms),
   `bloques/combos/` (skeletons per archetype). Delete what you don't use.
3. **Write the HTML** with census objects only. If something is missing, it does not exist:
   either use another object or add it to the repo — never invent a class or write local CSS.
4. **Validate** with the sibling skill `aurora-validate` (auditor + measurement). `0 fallos` in
   the auditor and a measured mobile check, or it is not done.
5. **Deliver** with the exact footer.

If you are generating many pages of the same shape, write a block renderer (one function per
block, variants as data) instead of copying markup by hand — hand copies drift from the system
the moment a pack changes.

## Pitfalls that cost real time

- **Invented classes.** `nz-card`, `nz-text--xs`, `nz-text--2xs`, `nz-fieldset__legend`
  (real: `__leyenda`), `nz-alert__text`, `nz-row` for action groups (use `nz-cluster`).
  If it is not in `components.json`, it does not exist.
- **`.nz-switch` without `__track` + `__thumb`** leaves the `<input>` inert: the user cannot
  toggle it and reports "it won't let me".
- **`min-height` on a container whose child uses `height:100%`**: the percentage does not
  resolve and the child collapses to 2 px. Give the container a *definite* height.
- **`.nz-callout` for long text or quotes**: it is a short notice. Long prose goes in
  `.nz-prose`, the attribution in `.nz-lbl`.
- **Emojis as status icons** (✅ ⚠ ❔): shape changes with the font and the auditor flags them.
  Use the sprite.
- **`.nz-hero-bleed--brand` with prose inside**: text families set their own colour, so dark
  grey lands on brand blue. Brand heroes carry headlines only.
- **Horizontal overflow**: `document.scrollingElement.scrollWidth === clientWidth` must hold at
  320/360/390. If it does not, that is a delivery failure, not a detail.
- **Fixing mobile with `max-width`, `overflow-x` on body or `display:none` on columns**: hides
  the data. Use the system's stacking objects.
- **Verifying by classes in the DOM instead of computed styles**: the `nz-*` classes show up
  even when the CDN 404s and no CSS loaded. Check `getComputedStyle` and `document.styleSheets`.
- **Copying the whole CSS into the prompt** (~340 KB). Read the docs, link the packs.
- **A tag that exists only locally** gives a 404 on the CDN and a naked page. Push the tag.

## Siblings

- `aurora-pages` — archetypes, layout, typography, mobile.
- `aurora-validate` — the auditor and browser measurement.
- `aurora-generative` — let a model compose Aurora at runtime (openui-lang).

Repo entry points: `LLM.md`, `components.json`, `base.html` (searchable design database),
`datos/base-diseno.json`, `bloques/`, `paginas/` (live demo per object), `iconos/`, `CONTRATO.md`.
