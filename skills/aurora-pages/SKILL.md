---
name: aurora-pages
description: "Use when choosing the shape of an Aurora page: archetypes, layout, desktop canvas, mobile stacking and typographic scale."
version: 1.0.0
license: MIT
tags: [design-system, css, layout, responsive, aurora]
---

# Aurora — page shapes

Read `aurora` first (version resolution and hard rules). This skill decides **what the page is
made of**; the census decides the exact class names.

## Start from the canonical file, never from zero

| You are building | Copy from (repo, `@master`) |
|---|---|
| Landing / marketing | `bloques/ejemplos/landing.html` |
| Login / access | `bloques/ejemplos/login.html` |
| Dashboard / panel | `bloques/ejemplos/dashboard.html` |
| Chat with an AI | `bloques/ejemplos/chat-ia.html` |
| Forms | `bloques/ejemplos/forms.html` |
| Admin, settings, list+detail | `bloques/recetas/` (one canonical page per type) |
| A skeleton by archetype | `bloques/combos/<arquetipo>.html` (8 of them) |

Copy, delete what you don't use, keep the object vocabulary. A page rebuilt "in the spirit of"
Aurora is how drift starts.

## Layout decisions

- **Tool** (panel, board, table, map, editor) → `<main class="nz-container nz-container--app">`.
  No max width: a 1920 px monitor must be at least 95% covered.
- **Prose or marketing** → `.nz-container` (72 → 84 rem ≥1200 → 96 rem ≥1440). Let the system
  size it; don't hand-write a max-width.
- **Panel grid** → `.nz-dash-grid` (up to 6 columns in the 1440 band).
- **Many small cards** (icons, thumbnails) → `.nz-grid-auto` (`--compact` 160 px,
  `--spacious` 320 px): auto-fit with `min(100%, N)`, no media queries.
- **Side gutters** → `--nz-gutter` (16 → 24 → 32 px, automatic).
- **Conversational tool** → `.nz-chat` **with a definite height** plus `.nz-prompt` inside
  `.nz-chat__foot`. `min-height` alone loses: the thread grows and pushes the composer off
  screen, which is the single most reported "broken" chat layout.

## Typography

- Body → `.nz-prose`; labels and notes → `.nz-lbl`; standfirst → `.nz-lead`.
- The `nz-text` family exists **only with a modifier** (`--muted`, `--small`, `--large`,
  `--peso-*`). `nz-text` alone, `nz-text--2xs` and `nz-text--xs` do not exist.
- Minimums: 13 px for interface text, 12 px only for data. Weight: 400 body, 500 support,
  600 interface, 700 headlines and figures only.
- Headlines are capped on purpose (3xl 34 px, 4xl 50 px). A 56 px h1 on a 27" screen is not
  hierarchy, it is disproportion.
- **Don't leave `nz-h1--brand` on by default**: ink headline + one brand moment (primary
  button) + one accent moment (the data) reads better and respects the colour budget.

## Mobile: solved by the system, don't reinvent it

| Classic break | Object |
|---|---|
| Table that must fit whole | `.nz-table-wrap--apilable` > `.nz-table--apilable` with `data-etiqueta="Column"` per `<td>`. **Both classes**: the wrapper removes its own overflow on mobile on purpose |
| Genuinely wide table (Gantt) | `.nz-table-wrap` (own scroll). Never a wide table without a wrapper |
| Tabs getting cut | `.nz-tabs` wraps onto several lines; single line on purpose is `.nz-tabs--scroll` |
| Navbar actions unreachable | `.nz-navbar` and `.nz-navbar__links` wrap |
| A grid child overflowing | `.nz-dash-grid`, `.nz-split`, `.nz-thirds`, `.nz-bento`, `.nz-grid-12`, `.nz-holy`, `.nz-article` already carry `min-width: 0` on their children |

Rule of thumb: **intrinsic width → scroll; tabular data → stackable.**

Two mobile facts that are measured, not admired:

1. The primary action must be visible **without scrolling, also on mobile**. A big headline +
   standfirst + notice eats 200 px and drops the composer below the fold. If it does not fit,
   raise the tool with `order` in the flex container (never reordering the DOM) and shrink the
   hero only under 640 px.
2. `.nz-segmented` with 3+ options inside a narrow panel (20 rem inspector) needs `flex-wrap:
   wrap`, or the last option is clipped.

## Desktop specifics

- Canvas grows, type does not.
- `.nz-cq` declares a container context for composite objects living in a sidebar; charts,
  kanban and chat already query their container.
- Never declare `container-type` on `.nz-table-wrap`: the sticky `thead` needs its own scroll
  container.

## Design method before writing HTML

1. **Brief** — 3–5 lines: who uses the page and in what situation, the task they must complete
   in 30 seconds, what must be preserved (brand, facts, behaviour).
2. **Critique** — without touching code: is the data that matters in accent? does the page guide
   the task? Output: 3 strengths to keep + priorities.
3. **Harden before polishing** — long text (60+ chars) without breaking, empty state with an
   action, error that doesn't lose what was typed, double submit (`.is-loading`), mismatched
   magnitudes, long lists (paginate, don't overflow). Measure, don't admire.
4. **Polish** — only once direction and failure states are solved.

## Eloquence is a budget, not a taste

Measured on real pages: the noise users call "big boxes stepping on each other" is not in the
packs — it is surface and shadow budget. Canonical recipes stay around 33–37 surfaces with 4
nested; hand-built shells reached 104 surfaces, 17 nested and 67 shadows. So: **one elevated
element per region**, base boxes = flat + hairline, nested surfaces max 2 levels.
