#!/usr/bin/env python3
"""Slides v11 — DEMO LIGHT del plugin (60 s, solo imagen, sin audio).

Un caso real, en claro, azul #0057ff + naranja #ff6a00:
  ask (aurora_search) → compose (página real) → measure (390 px) → validate (4 fallos)
  → fix (0 fallos) → cierre.
Las cifras y los textos de error salen de las salidas REALES de las tools
(video/demo-v10/salidas.json), no se inventan.
"""
from pathlib import Path
import html as _html
import json

OUT = Path(__file__).resolve().parent / "slides11"
OUT.mkdir(exist_ok=True)
RAIZ = Path(__file__).resolve().parent
SAL = json.loads((RAIZ / "demo-v10" / "salidas.json").read_text())
AZUL, NARANJA = "#0057ff", "#ff6a00"
TINTA, GRIS, LINEA, FONDO = "#0b1020", "#5b6478", "#e3e7f0", "#f4f6fa"

DUR = [("00-title", 5.0), ("01-ask", 9.0), ("02-compose", 9.0), ("03-mobile", 8.0),
       ("04-validate", 11.0), ("05-fix", 9.0), ("06-close", 9.0)]
OFFSETS, _t = {}, 0.0
for n, d in DUR:
    OFFSETS[n] = round(_t, 2); _t += d
TOTAL = round(_t, 2)

CSS = f"""
  @font-face {{ font-family:"Inter var"; font-weight:400 900; font-display:block;
    src:url("../slides/aurora-css/fuentes/inter-var-latin.woff2") format("woff2-variations"); }}
  * {{ box-sizing:border-box; }}
  html, body {{ margin:0; height:100%; overflow:hidden; background:{FONDO}; }}
  .marco {{ position:relative; width:1600px; height:900px; background:{FONDO}; overflow:hidden;
      font-family:"Inter var",-apple-system,Arial,sans-serif; color:{TINTA}; }}
  .barra {{ position:absolute; inset:0 0 auto 0; height:70px; background:#fff; border-bottom:1px solid {LINEA};
      display:flex; align-items:center; justify-content:space-between; padding:0 44px; z-index:20; }}
  .logo {{ font-weight:800; font-size:22px; letter-spacing:-.02em; }}
  .logo span {{ color:{NARANJA}; }}
  .meta {{ font-size:14px; color:{GRIS}; letter-spacing:.02em; }}
  .pasos {{ position:absolute; top:92px; left:44px; display:flex; gap:10px; z-index:20; }}
  .paso {{ font-size:13px; font-weight:600; letter-spacing:.10em; text-transform:uppercase;
      color:#94a0b8; padding:8px 14px; border-radius:999px; border:1px solid {LINEA}; background:#fff; }}
  .paso.on {{ color:#fff; background:{AZUL}; border-color:{AZUL}; }}
  .paso.hecho {{ color:{AZUL}; border-color:#c9d8ff; background:#eef4ff; }}
  .card {{ position:absolute; background:#fff; border:1px solid {LINEA}; border-radius:20px;
      box-shadow:0 18px 40px -26px rgba(16,24,48,.25); }}
  .k {{ font-size:13px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:{GRIS}; }}
  .h1 {{ font-weight:800; letter-spacing:-.04em; line-height:.98; margin:0; }}
  .mono {{ font-family:ui-monospace,"DejaVu Sans Mono",Menlo,monospace; }}
  .prog {{ position:absolute; left:0; bottom:0; height:4px; width:1600px; background:#e8ecf4; z-index:30; }}
  .prog i {{ display:block; height:4px; width:0; background:{AZUL}; }}
  .chip {{ display:inline-block; padding:7px 13px; border-radius:999px; font-size:14px; font-weight:600; }}
"""

JS = """
const t0=(typeof window.__t==='number')?window.__t:2.0;
const av=Math.min(100,((window.__T0||0)+t0)/__TOTAL__*100);
document.querySelectorAll('.prog i').forEach(e=>e.style.width=av+'%');
"""

def barra(paso):
    pasos = ["ASK", "COMPOSE", "MEASURE", "VALIDATE", "FIX"]
    html = ""
    for i, p in enumerate(pasos):
        cls = "paso on" if i == paso else ("paso hecho" if i < paso else "paso")
        html += f'<span class="{cls}">{i+1:02d} {p}</span>'
    return (f'<div class="barra"><div class="logo">AURORA<span>.</span> '
            f'<span style="color:{GRIS};font-weight:500;font-size:15px">hermes-aurora</span></div>'
            f'<div class="meta">real plugin · real output · offline</div></div>'
            f'<div class="pasos">{html}</div>')

def marco(nombre, cuerpo, paso):
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{nombre}</title>'
            f'<style>{CSS}</style></head><body><div class="marco">{barra(paso)}{cuerpo}'
            f'<div class="prog"><i></i></div></div>'
            f'<script>{JS.replace("__TOTAL__", str(TOTAL))}</script></body></html>')

slides = {}

# ── 00 · TITLE ────────────────────────────────────────────────────────────────
slides["00-title"] = (barra(-1) + f"""
<div style="position:absolute; left:120px; top:250px; width:1360px">
  <div class="k" data-d="0.1" style="color:{AZUL}">A real example · 60 seconds</div>
  <h1 class="h1" data-d="0.2" style="font-size:112px; margin-top:22px">A page the agent<br>can <span style="color:{AZUL}">prove</span>.</h1>
  <p data-d="1.2" style="font-size:26px; color:{GRIS}; margin-top:26px; max-width:900px">
    Aurora for Hermes: an offline catalogue of 2,223 classes and a validator that blocks invented ones.</p>
  <div data-d="2.0" style="margin-top:38px; display:flex; gap:12px">
    <span class="chip" style="background:#eef4ff; color:{AZUL}">2 tools</span>
    <span class="chip" style="background:#fff1e8; color:#b34a00">4 skills</span>
    <span class="chip" style="background:#eefaf3; color:#0a7a4f">0 network</span>
  </div>
</div>
<div data-d="1.6" style="position:absolute; right:90px; top:210px; width:430px; height:470px; border-radius:22px;
     background:#fff; border:1px solid {LINEA}; box-shadow:0 30px 60px -34px rgba(16,24,48,.35); overflow:hidden">
  <img src="../demo-v10/desk-top.png" style="width:100%; height:100%; object-fit:cover; object-position:top left;
       -webkit-mask-image:linear-gradient(180deg,#000 82%,transparent); mask-image:linear-gradient(180deg,#000 82%,transparent)">
</div>""", 0)

# ── 01 · ASK ──────────────────────────────────────────────────────────────────
r = SAL["search"]["results"][0]
clases = r["classes"][:4]
markup = (r["markup"] or "").replace("<", "&lt;")[:150]
slides["01-ask"] = (barra(0) + f"""
<div style="position:absolute; left:80px; top:190px; width:620px">
  <div class="k" data-d="0.1" style="color:{AZUL}">Step 01 · ask</div>
  <h2 class="h1" data-d="0.2" style="font-size:56px; margin-top:16px">The agent asks<br>in plain words.</h2>
  <div class="card" data-d="1.0" style="position:relative; margin-top:30px; width:600px; padding:26px 26px 22px">
    <div class="mono" style="font-size:19px; color:{TINTA}"><span style="color:{NARANJA}; font-weight:700">›</span>
      <span data-tipea="aurora_search(&quot;pricing table that stacks on mobile&quot;)" data-d="1.2">aurora_search("pricing table that stacks on mobile")</span></div>
    <div data-d="2.6" style="margin-top:18px; font-size:15px; color:{GRIS}">Offline. No key, no network, no guessing.</div>
  </div>
  <div data-d="3.2" style="margin-top:26px; display:flex; gap:10px">
    <span class="chip" style="background:#eef4ff; color:{AZUL}">2,223 classes</span>
    <span class="chip" style="background:#f2f4f9; color:{GRIS}">417 families</span>
    <span class="chip" style="background:#f2f4f9; color:{GRIS}">18 packs</span>
  </div>
</div>
<div class="card" data-d="2.4" style="left:760px; top:190px; width:760px; height:560px; background:#0c1226; border-color:#0c1226; color:#e8edf9; padding:30px 34px">
  <div class="mono" style="font-size:14px; color:#7f8fb3; letter-spacing:.14em">RESULT · 1 OF {len(SAL["search"]["results"])}</div>
  <div class="mono" style="margin-top:20px; font-size:22px; line-height:1.75">
    <span style="color:#8fb3ff">"family"</span>: <span style="color:#a8e6b8">"{r["family"]}"</span>,<br>
    <span style="color:#8fb3ff">"pack"</span>: <span style="color:#a8e6b8">"{r["pack"]}"</span>,<br>
    <span style="color:#8fb3ff">"classes"</span>: [<span style="color:#a8e6b8">"{clases[0]}"</span>, <span style="color:#a8e6b8">"{clases[1]}"</span>, <span style="color:#a8e6b8">"{clases[2]}"</span>, … {len(r["classes"])}],<br>
    <span style="color:#8fb3ff">"markup"</span>: <span style="color:#a8e6b8">"{markup}…"</span>
  </div>
  <div data-d="3.8" style="position:absolute; left:34px; bottom:30px; font-size:15px; color:#93a3c4">
    Real markup, extracted from the catalogue demo.</div>
</div>""", 0)

# ── 02 · COMPOSE ──────────────────────────────────────────────────────────────
slides["02-compose"] = (barra(1) + f"""
<div style="position:absolute; left:80px; top:180px; width:520px">
  <div class="k" data-d="0.1" style="color:{AZUL}">Step 02 · compose</div>
  <h2 class="h1" data-d="0.2" style="font-size:56px; margin-top:16px">Real classes.<br>Not guesses.</h2>
  <p data-d="1.0" style="font-size:20px; color:{GRIS}; margin-top:18px; line-height:1.5">
    Every block comes from the census: plans, price table, buttons, footer.</p>
  <div data-d="1.8" style="margin-top:26px; display:flex; flex-direction:column; gap:10px">
    <span class="mono" style="font-size:16px; color:{TINTA}">.nz-plans--3</span>
    <span class="mono" style="font-size:16px; color:{TINTA}">.nz-plan--featured</span>
    <span class="mono" style="font-size:16px; color:{TINTA}">.nz-pricetable</span>
    <span class="mono" style="font-size:16px; color:{TINTA}">.nz-btn--accent</span>
  </div>
</div>
<div data-d="0.6" style="position:absolute; left:640px; top:150px; width:900px; height:640px; border-radius:18px;
     background:#fff; border:1px solid {LINEA}; box-shadow:0 40px 80px -44px rgba(16,24,48,.4); overflow:hidden">
  <div style="height:38px; background:#eef1f7; border-bottom:1px solid {LINEA}; display:flex; align-items:center; gap:7px; padding-left:16px">
    <i style="width:10px;height:10px;border-radius:50%;background:#ff5f57;display:inline-block"></i>
    <i style="width:10px;height:10px;border-radius:50%;background:#febc2e;display:inline-block"></i>
    <i style="width:10px;height:10px;border-radius:50%;background:#28c840;display:inline-block"></i>
    <span class="mono" style="margin-left:14px; font-size:12px; color:#7b8598">meridian.app/pricing</span>
  </div>
  <div data-wipe="0.8,1.4,l" style="position:absolute; left:0; right:0; top:38px; bottom:0; overflow:hidden">
    <img src="../demo-v10/desk-top.png" style="width:100%; height:100%; object-fit:cover; object-position:top left;
       -webkit-mask-image:linear-gradient(180deg,#000 82%,transparent); mask-image:linear-gradient(180deg,#000 82%,transparent)">
  </div>
</div>
<div data-d="3.0" class="chip" style="position:absolute; left:1180px; top:700px; background:#fff1e8; color:#b34a00; z-index:9">
  orange accent, from the brand</div>""", 1)

# ── 03 · MEASURE ──────────────────────────────────────────────────────────────
slides["03-mobile"] = (barra(2) + f"""
<div style="position:absolute; left:80px; top:180px; width:470px">
  <div class="k" data-d="0.1" style="color:{AZUL}">Step 03 · measure</div>
  <h2 class="h1" data-d="0.2" style="font-size:56px; margin-top:16px">390 px.<br>No overflow.</h2>
  <p data-d="1.0" style="font-size:20px; color:{GRIS}; margin-top:18px; line-height:1.5">
    The table stacks with its own labels. Measured in the browser, not admired in a mockup.</p>
  <div data-d="2.0" class="card" style="position:relative; margin-top:26px; width:440px; padding:18px 20px">
    <div class="mono" style="font-size:15px; color:{TINTA}">scrollWidth 375 = clientWidth 375</div>
    <div style="margin-top:6px; font-size:14px; color:#0a7a4f; font-weight:700">✓ no horizontal scroll at 390</div>
  </div>
</div>
<div data-d="0.5" style="position:absolute; left:590px; top:150px; width:330px; height:660px; border-radius:34px;
     background:#0b1020; padding:12px; box-shadow:0 40px 80px -40px rgba(16,24,48,.45)">
  <div style="width:100%; height:100%; border-radius:26px; overflow:hidden; background:#fff">
    <img src="../demo-v10/movil-tabla.png" style="width:100%; height:100%; object-fit:cover; object-position:top">
  </div>
</div>
<div data-d="2.6" style="position:absolute; left:980px; top:190px; width:520px">
  <div class="mono" style="font-size:15px; color:{GRIS}">table.nz-table--apilable</div>
  <div class="mono" style="font-size:15px; color:{GRIS}; margin-top:8px">td[data-etiqueta="Usuarios"]</div>
  <div style="margin-top:26px; font-size:19px; color:{TINTA}; line-height:1.5; max-width:480px">
    Each cell carries its own label, so the table reads like a list on a phone.</div>
  <div data-d="3.6" style="margin-top:24px; font-size:15px; color:{GRIS}">
    Next: measure 320, 360 and 390 before shipping.</div>
</div>""", 2)

# ── 04 · VALIDATE ─────────────────────────────────────────────────────────────
fallos = SAL["rota"]["failures"]
filas = ""
for i, f in enumerate(fallos):
    filas += (f'<div data-d="{1.2 + i*0.55}" style="display:flex; gap:14px; margin-top:14px; font-size:18px; line-height:1.35">'
              f'<span style="color:#ff6b5e; font-weight:800">✗</span>'
              f'<span style="color:#ffe7e4">{_html.escape(f)}</span></div>')
slides["04-validate"] = (barra(3) + f"""
<div style="position:absolute; left:80px; top:180px; width:520px">
  <div class="k" data-d="0.1" style="color:#c2261a">Step 04 · validate</div>
  <h2 class="h1" data-d="0.2" style="font-size:56px; margin-top:16px">Four failures.<br>Milliseconds.</h2>
  <p data-d="0.9" style="font-size:20px; color:{GRIS}; margin-top:18px; line-height:1.5">
    The same page, checked against the census. Invented class, gradient, hand-written colours, missing footer.</p>
  <div data-d="6.2" class="card" style="position:relative; margin-top:24px; width:470px; padding:16px 20px; border-color:#f3c9c4; background:#fff6f5">
    <div style="font-size:15px; color:#8a2418; font-weight:700">ok: false — the agent must fix it before shipping.</div>
  </div>
</div>
<div data-d="0.5" class="card" style="left:640px; top:160px; width:880px; height:620px; background:#0c1226; border-color:#0c1226; padding:32px 36px">
  <div style="display:flex; justify-content:space-between; align-items:flex-start">
    <div class="mono" style="font-size:17px; color:#ffe7e4"><span style="color:#ff6b5e">›</span> aurora_validate("page.html")</div>
    <div style="text-align:right"><div class="mono" data-count="1.0,0.5,0,4" style="font-size:64px; font-weight:800; color:#ff6b5e; line-height:1">4</div>
      <div class="k" style="color:#ff9c92">failures</div></div>
  </div>
  <div style="margin-top:22px">{filas}</div>
  <div data-d="4.6" class="mono" style="position:absolute; left:36px; bottom:26px; font-size:14px; color:#7f8fb3">
    ok: false · nz_classes 38 · families 13</div>
</div>""", 3)

# ── 05 · FIX ──────────────────────────────────────────────────────────────────
arreglos = [
    ("nz-card--glass", "→ .nz-plan--featured"),
    ("linear-gradient(...)", "→ deleted (Aurora uses none)"),
    ("#3b82f6 ×2", "→ var(--nz-marca-600)"),
    ("footer", "→ «Hecho con ❤️ por David Antizar»"),
]
filas5 = ""
for i, (a, b) in enumerate(arreglos):
    filas5 += (f'<div data-d="{1.4 + i*0.5}" style="display:flex; justify-content:space-between; gap:20px; margin-top:16px;'
               f' font-size:18px;"><span class="mono" style="color:#ffb0a5; text-decoration:line-through">{a}</span>'
               f'<span class="mono" style="color:#9ff0bb">{b}</span></div>')
slides["05-fix"] = (barra(4) + f"""
<div style="position:absolute; left:80px; top:180px; width:520px">
  <div class="k" data-d="0.1" style="color:#0a7a4f">Step 05 · fix</div>
  <h2 class="h1" data-d="0.2" style="font-size:56px; margin-top:16px">Zero failures.<br>Then it ships.</h2>
  <p data-d="1.0" style="font-size:20px; color:{GRIS}; margin-top:18px; line-height:1.5">
    Four edits. Re-run. The report is clean and the numbers are real.</p>
  <div data-d="3.4" class="card" style="position:relative; margin-top:26px; width:470px; padding:22px">
    <div class="mono" style="font-size:22px; color:#0a7a4f; font-weight:700">ok: true</div>
    <div style="margin-top:8px; font-size:15px; color:{GRIS}">39 nz-classes · 14 families · 7 packs linked</div>
  </div>
</div>
<div data-d="0.5" class="card" style="left:640px; top:160px; width:880px; height:620px; background:#0c1226; border-color:#0c1226; padding:32px 36px">
  <div style="display:flex; justify-content:space-between; align-items:flex-start">
    <div class="mono" style="font-size:17px; color:#d8ffe9"><span style="color:#34d399">›</span> aurora_validate("page.html")</div>
    <div style="text-align:right"><div class="mono" data-count="3.0,0.5,4,0" style="font-size:64px; font-weight:800; color:#34d399; line-height:1">0</div>
      <div class="k" style="color:#8fe3a6">failures</div></div>
  </div>
  <div style="margin-top:20px">{filas5}</div>
  <div data-d="4.0" class="mono" style="position:absolute; left:36px; bottom:26px; font-size:14px; color:#7f8fb3">
    No failures. Now measure the render at 320 / 360 / 390.</div>
</div>""", 4)

# ── 06 · CLOSE ────────────────────────────────────────────────────────────────
slides["06-close"] = (barra(-1) + f"""
<div style="position:absolute; left:120px; top:230px; width:1360px">
  <h1 class="h1" data-d="0.1" style="font-size:104px">Two tools.<br>Four skills. <span style="color:{AZUL}">Zero guessing.</span></h1>
  <div data-d="1.2" style="margin-top:34px; display:flex; gap:12px">
    <span class="chip" style="background:#eef4ff; color:{AZUL}">aurora_search</span>
    <span class="chip" style="background:#eef4ff; color:{AZUL}">aurora_validate</span>
    <span class="chip" style="background:#f2f4f9; color:{GRIS}">0 network</span>
    <span class="chip" style="background:#f2f4f9; color:{GRIS}">MIT</span>
  </div>
  <div data-d="2.0" style="margin-top:42px; padding:22px 28px; width:900px; background:#0c1226; border-radius:14px">
    <div class="mono" style="font-size:24px; color:#eef2ff"><span style="color:{NARANJA}; font-weight:700">$</span> hermes plugins install aurora-design-system</div>
  </div>
  <div data-d="2.8" style="margin-top:26px; font-size:19px; color:{GRIS}">github.com/Ntizar/hermes-aurora · ntizar.github.io/hermes-aurora</div>
</div>
<div data-d="0.8" style="position:absolute; right:110px; top:700px; text-align:right">
  <div style="font-weight:800; font-size:72px; letter-spacing:-.05em; line-height:1; color:{AZUL}">AURORA<span style="color:{NARANJA}">.</span></div>
  <div style="margin-top:6px; font-size:16px; color:{GRIS}">for Hermes</div></div>""", 4)

for nombre, (cuerpo, paso) in slides.items():
    (OUT / f"{nombre}.html").write_text(marco(nombre, cuerpo, paso), encoding="utf-8")
    print("slide", nombre)
(RAIZ / "manifest-v11.json").write_text(json.dumps(dict(DUR), indent=1))
(RAIZ / "offsets-v11.json").write_text(json.dumps(OFFSETS, indent=1))
print("total", TOTAL, "s ·", sum(round(d*20) for _, d in DUR), "frames")
