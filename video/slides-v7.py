#!/usr/bin/env python3
"""Slides v7 — PORTAL DE CRISTAL: liquid glass de verdad (refracción feDisplacementMap).

Doctrina (skill nivel-premio / references/liquid-glass-web.md):
  · Refracción por CLON: el fondo (cortinas + retícula) se clona dentro de cada portal con
    translate(-x,-y) y filter:url(#lg). No usamos backdrop-filter:url() porque se ignora en
    silencio según motor; el clon refringe SIEMPRE y es determinista. Sonda medida: dentro
    de la lente no queda NI UNA frontera de color nítida (blur puro: 3; lente: 0).
  · Cristal solo para el CHROME; el dato va delante nítido o sobre chip oscuro.
  · Especular inset 0 1px 0 .8, edge lightening, sombra amplia, box-reflect en héroes.
  · Cortinas pintadas en TODOS los canvas .cielo (el del fondo + cada clon del vidrio),
    con la MISMA función cerrada de t → el clon refringe las cortinas vivas, no un negro.
  · Materialización: la salida aparece dos veces — fantasma (filter:url(#lg2), fade-OUT
    data-out) sobre el texto nítido (fade-IN data-d): el dato atraviesa el vidrio.

Sin @keyframes ni setTimeout: rasterizar-v8 es el único dueño del tiempo (cero parpadeo).
"""
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent / "slides"

MARCAS = {  # rampas oficiales Aurora v10.10.0
    "ntizar":    ["#0057ff", "#3a7aff", "#ff6a00"],
    "indigo":    ["#4f46e5", "#06b6d4", "#6261ff"],
    "aurora":    ["#2563eb", "#f97316", "#417eff"],
    "esmeralda": ["#00875e", "#f59e0b", "#2f9e74"],
    "carmesi":   ["#dc2626", "#0891b2", "#f6453d"],
    "violeta":   ["#7c3aed", "#ec4899", "#905dff"],
}

GRANO = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'"
         "%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'"
         " stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)"
         "' opacity='0.5'/%3E%3C/svg%3E\")")

FILTRO = """<svg width="0" height="0" style="position:absolute"><defs>
  <filter id="lg" x="-14%" y="-14%" width="128%" height="128%">
    <feTurbulence type="fractalNoise" baseFrequency="0.007 0.011" numOctaves="1" seed="7" result="n"/>
    <feGaussianBlur in="SourceGraphic" stdDeviation="1.2" result="b"/>
    <feDisplacementMap in="b" in2="n" scale="24" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="lg2" x="-14%" y="-14%" width="128%" height="128%">
    <feTurbulence type="fractalNoise" baseFrequency="0.006 0.009" numOctaves="1" seed="11" result="n"/>
    <feGaussianBlur in="SourceGraphic" stdDeviation="1.6" result="b"/>
    <feDisplacementMap in="b" in2="n" scale="38" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</defs></svg>
"""

CIELO = ("<canvas class='cielo' width='1600' height='900'></canvas>"
         "<div class='reticula'></div><div class='luz'></div>")

def portal(x, y, w, h, interior="", ref=False, cls=""):
    vidrio = (f'<div class="vidrio"><div class="clon" style="transform:translate(-{x}px,-{y}px)">'
              + CIELO + '</div></div><div class="tinte"></div><div class="grano"></div>')
    sombra = 'portal ref' if ref else 'portal'
    return (f'<div class="{sombra}" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px; {cls}">'
            + vidrio + interior + '</div>')

BASE_CSS = """
  @font-face { font-family:"Inter var"; font-weight:400 700; font-display:block;
    src:url("aurora-css/fuentes/inter-var-latin.woff2") format("woff2-variations"); }
  html, body { height: 100%; margin: 0; overflow: hidden; }
  body { background: #04050c; }
  .marco { position: relative; width: 1600px; height: 900px; overflow: hidden; }
  .cielo { position: absolute; inset: 0; }
  .clon { position: absolute; width: 1600px; height: 900px; }
  .reticula { position: absolute; inset: 0; background:
      repeating-linear-gradient(0deg, rgba(255,255,255,.05) 0 1px, transparent 1px 160px),
      repeating-linear-gradient(90deg, rgba(255,255,255,.05) 0 1px, transparent 1px 160px); }
  .luz { position: absolute; inset: 0; background: radial-gradient(60% 50% at 50% 42%,
      rgba(255,255,255,.10), transparent 70%); }
  .vineta { position: absolute; inset: 0; background: radial-gradient(120% 100% at 50% 50%,
      transparent 58%, rgba(0,0,0,.5) 100%); }
  .portal { position: absolute; border-radius: 34px; overflow: hidden;
      border: 1px solid rgba(255,255,255,.22);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.80), inset 0 -1px 0 rgba(255,255,255,.14),
                  inset 0 0 44px rgba(255,255,255,.05), 0 40px 90px -26px rgba(0,0,0,.95); }
  .portal.ref { -webkit-box-reflect: below 14px linear-gradient(transparent 62%, rgba(255,255,255,.12)); }
  .vidrio { position: absolute; inset: 0; filter: url(#lg); }
  .tinte { position: absolute; inset: 0; background: linear-gradient(150deg,
      rgba(255,255,255,.16), rgba(255,255,255,.045) 48%, rgba(255,255,255,.12)); pointer-events: none; }
  .grano { position: absolute; inset: 0; background-image: __GRANO__; opacity: .05;
      mix-blend-mode: overlay; pointer-events: none; }
  .chip { position: absolute; inset: 18px; border-radius: 24px; background: rgba(7,10,20,.72);
      border: 1px solid rgba(255,255,255,.10); }
  .txt { position: absolute; font-family: "Inter var", -apple-system, Arial, sans-serif; }
  .beat { font-weight: 800; letter-spacing: -0.03em; line-height: 1.04; color: #fff; margin: 0; }
  .dim { color: rgba(255,255,255,.42); }
  .mono { font-family: ui-monospace, Menlo, monospace; }
  .lbl { letter-spacing: .22em; text-transform: uppercase; font-weight: 600; font-size: 21px; }
  .fantasma { filter: url(#lg2); }
"""

JS_CIELO = """
// Cortinas de aurora en TODOS los canvas .cielo (fondo + clones de los vidrios):
// posición = función cerrada de t (determinista). Cada clon pinta lo MISMO: la lente
// refringe el cielo vivo, no un negro.
const COLES = __SKY__;
function mulberry(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const rnd = mulberry(__SEED__);
const C = [];
for (let i = 0; i < 9; i++) {
  C.push({ x: 90 + rnd()*1420, a: 0.12 + rnd()*0.18, f: 0.20 + rnd()*0.35,
           ph: rnd()*6.283, am: 30 + rnd()*70, col: COLES[i % COLES.length], w: 70 + rnd()*140 });
}
function cielo(g, t) {
  g.fillStyle = __BG__; g.fillRect(0, 0, 1600, 900);
  for (const c of C) {
    const x = c.x + Math.sin(t * c.f + c.ph) * c.am;
    const grad = g.createLinearGradient(0, 0, 0, 900);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(0.45, c.col);
    grad.addColorStop(1, 'rgba(0,0,0,0)');
    g.globalAlpha = c.a * (0.75 + 0.25 * Math.sin(t * 0.5 + c.ph));
    g.strokeStyle = grad; g.lineWidth = c.w; g.lineCap = 'round';
    g.beginPath(); g.moveTo(x, -30);
    g.bezierCurveTo(x + 120 * Math.sin(t * 0.3 + c.ph), 300,
                    x - 120 * Math.cos(t * 0.22 + c.ph), 600, x + 60, 930);
    g.stroke();
  }
  g.globalAlpha = 1;
}
const t0 = (typeof window.__t === 'number') ? window.__t : 2.0;
document.querySelectorAll('canvas.cielo').forEach(cv => cielo(cv.getContext('2d'), t0));
"""

def escena(titulo, marca, seed, cuerpo, bg="'#04050c'"):
    js = JS_CIELO.replace("__SKY__", json.dumps(MARCAS[marca])).replace("__SEED__", str(seed)).replace("__BG__", bg)
    return (f'<!DOCTYPE html>\n<html lang="en" data-nz-marca="{marca}"><head><meta charset="utf-8">'
            f'<title>{titulo}</title>\n<style>{BASE_CSS.replace("__GRANO__", GRANO)}</style>{FILTRO}</head>\n'
            f'<body><div class="marco">\n{CIELO}<div class="vineta"></div>\n{cuerpo}\n</div>'
            f'<script>{js}</script></body></html>\n')

slides = {}

# 00 · PORTAL HÉROE: cortinas tras el vidrio gigante (reflejo debajo), AURORA nítido delante
slides["00-three"] = ("ntizar", 7,
    portal(140, 170, 1320, 520, "", ref=True, cls="z-index:2") + """
<h1 class="beat" data-claim="0.8,1.5" style="position:absolute; inset:0; display:grid; place-items:center;
    font-size:170px; z-index:6; margin:0">
  <span style="white-space:nowrap"><span style="color:#3a7aff">A</span><span style="color:#6261ff">U</span><span style="color:#417eff">R</span><span style="color:#2f9e74">O</span><span style="color:#ff8c4e">R</span><span style="color:#a78bfa">A</span></span></h1>
<div class="txt lbl" data-d="2.6" style="top:560px; width:100%; text-align:center; color:rgba(255,255,255,.55); z-index:6">design system · through the glass</div>
""")

# 01 · beat — el titular delante, cortinas y cristal de fondo
slides["01-beat1"] = ("ntizar", 13, """
<h1 class="beat pz" style="position:absolute; left:110px; top:330px; font-size:96px; z-index:6; max-width:1300px; margin:0">
  Every agent can<br>build a <span style="color:#6599ff">page.</span></h1>
<div class="txt lbl" data-d="1.6" style="bottom:64px; left:110px; color:rgba(255,255,255,.5); z-index:6">Aurora · Hermes Agent</div>
""")

# 02 · beat tensión — indigo
slides["02-beat2"] = ("indigo", 19, """
<h1 class="beat pz" style="position:absolute; left:110px; top:320px; font-size:96px; z-index:6; max-width:1350px; margin:0">
  Almost none<br><span class="dim">can prove it's</span> <span style="color:#2fc6e4">real.</span></h1>
<div class="txt lbl" data-d="1.5" style="bottom:64px; left:110px; color:rgba(255,255,255,.5); z-index:6">Aurora · Hermes Agent</div>
""")

# 03 · el nombre en la vitrina: portal con reflejo y el nombre sobre él
slides["03-nombre"] = ("ntizar", 23,
    portal(200, 250, 1200, 420, "", ref=True, cls="z-index:2") + """
<div class="txt" style="top:180px; width:100%; text-align:center; z-index:6">
  <div class="beat" style="font-size:140px; margin:0"><span style="color:#3a7aff">AURORA</span><span style="color:#ff6a00">.</span></div></div>
<p class="txt" data-d="1.2" style="top:340px; width:100%; text-align:center; font-size:36px; color:#fff; z-index:7; margin:0">
  A design system your agent <b style="color:#ff8a53">can't fake.</b></p>
""")

# 04 · aurora_search — terminal tras el vidrio; la salida se MATERIALIZA (fantasma→nítido)
SALIDA4 = """<div style="margin-top:20px">
  {<br>
  &nbsp;&nbsp;<span style="color:#9db8ff">"family"</span>:&nbsp; <span style="color:#bfe3c0">"nz-table"</span>,<br>
  &nbsp;&nbsp;<span style="color:#9db8ff">"pack"</span>:&nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#bfe3c0">"packs/p8-data.css"</span>,<br>
  &nbsp;&nbsp;<span style="color:#9db8ff">"classes"</span>: [<span style="color:#bfe3c0">"nz-table"</span>, <span style="color:#bfe3c0">"nz-table--apilable"</span>, …],<br>
  &nbsp;&nbsp;<span style="color:#9db8ff">"markup"</span>:&nbsp; <span style="color:#bfe3c0">"&lt;div class=\\\"nz-table-wrap\\\"&gt;…"</span><br>}</div>"""

slides["04-buscar"] = ("aurora", 29,
    '<div class="txt lbl" data-d="0.1" style="left:110px; top:96px; z-index:6; color:#6b9dff">tool 1 · aurora_search</div>'
    + portal(250, 150, 1100, 560, f"""
<div class="chip"></div>
<div class="txt mono" style="left:64px; top:64px; z-index:4; font-size:25px; color:#e8ecf5; line-height:1.55">
  <span style="color:#ff8c4e; font-weight:700">›</span> <span data-tipea="aurora_search(&quot;table that stacks on mobile&quot;)" data-d="0.9">aurora_search("table that stacks on mobile")</span><span style="display:inline-block;width:13px;height:1em;background:#ff8c4e;vertical-align:text-bottom"></span>
  <div class="fantasma" data-d="2.8" data-out="4.5,1.2" style="position:absolute; left:0; top:64px; width:98%; z-index:6">{SALIDA4}</div>
  <div data-d="3.4" style="position:relative; z-index:4">{SALIDA4}</div>
</div>""")
    + '<p class="txt" data-d="6.6" style="top:742px; width:100%; text-align:center; font-size:32px; font-weight:700; color:#a0c0ff; z-index:6; margin:0">Real objects. Real markup. Every class.</p>')

# 05 · tríptico en tres vitrinas con captura nítida Delante del vidrio (chrome de cristal)
def vitrina(x, img, etiqueta, color):
    interior = (f'<img src="img/{img}" style="position:absolute; left:16px; top:50px; width:378px; height:398px;'
                f' object-fit:cover; object-position:top left; border-radius:16px; z-index:4">'
                f'<div class="txt" style="top:18px; left:18px; z-index:5; font-size:15px; font-weight:700; letter-spacing:.12em;'
                f' color:#fff; background:{color}; padding:5px 13px; border-radius:999px">{etiqueta}</div>')
    return portal(x, 240, 410, 480, interior)

slides["05-trio"] = ("aurora", 31,
    '<div class="txt lbl" data-d="0.1" style="left:110px; top:92px; z-index:6; color:#9db8ff">one system · any brand · every product</div>'
    + vitrina(110, "landing.png", "ntizar", "#0057ff")
    + vitrina(585, "dashboard-esm.png", "esmeralda", "#00875e")
    + vitrina(1060, "login.png", "violeta", "#7c3aed"))

# 06 · validate — el fracaso rojo se materializa
SALIDA6 = """<div style="margin-top:18px">
  <span style="color:#ff7468; font-weight:700">✗ FAILED — 4 violations</span><br>
  <span style="color:#ff7468">−</span> unknown class: nz-card--glass&nbsp;&nbsp;<span style="font-size:19px;color:rgba(255,255,255,.42)">not in the census</span><br>
  <span style="color:#ff7468">−</span> gradient in page CSS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="font-size:19px;color:rgba(255,255,255,.42)">banned by contract</span><br>
  <span style="color:#ff7468">−</span> 3 hand-written colors&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="font-size:19px;color:rgba(255,255,255,.42)">use --nz-* tokens</span><br>
  <span style="color:#ff7468">−</span> missing attribution footer</div>"""

slides["06-validar"] = ("carmesi", 37,
    '<div class="txt lbl" data-d="0.1" style="left:110px; top:96px; z-index:6; color:#ff7468">tool 2 · aurora_validate</div>'
    + portal(250, 150, 1100, 560, f"""
<div class="chip"></div>
<div class="txt mono" style="left:64px; top:58px; z-index:4; font-size:24px; color:#e8ecf5; line-height:1.6">
  <span style="color:#32a7c8; font-weight:700">›</span> <span data-tipea="aurora_validate(path=&quot;page.html&quot;)" data-d="0.9">aurora_validate(path="page.html")</span><span style="display:inline-block;width:13px;height:1em;background:#32a7c8;vertical-align:text-bottom"></span>
  <div class="fantasma" data-d="2.6" data-out="4.2,1.2" style="position:absolute; left:0; top:58px; width:98%; z-index:6">{SALIDA6}</div>
  <div data-d="3.1" style="position:relative; z-index:4">{SALIDA6}</div>
</div>""")
    + '<p class="txt" data-d="5.9" style="top:748px; width:100%; text-align:center; font-size:30px; font-weight:700; color:#ffaba0; z-index:6; margin:0">Caught in milliseconds. Every time.</p>')

# 07 · limpio — vitrina esmeralda: ok + dashboard, reflejo
slides["07-limpio"] = ("esmeralda", 41,
    '<div class="txt lbl" data-d="0.1" style="left:110px; top:96px; z-index:6; color:#5fb58f">the agent fixes it · two iterations later</div>'
    + portal(230, 170, 1140, 500, f"""
<div class="chip"></div>
<div class="txt mono" style="left:44px; top:38px; z-index:5; font-size:25px; color:#95d0b4; font-weight:700">✓ PASSED — ok: true · 0 failures · 8 packs linked</div>
<img src="img/dashboard-esm.png" style="position:absolute; left:28px; top:92px; width:1084px; height:360px;
  object-fit:cover; object-position:top left; border-radius:16px; z-index:5; filter:saturate(1.06)">""", ref=True))

# 08 · light/dark — dos portales, mismo markup, un atributo
def cristal_tema(x, img, etiqueta, color):
    interior = (f'<img src="img/{img}" style="position:absolute; left:14px; top:50px; width:644px; height:400px;'
                f' object-fit:cover; object-position:top left; border-radius:16px; z-index:5">'
                f'<div class="txt mono" style="top:16px; left:16px; z-index:6; font-size:15px;'
                f' color:#fff; background:{color}; padding:5px 14px; border-radius:999px">{etiqueta}</div>')
    return portal(x, 350, 672, 470, interior)

slides["08-dark"] = ("aurora", 43,
    '<div class="txt lbl" data-d="0.1" style="left:110px; top:76px; z-index:6; color:#6b9dff">same markup · one attribute</div>'
    + '<h1 class="beat pz" style="position:absolute; left:110px; top:118px; font-size:64px; z-index:6; margin:0">Light and dark,<br><span style="color:#417eff">both designed.</span></h1>'
    + cristal_tema(144, "dashboard.png", 'theme="light"', "#2563eb")
    + cristal_tema(812, "dashboard-dark.png", 'theme="dark"', "#f97316"))

# 09 · instalar — consola violeta tras el vidrio
slides["09-instalar"] = ("violeta", 47,
    '<h1 class="beat pz" style="position:absolute; left:110px; top:110px; font-size:76px; z-index:6; margin:0">Aurora <span class="dim">for</span> <span style="color:#a485ff">Hermes.</span></h1>'
    + portal(230, 260, 1140, 420, """
<div class="chip"></div>
<div class="txt mono" style="left:60px; top:54px; z-index:5; font-size:27px; color:#ede9fe; line-height:1.7">
  <span style="color:#ff61ab; font-weight:700">$</span> <span data-tipea="hermes plugins install aurora-design-system" data-d="1.1">hermes plugins install aurora-design-system</span><span style="display:inline-block;width:14px;height:1em;background:#ff61ab;vertical-align:text-bottom"></span>
  <div class="ok7" data-d="3.5" style="margin-top:14px; color:#8fe3a6">✓ installed · 2 tools · 4 skills · 0 network</div>
</div>""")
    + '<p class="txt" data-d="4.6" style="top:716px; left:230px; z-index:6; color:rgba(255,255,255,.5); font-size:24px; margin:0">github.com/Ntizar/hermes-aurora</p>')

# 10 · cierre — píldora de cristal con el comando; titular multicolor nítido
slides["10-cierre"] = ("ntizar", 53,
    '<h1 class="beat pz" style="position:absolute; left:110px; top:170px; font-size:100px; z-index:6; margin:0">'
    '<span style="color:#3a7aff">A</span><span style="color:#6261ff">U</span><span style="color:#417eff">R</span><span style="color:#2f9e74">O</span><span style="color:#ff8c4e">R</span><span style="color:#a78bfa">A</span>'
    ' <span class="dim">for</span> <span style="color:#fff">Hermes.</span></h1>'
    + portal(230, 400, 1000, 92,
        '<div class="chip" style="inset:8px; border-radius:22px; background:rgba(10,14,28,.55)"></div>'
        '<div class="txt mono" style="left:40px; top:28px; z-index:5; font-size:25px; color:#e8ecf5">'
        '<span style="color:#ff6a00; font-weight:700">$</span> hermes plugins install aurora-design-system</div>',
        cls="border-radius:22px")
    + '<p class="txt" data-d="3.4" style="top:560px; left:110px; z-index:6; color:rgba(255,255,255,.55); font-size:24px; margin:0">github.com/Ntizar/hermes-aurora · ntizar.github.io/hermes-aurora</p>'
    + '<p class="txt" data-d="4.4" style="bottom:44px; left:110px; z-index:6; color:rgba(255,255,255,.4); font-size:21px; margin:0">Hecho con ❤️ por David Antizar</p>')

for nombre, (marca, seed, cuerpo) in slides.items():
    html = escena(nombre, marca, seed, cuerpo)
    (OUT / f"{nombre}.html").write_text(html, encoding="utf-8")
    print("slide v7", nombre, marca)
print("ok", len(slides))
