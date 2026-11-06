#!/usr/bin/env python3
"""Slides v6 — COLOR (una marca de Aurora por tramo) y CERO parpadeo.

Reglas de determinismo (las tres fuentes del parpadeo v5, corregidas):
  1. Ningún @keyframes ni <script> en las escenas: el rasterizador-v7 calcula por
     fotograma la opacidad (data-d), el push (class pz), el ken-burns (data-ken),
     el tecleo (data-tipea) y el blur del claim (data-claim). Un solo dueño del style.
  2. CSS 100% local (slides/aurora-css, con Inter self-hosted): nada de CDN que
     cargue tarde y parpadee entre fotogramas.
  3. El estado BASE del HTML es el FINAL (todo visible, texto completo): si el
     rasterizador falla, la escena se lee entera; nunca opacity:0 dependiente de JS.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "slides"
IMG = "img"   # capturas a color (capturar-colores.py)

PACKS = ["tokens.css"]  # la marca se añade por escena

def css_links(marca):
    ficheros = (["tokens.css", f"marcas/{marca}.css"] +
                [f"packs/p{k}.css" for k in
                 ["1-layout", "3-typography", "4-actions", "6-feedback", "8-data"]])
    return "".join(f'<link rel="stylesheet" href="aurora-css/{f}">\n' for f in ficheros)

TINT_DARK = {"ntizar": "#060a1c", "indigo": "#0a0920", "aurora": "#071021",
             "carmesi": "#1c0708", "violeta": "#100a1f", "esmeralda": "#04150e"}
TINT_LIGHT = {"ntizar": "#f2f7ff", "indigo": "#f2f3ff", "aurora": "#f3f7ff",
              "carmesi": "#fff4f3", "violeta": "#f7f4ff", "esmeralda": "#eefbf4"}

def head(titulo, tema, marca):
    fondo = TINT_DARK[marca] if tema == "dark" else TINT_LIGHT[marca]
    return f"""<!DOCTYPE html>
<html lang="en" data-nz-theme="{tema}" data-nz-marca="{marca}">
<head>
<meta charset="utf-8">
<title>{titulo}</title>
{css_links(marca)}<style>
  html, body {{ height: 100%; }}
  body {{ display: grid; place-items: center; overflow: hidden; margin: 0; }}
  /* body.nz (0,1,1) y posterior: gana a la regla `.nz, body {{ background: --nz-gray-0 }}`
     de tokens.css — si no, el tinte de marca del slide no se aplica nunca */
  body.nz {{ background: {fondo}; }}
  .slide {{ width: 1600px; height: 900px; padding: 80px 110px 140px; box-sizing: border-box;
            display: flex; flex-direction: column; justify-content: center; gap: 40px; position: relative; }}
  .beat {{ font-size: 96px; font-weight: 800; letter-spacing: -0.03em; line-height: 1.04;
           color: var(--nz-text, #fff); max-width: 1300px; margin: 0; }}
  .beat .dim {{ color: var(--nz-text-mute); }}
  .beat .mk {{ color: var(--nz-marca-500); }}
  .beat .ac {{ color: var(--nz-acento-500); }}
  .sub {{ font-size: 40px; font-weight: 500; color: var(--nz-text-soft); margin: 0; }}
  .eyebrow {{ color: var(--nz-marca-500); font-size: 21px; letter-spacing: .22em; text-transform: uppercase; font-weight: 600; }}
  .foot {{ position: absolute; bottom: 52px; left: 110px; right: 110px; display: flex;
           justify-content: space-between; color: var(--nz-text-mute); font-size: 21px; }}
  .term {{ border-radius: 14px; overflow: hidden; border: 1px solid var(--nz-border, rgba(128,128,128,.35));
           box-shadow: 0 24px 80px rgba(0,0,0,.35); max-width: 1200px; }}
  .term__bar {{ display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: #161d2e; }}
  .term__bar i {{ width: 12px; height: 12px; border-radius: 50%; background: var(--nz-marca-400); }}
  .term__bar i:nth-child(2) {{ background: var(--nz-acento-400); }}
  .term__bar i:nth-child(3) {{ background: #3a4560; }}
  .term__bar span {{ margin-left: 8px; color: #8a96b5; font-size: 15px; font-family: ui-monospace, Menlo, monospace; }}
  .term__body {{ padding: 40px 46px; background: #0c111e; color: #e8ecf5;
                 font-size: 26px; line-height: 1.6; font-family: ui-monospace, Menlo, monospace; }}
  .term__body pre {{ margin: 0; font-family: inherit; }}
  .prompt {{ color: var(--nz-acento-400); font-weight: 700; }}
  .cursor {{ display: inline-block; width: 14px; height: 1.05em; background: var(--nz-acento-400); vertical-align: text-bottom; }}
  .k {{ color: #9db8ff; }} .s {{ color: #bfe3c0; }}
  .bad {{ color: #ff9d87; }} .ok7 {{ color: #8fe3a6; }}
  .trio {{ display: flex; gap: 26px; }}
  .trio .shot-wrap {{ flex: 1; }}
  .shot-wrap {{ border-radius: 16px; overflow: hidden; position: relative;
                 border: 2px solid var(--nz-marca-400); box-shadow: 0 30px 90px rgba(0,0,0,.35); }}
  .shot {{ width: 100%; height: 500px; object-fit: cover; object-position: top left; display: block; }}
  .trio .shot {{ height: 440px; }}
  .half {{ display: flex; gap: 28px; align-items: stretch; }}
  .half .shot-wrap {{ flex: 1; }}
  .half .shot {{ height: 480px; }}
  .lbl-bajo {{ position: absolute; top: 10px; left: 14px; font-size: 16px; letter-spacing: .12em;
               text-transform: uppercase; font-weight: 700; color: #fff; background: var(--nz-marca-600);
               padding: 4px 12px; border-radius: 999px; z-index: 3; }}
</style>
</head>
<body class="nz">
"""

FOOT = "</body>\n</html>\n"
slides = {}

# ── 01 · beat de apertura — marca ntizar (azul eléctrico), fondo tinta oscura de marca
slides["01-beat1"] = ("dark", "ntizar", """
<div class="slide">
  <h1 class="beat pz" data-d="0">Every agent can<br>build a <span class="mk">page.</span></h1>
  <div class="foot" data-d="1.6"><span>Aurora</span><span>Hermes Agent</span></div>
</div>
""")

# ── 02 · beat de tensión — marca indigo (índigo + cian)
slides["02-beat2"] = ("dark", "indigo", """
<div class="slide">
  <h1 class="beat pz" data-d="0">Almost none<br><span class="dim">can prove it's</span> <span class="ac">real.</span></h1>
  <div class="foot" data-d="1.5"><span>Aurora</span><span>Hermes Agent</span></div>
</div>
""")

# ── 03 · el nombre — ntizar en claro, titular en color de marca
slides["03-nombre"] = ("light", "ntizar", """
<div class="slide">
  <h1 class="beat pz" data-d="0" style="font-size:170px; color:var(--nz-marca-600)">AURORA.</h1>
  <p class="sub" data-d="1.0">A design system your agent <span style="color:var(--nz-acento-500); font-weight:700">can't fake.</span></p>
</div>
""")

# ── 04 · aurora_search — marca aurora (azul #2563eb + naranja), claro
slides["04-buscar"] = ("light", "aurora", """
<div class="slide">
  <span class="eyebrow" data-d="0.1">tool 1 · aurora_search</span>
  <div class="term" data-d="0.35">
    <div class="term__bar"><i></i><i></i><i></i><span>census — 2,223 objects</span></div>
    <div class="term__body"><pre><code><span class="prompt">›</span> <span data-tipea="aurora_search(&quot;table that stacks on mobile&quot;)" data-d="0.9" data-v="38">aurora_search("table that stacks on mobile")</span><span class="cursor"></span>
<span data-d="3.3">{
  <span class="k">"family"</span>:  <span class="s">"nz-table"</span>,
  <span class="k">"pack"</span>:    <span class="s">"packs/p8-data.css"</span>,
  <span class="k">"classes"</span>: [<span class="s">"nz-table"</span>, <span class="s">"nz-table--apilable"</span>, …],
  <span class="k">"markup"</span>:  <span class="s">"&lt;div class=\\"nz-table-wrap\\"&gt;…"</span>
}</span></code></pre></div>
  </div>
  <p class="sub" data-d="6.3" style="font-size:34px; font-weight:700; color:var(--nz-marca-600)">Real objects. Real markup. Every class.</p>
</div>
""")

# ── 05 · tríptico de producto CADA UNO EN SU MARCA — el disparo de color del vídeo
slides["05-trio"] = ("light", "aurora", """
<div class="slide">
  <span class="eyebrow" data-d="0.1">one system · four brands · every product</span>
  <div class="trio">
    <div class="shot-wrap" data-d="0.35" data-ken="1.05" style="border-color:#0057ff"><span class="lbl-bajo" style="background:#0057ff">ntizar</span><img class="shot" src="{IMG}/landing.png" alt="Landing — marca ntizar"></div>
    <div class="shot-wrap" data-d="0.7" data-ken="1.05" style="border-color:#00875e"><span class="lbl-bajo" style="background:#00875e">esmeralda</span><img class="shot" src="{IMG}/dashboard-esm.png" alt="Dashboard — marca esmeralda"></div>
    <div class="shot-wrap" data-d="1.05" data-ken="1.05" style="border-color:#7c3aed"><span class="lbl-bajo" style="background:#7c3aed">violeta</span><img class="shot" src="{IMG}/login.png" alt="Login — marca violeta" style="object-position:center top"></div>
  </div>
</div>
""")

# ── 06 · aurora_validate — marca carmesí (rojo + cian): el auditor en rojo
slides["06-validar"] = ("dark", "carmesi", """
<div class="slide">
  <span class="eyebrow" data-d="0.1">tool 2 · aurora_validate</span>
  <div class="term" data-d="0.35">
    <div class="term__bar"><i></i><i></i><i></i><span>report — page.html</span></div>
    <div class="term__body"><pre><code><span class="prompt">›</span> <span data-tipea="aurora_validate(path=&quot;page.html&quot;)" data-d="0.9" data-v="38">aurora_validate(path="page.html")</span><span class="cursor"></span>
<span data-d="3.0"><span class="bad">✗ FAILED — 4 violations</span>
 <span class="bad">−</span> unknown class: nz-card--glass     <span class="dim" style="font-size:20px">not in the census</span>
 <span class="bad">−</span> gradient in page CSS            <span class="dim" style="font-size:20px">banned by contract</span>
 <span class="bad">−</span> 3 hand-written colors           <span class="dim" style="font-size:20px">use --nz-* tokens</span>
 <span class="bad">−</span> missing attribution footer</span></code></pre></div>
  </div>
  <p class="sub" data-d="5.6" style="font-size:32px; color:#ff9d87; font-weight:700">Caught in milliseconds. Every time.</p>
</div>
""")

# ── 07 · limpio — esmeralda: el verde del ok:true
slides["07-limpio"] = ("light", "esmeralda", """
<div class="slide">
  <span class="eyebrow" data-d="0.1">the agent fixes it · two iterations later</span>
  <div class="term" data-d="0.4">
    <div class="term__bar"><i></i><i></i><i></i><span>report — page.html</span></div>
    <div class="term__body" style="font-size:32px"><pre><code><span class="prompt">›</span> aurora_validate(path="page.html")
<span class="ok7" style="color:var(--nz-marca-600)">✓ PASSED — ok: true · 0 failures · 8 packs linked</span></code></pre></div>
  </div>
  <div class="shot-wrap" data-d="1.0" data-ken="1.06" style="max-width:1100px"><span class="lbl-bajo" style="background:var(--nz-marca-600)">audited</span><img class="shot" src="{IMG}/dashboard-esm.png" alt="Dashboard validado" style="height:360px"></div>
</div>
""")

# ── 08 · light/dark — marca aurora en los dos paneles (mismo markup, un atributo)
slides["08-dark"] = ("dark", "aurora", """
<div class="slide">
  <span class="eyebrow" data-d="0.1">same markup · one attribute</span>
  <h1 class="beat pz" data-d="0" style="font-size:70px">Light and dark,<br><span class="mk">both designed.</span></h1>
  <div class="half">
    <div class="shot-wrap" data-d="0.65" data-ken="1.04"><span class="lbl-bajo" style="background:#2563eb">data-nz-theme="light"</span><img class="shot" src="{IMG}/dashboard.png" alt="Dashboard light — marca aurora"></div>
    <div class="shot-wrap" data-d="0.95" data-ken="1.04"><span class="lbl-bajo" style="background:#f97316">data-nz-theme="dark"</span><img class="shot" src="{IMG}/dashboard-dark.png" alt="Dashboard dark — marca aurora"></div>
  </div>
</div>
""")

# ── 09 · instalar — violeta
slides["09-instalar"] = ("dark", "violeta", """
<div class="slide">
  <h1 class="beat pz" data-d="0" style="font-size:82px">Aurora <span class="dim">for</span> <span class="mk">Hermes.</span></h1>
  <div class="term" data-d="0.6" style="max-width:1100px">
    <div class="term__bar"><i></i><i></i><i></i><span>terminal</span></div>
    <div class="term__body"><pre><code><span class="prompt">$</span> <span data-tipea="hermes plugins install aurora-design-system" data-d="1.2" data-v="40">hermes plugins install aurora-design-system</span><span class="cursor"></span>
<span class="ok7" data-d="3.4">✓ installed · 2 tools · 4 skills · 0 network</span></code></pre></div>
  </div>
  <p data-d="4.4" style="color:var(--nz-text-mute); font-size:26px; margin:0">github.com/Ntizar/hermes-aurora</p>
</div>
""")

# ── 10 · cierre multicolor — las marcas del sistema en una sola línea
slides["10-cierre"] = ("dark", "ntizar", """
<div class="slide" style="align-items:flex-start">
  <h1 class="beat pz" data-d="0.4" style="font-size:96px; max-width:1400px">
    <span style="color:#3a7aff">A</span><span style="color:#6261ff">U</span><span style="color:#417eff">R</span><span style="color:#2f9e74">O</span><span style="color:#ff8c4e">R</span><span style="color:#a78bfa">A</span> <span class="dim">for</span> <span style="color:#fff">Hermes.</span>
  </h1>
  <div class="term" data-d="1.7" style="max-width:1000px">
    <div class="term__bar"><i></i><i></i><i></i><span>one command</span></div>
    <div class="term__body" style="font-size:28px"><pre><code><span class="prompt">$</span> hermes plugins install aurora-design-system</code></pre></div>
  </div>
  <p data-d="3.1" style="color:var(--nz-text-soft); font-size:26px; margin:0">github.com/Ntizar/hermes-aurora · ntizar.github.io/hermes-aurora</p>
  <p data-d="4.2" style="position:absolute; bottom:48px; left:110px; color:var(--nz-text-mute); font-size:22px; margin:0">Hecho con ❤️ por David Antizar</p>
</div>
""")

for nombre, (tema, marca, cuerpo) in slides.items():
    cuerpo = cuerpo.replace("{IMG}", IMG)
    (OUT / f"{nombre}.html").write_text(head(nombre, tema, marca) + cuerpo + FOOT, encoding="utf-8")
    print("slide", nombre, tema, marca)
print("ok", len(slides))
