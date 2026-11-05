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
  .slide {{ width: 1600px; height: 900px; padding: var(--nz-space-9) var(--nz-space-9) 200px; box-sizing: border-box;
            display: flex; flex-direction: column; justify-content: center; gap: var(--nz-space-6); }}
  .slide--app {{ padding: var(--nz-space-6) var(--nz-space-7) 200px; }}
  .mono {{ font-family: ui-monospace, "SFMono-Regular", Menlo, monospace; }}
  pre {{ margin: 0; }}
  .shot {{ width: 100%; height: 600px; object-fit: cover; object-position: top left; }}
  .slide pre, .slide code {{ font-size: 30px; line-height: 1.45; }}
  .slide .nz-code--block {{ padding: var(--nz-space-6); }}
  .slide .nz-h1 {{ font-size: 54px; }}
  .slide .nz-h3 {{ font-size: 40px; }}
  .slide .nz-lead {{ font-size: 30px; }}
  /* — animación (timeline en rasterizar.py: virtual-time-budget) — */
  .nz-fade   {{ animation: nzIn .5s var(--ease, ease-out) both; }}
  .nz-fade-2 {{ animation: nzIn .5s .35s ease-out both; }}
  .nz-fade-3 {{ animation: nzIn .5s .7s ease-out both; }}
  .nz-pop    {{ animation: nzPop .4s var(--d, 0s) ease-out both; }}
  @keyframes nzIn  {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes nzPop {{ from {{ opacity: 0; transform: scale(.7); }} 60% {{ transform: scale(1.06); }} to {{ opacity: 1; transform: none; }} }}
  .slide--anim .nz-reveal {{ opacity: 0; animation: nzIn .45s var(--d, 0s) ease-out both; }}
  .no-anim .slide--anim .nz-reveal, .no-anim .nz-fade, .no-anim .nz-fade-2, .no-anim .nz-fade-3, .no-anim .nz-pop {{ opacity: 1 !important; animation: none !important; }}
  /* — terminal con chrome — */
  .term {{ border-radius: 10px; overflow: hidden; border: 1px solid rgba(0,0,0,.14); box-shadow: 0 2px 14px rgba(0,0,0,.06); }}
  .term__bar {{ display: flex; align-items: center; gap: 8px; padding: 10px 14px; background: #10182b; }}
  .term__bar i {{ width: 11px; height: 11px; border-radius: 50%; background: #3a4a6b; }}
  .term__bar i:first-child {{ background: #d8d8d8; }}
  .term__bar span {{ margin-left: 8px; color: #8a96b5; font-size: 15px; font-family: ui-monospace, Menlo, monospace; }}
  .term__body {{ padding: var(--nz-space-6); background: #0d1526; color: #e8ecf5; }}
  .term__body .prompt {{ color: #f0c75e; font-weight: 700; }}
  .term__body .cursor {{ display: inline-block; width: 13px; height: 1.1em; background: #f0c75e; vertical-align: text-bottom; animation: nzBlink 1s steps(1) infinite; }}
  .term__body .k {{ color: #9db8ff; }}
  .term__body .s {{ color: #bfe3c0; }}
  .term__body .bad {{ color: #ff9d87; }}
  .term__body .ok7 {{ color: #bfe3c0; }}
  @keyframes nzBlink {{ 50% {{ opacity: 0; }} }}
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
<div class="slide slide--anim">
  <span class="nz-eyebrow nz-fade">Hermes Agent · plugin hackathon 2026</span>
  <h1 class="nz-display nz-display--xl nz-fade-2">Aurora × Hermes</h1>
  <p class="nz-lead nz-lead--lg nz-fade-3">A design system the agent cannot fake: it looks up the census, then proves the page.</p>
  <div class="nz-cluster">
    <span class="nz-badge nz-pop" style="--d:1.6s">2 tools</span>
    <span class="nz-badge nz-pop" style="--d:1.8s">4 skills</span>
    <span class="nz-badge nz-badge--accent nz-pop" style="--d:2.0s">0 network</span>
  </div>
</div>
""")

slides["02-problema"] = ("The problem", """
<div class="slide slide--anim">
  <span class="nz-eyebrow nz-fade">The problem</span>
  <h2 class="nz-h1 nz-fade-2">What an agent writes without a design system</h2>
  <div class="nz-stack">
    <div class="nz-callout nz-callout--danger nz-reveal" style="--d:.6s"><p class="mono">.nz-card--glass&nbsp;&nbsp;&nbsp;← invented class, never existed</p></div>
    <div class="nz-callout nz-callout--danger nz-reveal" style="--d:1.3s"><p class="mono">background: linear-gradient(...)&nbsp;&nbsp;← nobody asked</p></div>
    <div class="nz-callout nz-callout--danger nz-reveal" style="--d:2.0s"><p class="mono">!important&nbsp;&nbsp;← to win a fight it started</p></div>
  </div>
  <p class="nz-prose nz-text--muted nz-reveal" style="--d:2.8s">Looks fine in the screenshot. Falls apart on a phone.</p>
</div>
""")

slides["03-buscar"] = ("aurora_search", """
<div class="slide slide--app slide--anim">
  <span class="nz-eyebrow nz-fade">Tool 1 · aurora_search</span>
  <h2 class="nz-h3 nz-fade-2">Ask the census, get the real markup</h2>
  <div class="nz-article nz-reveal" style="--d:.2s">
    <div class="term">
      <div class="term__bar"><i></i><i></i><i></i><span>aurora_search — result</span></div>
      <pre class="term__body"><code><span class="prompt">›</span> <span id="cmd"></span><span class="cursor"></span>
<span class="resp nz-reveal" style="--d:3.4s">{
  <span class="k">"family"</span>:  <span class="s">"nz-table"</span>,
  <span class="k">"pack"</span>:    <span class="s">"packs/p8-data.css"</span>,
  <span class="k">"classes"</span>: [<span class="s">"nz-table"</span>, <span class="s">"nz-table--apilable"</span>, <span class="s">"nz-table--striped"</span>, …],
  <span class="k">"markup"</span>:  <span class="s">"&lt;div class=\\"nz-table-wrap nz-table-wrap--apilable\\"&gt;…"</span>
}</span></code></pre>
    </div>
  </div>
</div>
<script>
  const S = 'aurora_search("table that stacks on mobile")';
  const el = document.getElementById('cmd'); let i = 0;
  (function t(){ if (i < S.length) { el.textContent = S.slice(0, ++i); setTimeout(t, 52); } })();
</script>
""")

slides["04-pagina"] = ("Built from the census", """
<div class="slide slide--app">
  <span class="nz-eyebrow">The page</span>
  <h2 class="nz-h3">Built from objects that exist</h2>
  <img class="nz-img nz-img--bordered nz-img--rounded shot" src="../../docs/screenshots/landing.png" alt="Landing page built with Aurora">
</div>
""")

slides["05-validar"] = ("aurora_validate", """
<div class="slide slide--app slide--anim">
  <span class="nz-eyebrow nz-fade">Tool 2 · aurora_validate</span>
  <h2 class="nz-h3 nz-fade-2">Prove it before saying done</h2>
  <div class="nz-article nz-reveal" style="--d:.2s">
    <div class="term">
      <div class="term__bar"><i></i><i></i><i></i><span>aurora_validate — report</span></div>
      <pre class="term__body"><code><span class="prompt">›</span> <span id="cmd5"></span><span class="cursor"></span>
<span class="resp nz-reveal" style="--d:3.2s">ok: <span class="bad">false</span>
 <span class="bad">-</span> unknown class: nz-card--glass
 <span class="bad">-</span> gradient in page CSS
 <span class="bad">-</span> !important in page CSS
 <span class="bad">-</span> 3 hand-written colours
 <span class="bad">-</span> emoji in the UI
 <span class="bad">-</span> missing attribution footer</span></code></pre>
    </div>
  </div>
</div>
<script>
  const S5 = 'aurora_validate(path="page.html")';
  const el5 = document.getElementById('cmd5'); let j = 0;
  (function t(){ if (j < S5.length) { el5.textContent = S5.slice(0, ++j); setTimeout(t, 52); } })();
</script>
""")

slides["06-limpio"] = ("Clean", """
<div class="slide slide--app slide--anim">
  <span class="nz-eyebrow nz-fade">After two iterations</span>
  <h2 class="nz-h3 nz-fade-2">Clean report, page delivered</h2>
  <div class="nz-callout nz-callout--success nz-reveal" style="--d:.6s">
    <p class="mono">ok: true · 0 failures · 47 classes · 25 families · 8 packs linked</p>
  </div>
  <img class="nz-img nz-img--bordered nz-img--rounded shot nz-reveal" style="--d:1.4s" src="../../docs/screenshots/dashboard.png" alt="Dashboard built with Aurora">
</div>
""")

slides["07-cierre"] = ("Install", """
<div class="slide slide--anim">
  <span class="nz-eyebrow nz-fade">Get it</span>
  <h2 class="nz-h1 nz-fade-2">Four skills. Two tools. Zero network.</h2>
  <div class="nz-article nz-reveal" style="--d:.5s">
    <div class="term">
      <div class="term__bar"><i></i><i></i><i></i><span>terminal</span></div>
      <pre class="term__body"><code><span class="prompt">$</span> <span id="cmd7"></span><span class="cursor"></span>
<span class="ok7 nz-reveal" style="--d:2.6s">✓ installed · 2 tools, 4 skills registered</span></code></pre>
    </div>
  </div>
  <p class="nz-prose nz-reveal" style="--d:3.4s">github.com/Ntizar/hermes-aurora&nbsp;&nbsp;·&nbsp;&nbsp;ntizar.github.io/hermes-aurora</p>
</div>
<script>
  const S7 = 'hermes plugins install aurora-design-system';
  const el7 = document.getElementById('cmd7'); let k = 0;
  (function t(){ if (k < S7.length) { el7.textContent = S7.slice(0, ++k); setTimeout(t, 58); } })();
</script>
""")

for name, (title, body) in slides.items():
    (OUT / f"{name}.html").write_text(HEAD.format(title=title) + body + FOOT, encoding="utf-8")
    print("slide", name)
