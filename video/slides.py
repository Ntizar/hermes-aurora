#!/usr/bin/env python3
"""Build the seven demo slides (1600×900) for the hackathon video."""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent / "slides"
OUT.mkdir(exist_ok=True)

HEAD = """<!DOCTYPE html>
<html lang="en" data-nz-theme="light" data-nz-marca="monocromo">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/tokens.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/marcas/monocromo.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p1-layout.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p2-navigation.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p3-typography.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p4-actions.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p6-feedback.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p8-data.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p9-media.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p12-system.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Aurora@v10/packs/p16-cristal.css">
<style>
  html, body {{ height: 100%; }}
  body {{ display: grid; place-items: center; overflow: hidden; }}
  .slide {{ width: 1600px; height: 900px; padding: var(--nz-space-9); box-sizing: border-box;
            display: flex; flex-direction: column; justify-content: center; gap: var(--nz-space-6); }}
  .slide--app {{ padding: var(--nz-space-7); }}
  .mono {{ font-family: ui-monospace, "SFMono-Regular", Menlo, monospace; }}
  pre {{ margin: 0; }}
  .shot {{ width: 100%; height: 600px; object-fit: cover; object-position: top left; }}
  .slide pre, .slide code {{ font-size: 30px; line-height: 1.45; }}
  .slide .nz-code--block {{ padding: var(--nz-space-6); }}
  .slide .nz-h1 {{ font-size: 54px; }}
  .slide .nz-h3 {{ font-size: 40px; }}
  .slide .nz-lead {{ font-size: 30px; }}
  .slide .nz-prose {{ font-size: 26px; }}
</style>
</head>
<body class="nz">
"""

FOOT = """
</body>
</html>
"""

slides: dict[str, tuple[str, str]] = {}

slides["01-titulo"] = ("Aurora × Hermes", """
<div class="slide">
  <span class="nz-eyebrow">Hermes Agent · plugin hackathon 2026</span>
  <h1 class="nz-display nz-display--xl">Aurora × Hermes</h1>
  <p class="nz-lead nz-lead--lg">A design system the agent cannot fake: it looks up the census, then proves the page.</p>
  <div class="nz-cluster">
    <span class="nz-badge">2 tools</span>
    <span class="nz-badge">4 skills</span>
    <span class="nz-badge nz-badge--accent">0 network</span>
  </div>
</div>
""")

slides["02-problema"] = ("The problem", """
<div class="slide">
  <span class="nz-eyebrow">The problem</span>
  <h2 class="nz-h1">What an agent writes without a design system</h2>
  <div class="nz-stack">
    <div class="nz-callout nz-callout--danger"><p class="mono">.nz-card--glass&nbsp;&nbsp;&nbsp;← invented class, never existed</p></div>
    <div class="nz-callout nz-callout--danger"><p class="mono">background: linear-gradient(...)&nbsp;&nbsp;← nobody asked</p></div>
    <div class="nz-callout nz-callout--danger"><p class="mono">!important&nbsp;&nbsp;← to win a fight it started</p></div>
  </div>
  <p class="nz-prose nz-text--muted">Looks fine in the screenshot. Falls apart on a phone.</p>
</div>
""")

slides["03-buscar"] = ("aurora_buscar", """
<div class="slide slide--app">
  <span class="nz-eyebrow">Tool 1 · aurora_buscar</span>
  <h2 class="nz-h3">Ask the census, get the real markup</h2>
  <div class="nz-article">
    <pre class="nz-code nz-code--block"><code>› aurora_buscar("table that stacks on mobile")

{
  "familia": "nz-table",
  "pack":    "packs/p8-data.css",
  "clases":  ["nz-table", "nz-table--apilable", "nz-table--striped", ...],
  "markup":  "<div class=\\"nz-table-wrap nz-table-wrap--apilable\\">…"
}</code></pre>
  </div>
  <p class="nz-prose nz-text--muted">1.448 objects, offline, in-process. The model stops inventing.</p>
</div>
""")

slides["04-pagina"] = ("Built from the census", """
<div class="slide slide--app">
  <span class="nz-eyebrow">The page</span>
  <h2 class="nz-h3">Built from objects that exist</h2>
  <img class="nz-img nz-img--bordered nz-img--rounded shot" src="../../docs/screenshots/landing.png" alt="Landing page built with Aurora">
</div>
""")

slides["05-validar"] = ("aurora_validar", """
<div class="slide slide--app">
  <span class="nz-eyebrow">Tool 2 · aurora_validar</span>
  <h2 class="nz-h3">Prove it before saying done</h2>
  <div class="nz-article">
    <pre class="nz-code nz-code--block"><code>› aurora_validar(ruta="page.html")

ok: false
 - clase(s) inventada(s): nz-card--glass
 - gradiente en CSS propio
 - !important en CSS propio
 - 3 color(es) a mano
 - emoji en la interfaz
 - falta el pie de atribución</code></pre>
  </div>
  <p class="nz-prose nz-text--muted">Census-backed, offline, milliseconds. The same check anyone can rerun.</p>
</div>
""")

slides["06-limpio"] = ("Clean", """
<div class="slide slide--app">
  <span class="nz-eyebrow">After two iterations</span>
  <h2 class="nz-h3">Clean report, page delivered</h2>
  <div class="nz-callout nz-callout--success">
    <p class="mono">ok: true · 0 fallos · 47 classes · 25 families · 8 packs linked</p>
  </div>
  <img class="nz-img nz-img--bordered nz-img--rounded shot" src="../../docs/screenshots/dashboard.png" alt="Dashboard built with Aurora">
</div>
""")

slides["07-cierre"] = ("Install", """
<div class="slide">
  <span class="nz-eyebrow">Get it</span>
  <h2 class="nz-h1">Four skills. Two tools. Zero network.</h2>
  <div class="nz-article">
    <pre class="nz-code nz-code--block"><code>hermes plugins install aurora-design-system</code></pre>
  </div>
  <p class="nz-prose">github.com/Ntizar/hermes-aurora&nbsp;&nbsp;·&nbsp;&nbsp;ntizar.github.io/hermes-aurora</p>
  <p class="nz-prose nz-text--muted">Bring your own design system: the census is a build artefact.</p>
</div>
""")

for name, (title, body) in slides.items():
    (OUT / f"{name}.html").write_text(HEAD.format(title=title) + body + FOOT, encoding="utf-8")
    print("slide", name)
