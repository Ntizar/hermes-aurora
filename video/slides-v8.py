#!/usr/bin/env python3
"""Slides v8 — «THE RECIPE» (70 s). Portal de cristal + HUD de película.

Dirección (GUION-v8.md):
  · Asimetría editorial: titular enorme a la izquierda, panel de cristal a la derecha
    cortado por el borde. Nunca tres tarjetas iguales centradas.
  · Cristal por CLON con filter:url(#lg) (refringe siempre, determinista). El dato va
    nítido delante o sobre chip oscuro; el vidrio es chrome, no contenido.
  · HUD de film en todas las escenas: wordmark, acto N/10, etiqueta y barra de progreso.
  · Todo el movimiento lo calcula rasterizar-v9.py por fotograma. Sin @keyframes.
"""
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent / "slides"
RAIZ = Path(__file__).resolve().parent
MANIFEST = json.loads((RAIZ / "manifest-v8.json").read_text())
OFFSETS = json.loads((RAIZ / "offsets-v8.json").read_text())
TOTAL = 70.0

MARCAS = {
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
  <filter id="lg" x="-16%" y="-16%" width="132%" height="132%">
    <feTurbulence type="fractalNoise" baseFrequency="0.006 0.010" numOctaves="1" seed="7" result="n"/>
    <feGaussianBlur in="SourceGraphic" stdDeviation="1.1" result="b"/>
    <feDisplacementMap in="b" in2="n" scale="30" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="lg2" x="-16%" y="-16%" width="132%" height="132%">
    <feTurbulence type="fractalNoise" baseFrequency="0.005 0.008" numOctaves="1" seed="11" result="n"/>
    <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="b"/>
    <feDisplacementMap in="b" in2="n" scale="42" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</defs></svg>"""

CIELO = "<canvas class='cielo' width='1600' height='900'></canvas><div class='reticula'></div><div class='luz'></div>"

BASE_CSS = """
  @font-face { font-family:"Inter var"; font-weight:400 900; font-display:block;
    src:url("aurora-css/fuentes/inter-var-latin.woff2") format("woff2-variations"); }
  html, body { height:100%; margin:0; overflow:hidden; }
  body { background:#04050c; }
  .marco { position:relative; width:1600px; height:900px; overflow:hidden; background:#04050c; }
  .cielo { position:absolute; inset:0; }
  .clon { position:absolute; width:1600px; height:900px; }
  .reticula { position:absolute; inset:0; background:
      repeating-linear-gradient(0deg, rgba(255,255,255,.055) 0 1px, transparent 1px 160px),
      repeating-linear-gradient(90deg, rgba(255,255,255,.055) 0 1px, transparent 1px 160px); }
  .luz { position:absolute; inset:0; background:radial-gradient(58% 48% at 62% 40%,
      rgba(255,255,255,.10), transparent 72%); }
  .vineta { position:absolute; inset:0; background:radial-gradient(118% 98% at 50% 48%,
      transparent 54%, rgba(0,0,0,.62) 100%); }
  .portal { position:absolute; border-radius:30px; overflow:hidden;
      border:1px solid rgba(255,255,255,.20);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.75), inset 0 -1px 0 rgba(255,255,255,.12),
                  inset 0 0 48px rgba(255,255,255,.05), 0 44px 96px -30px rgba(0,0,0,.95); }
  .portal.ref { -webkit-box-reflect: below 12px linear-gradient(transparent 64%, rgba(255,255,255,.10)); }
  .vidrio { position:absolute; inset:0; filter:url(#lg); }
  .tinte { position:absolute; inset:0; pointer-events:none; background:linear-gradient(152deg,
      rgba(255,255,255,.15), rgba(255,255,255,.035) 46%, rgba(255,255,255,.11)); }
  .grano { position:absolute; inset:0; background-image:__GRANO__; opacity:.055;
      mix-blend-mode:overlay; pointer-events:none; }
  .chip { position:absolute; background:rgba(7,10,20,.55); border:1px solid rgba(255,255,255,.10);
      border-radius:20px; }
  .hud { position:absolute; z-index:30; font:600 13px/1 "Inter var",sans-serif;
      letter-spacing:.16em; text-transform:uppercase; color:rgba(255,255,255,.62); }
  .hud.low { letter-spacing:.10em; text-transform:none; font-weight:500; font-size:14px;
      color:rgba(255,255,255,.50); }
  .hud b { color:#fff; font-weight:800; }
  .hud .punto { display:inline-block; width:7px; height:7px; border-radius:50%;
      background:__BRAND__; margin-right:11px; box-shadow:0 0 12px __BRAND__; vertical-align:1px; }
  .prog { position:absolute; left:0; bottom:0; width:1600px; height:2px; z-index:30;
      background:rgba(255,255,255,.07); }
  .prog-fill { height:2px; width:0; background:linear-gradient(90deg,__BRAND__,rgba(255,255,255,.9));
      box-shadow:0 0 14px __BRAND__; }
  .esq { position:absolute; width:26px; height:26px; border-color:rgba(255,255,255,.18);
      border-style:solid; border-width:0; z-index:29; }
  .k { font:700 15px/1.3 "Inter var",sans-serif; letter-spacing:.22em; text-transform:uppercase; }
  .h1 { font-weight:800; letter-spacing:-.045em; line-height:.97; margin:0; color:#fff; }
  .mono { font-family:ui-monospace,"DejaVu Sans Mono",Menlo,monospace; }
  .dim { color:rgba(255,255,255,.54); }
  .sub { color:rgba(255,255,255,.68); font-weight:400; }
  .tag { display:inline-block; padding:6px 13px; border-radius:999px; font:700 14px/1.2 "Inter var",sans-serif;
      letter-spacing:.10em; text-transform:uppercase; }
  .sweep { position:absolute; top:-20%; bottom:-20%; width:220px; z-index:12; pointer-events:none;
      background:linear-gradient(105deg,transparent,rgba(255,255,255,.30),rgba(255,255,255,.05),transparent);
      filter:blur(2px); }
  .file { position:absolute; left:0; right:0; height:128px; border-top:1px solid rgba(255,255,255,.10); }
"""

JS_CIELO = """
const COLES = __SKY__;
function mulberry(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const rnd = mulberry(__SEED__);
const C = [];
for (let i = 0; i < 13; i++) {
  C.push({ x: 60 + rnd()*1500, a: 0.16 + rnd()*0.22, f: 0.16 + rnd()*0.30,
           ph: rnd()*6.283, am: 34 + rnd()*80, col: COLES[i % COLES.length],
           w: 90 + rnd()*180, core: rnd() < 0.35 });
}
function rgb(h){ const n = parseInt(h.slice(1), 16); return [n>>16 & 255, n>>8 & 255, n & 255]; }
function cielo(g, t) {
  g.fillStyle = '#04050c'; g.fillRect(0, 0, 1600, 900);
  g.globalCompositeOperation = 'lighter';
  const focos = [[1010, 400, 620, COLES[0], 0.20], [380, 720, 540, COLES[2], 0.15]];
  for (const f of focos) {
    const [r, gg, b] = rgb(f[3]);
    const rad = g.createRadialGradient(f[0], f[1], 0, f[0], f[1], f[2]);
    rad.addColorStop(0, 'rgba(' + r + ',' + gg + ',' + b + ',' + f[4] + ')');
    rad.addColorStop(1, 'rgba(' + r + ',' + gg + ',' + b + ',0)');
    g.fillStyle = rad; g.fillRect(0, 0, 1600, 900);
  }
  g.globalCompositeOperation = 'source-over';
  for (const c of C) {
    const x = c.x + Math.sin(t * c.f + c.ph) * c.am;
    const grad = g.createLinearGradient(0, 0, 0, 900);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(0.45, c.col);
    grad.addColorStop(1, 'rgba(0,0,0,0)');
    g.globalAlpha = c.a * (0.72 + 0.28 * Math.sin(t * 0.45 + c.ph));
    g.strokeStyle = grad; g.lineWidth = c.w; g.lineCap = 'round';
    g.beginPath(); g.moveTo(x, -30);
    g.bezierCurveTo(x + 130 * Math.sin(t * 0.28 + c.ph), 300,
                    x - 130 * Math.cos(t * 0.20 + c.ph), 600, x + 70, 930);
    g.stroke();
    if (c.core) { g.globalAlpha = Math.min(0.55, c.a * 2.2); g.lineWidth = 3.5;
      g.strokeStyle = 'rgba(255,255,255,.55)'; g.stroke(); }
  }
  g.globalAlpha = 1;
}
const t0 = (typeof window.__t === 'number') ? window.__t : 2.0;
document.querySelectorAll('canvas.cielo').forEach(cv => cielo(cv.getContext('2d'), t0));
const avance = Math.min(100, ((window.__T0 || 0) + t0) / __TOTAL__ * 100);
document.querySelectorAll('.prog-fill').forEach(el => el.style.width = avance + '%');
document.querySelectorAll('.strip-in').forEach(el => {
  el.style.transform = 'translateX(' + (-((t0 * 48) % 1180)) + 'px)';
});
"""

def portal(x, y, w, h, interior="", ref=False, cls="", radio=""):
    vidrio = (f'<div class="vidrio"><div class="clon" style="transform:translate(-{x}px,-{y}px)">'
              + CIELO + '</div></div><div class="tinte"></div><div class="grano"></div>')
    refc = " ref" if ref else ""
    return (f'<div class="portal{refc}" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px;'
            f' {radio} {cls}">' + vidrio + interior + '</div>')

def hud(n, etiqueta):
    return (f'<div class="hud" style="left:64px; top:50px"><span class="punto"></span>'
            f'AURORA <span class="dim" style="letter-spacing:.06em">/ hermes-aurora</span></div>'
            f'<div class="hud" style="right:64px; top:50px">ACT <b>{n}</b> <span class="dim">/ 10</span></div>'
            f'<div class="hud low" style="left:64px; bottom:46px">{etiqueta}</div>'
            '<div class="prog"><div class="prog-fill"></div></div>'
            '<div class="esq" style="left:30px; top:30px; border-left-width:1px; border-top-width:1px"></div>'
            '<div class="esq" style="right:30px; bottom:30px; border-right-width:1px; border-bottom-width:1px"></div>')

def escena(nombre, marca, seed, cuerpo, act, etiqueta):
    c1, c2, c3 = MARCAS[marca]
    css = (BASE_CSS.replace("__GRANO__", GRANO).replace("__BRAND__", c2))
    js = (JS_CIELO.replace("__SKY__", json.dumps(MARCAS[marca]))
          .replace("__SEED__", str(seed)).replace("__TOTAL__", str(TOTAL)))
    t0 = OFFSETS[nombre]
    return (f'<!DOCTYPE html>\n<html lang="en" data-nz-marca="{marca}"><head><meta charset="utf-8">'
            f'<title>{nombre}</title>\n<style>{css}</style>{FILTRO}</head>\n'
            f'<body data-t0="{t0}"><div class="marco">\n{CIELO}<div class="vineta"></div>\n'
            f'{hud(act, etiqueta) if act else ""}\n{cuerpo}\n</div>'
            f'<script>{js}</script></body></html>\n')

slides = {}

# ── 00 · COLD OPEN ─────────────────────────────────────────────────────────────
hojas = ""
X0, Y0, W0, H0 = 200, 180, 1200, 520
for i in range(6):
    x = X0 + i * 200.4
    dx = (-1 if i % 2 == 0 else 1) * (760 + i * 70)
    rot = (-7 if i % 2 == 0 else 7)
    hojas += (f'<div class="hoja" data-shard="0.08,{0.85 + i * 0.03},{dx},0,{rot}" '
              f'style="left:{x}px; top:{Y0}px; width:197px; height:{H0}px; position:absolute; '
              f'border-radius:5px; overflow:hidden; border:1px solid rgba(255,255,255,.30); '
              f'box-shadow:inset 1px 0 0 rgba(255,255,255,.22), 0 18px 50px rgba(0,0,0,.55); z-index:2">'
              f'<div class="vidrio"><div class="clon" style="transform:translate(-{x}px,-{Y0}px)">'
              f'{CIELO}</div></div><div class="tinte"></div></div>')

slides["00-open"] = ("ntizar", 7, "", "cold open",
"""<div class="hud" style="left:64px; top:50px"><span class="punto"></span>COLD OPEN</div>
""" + hojas + f"""
<div data-d="1.35,0.45" style="position:absolute; left:{X0}px; top:{Y0}px; width:{W0}px; height:{H0}px; border-radius:26px;
     border:1px solid rgba(255,255,255,.30); box-shadow:inset 0 1px 0 rgba(255,255,255,.7),
     0 40px 90px -28px rgba(0,0,0,.95); z-index:6; overflow:hidden; pointer-events:none">
  <img src="img/landing.png" data-d="2.15,1.1" data-ken="1.05"
       style="width:100%; height:100%; object-fit:cover; object-position:top left; filter:saturate(1.05)">
</div>
<div class="sweep" data-sweep="1.55,0.85" style="left:{X0 - 40}px; top:{Y0 - 40}px; height:{H0 + 80}px"></div>
<div class="chip" data-d="0.55,0.3" style="left:{X0 + 42}px; top:{Y0 + H0 - 86}px; height:56px; width:560px;
     border-radius:14px; background:rgba(4,6,14,.82); z-index:9"></div>
<div class="mono" style="position:absolute; left:{X0 + 64}px; top:{Y0 + H0 - 68}px; z-index:10; font-size:22px; color:#dfe6f5">
  <span style="color:#ff6a00; font-weight:700">›</span>
  <span data-tipea="build me a landing page" data-d="0.75">build me a landing page</span>
  <span style="display:inline-block;width:11px;height:1em;background:#ff6a00;vertical-align:text-bottom"></span>
</div>
<div class="hud" style="left:64px; bottom:46px">a film about proof</div>
<div class="prog"><div class="prog-fill"></div></div>""")

# ── 01 · LA PROMESA ────────────────────────────────────────────────────────────
slides["01-hook"] = ("ntizar", 13, "1", "the promise",
portal(880, 74, 780, 780, '<img src="img/landing.png" data-ken="1.06" style="position:absolute; inset:0;'
       ' width:100%; height:100%; object-fit:cover; object-position:top left">', cls="z-index:2") + """
<div class="k" data-d="0.05" style="position:absolute; left:110px; top:196px; color:#6b9dff">01 — the promise</div>
<h1 class="h1 pz" style="position:absolute; left:104px; top:246px; font-size:122px">Any page.<br>
  <span class="dim">In seconds.</span></h1>
<div class="sub" data-d="1.5" style="position:absolute; left:110px; top:520px; font-size:29px; line-height:1.45; max-width:660px">
  Beautiful. Fast. And completely improvised.</div>
<div class="mono" data-d="2.3" style="position:absolute; left:110px; top:626px; font-size:19px; color:rgba(255,255,255,.38)">
  one prompt · no designer · no rules</div>
""")

# ── 02 · EL HUECO ──────────────────────────────────────────────────────────────
ANOT = [
    (760, 150, 300, 54, "unknown class", "nz-card--glass", 1.1),
    (760, 300, 380, 54, "banned gradient", "linear-gradient(#fff0…)", 2.0),
    (760, 470, 320, 54, "hand-written colour", "#3b82f6", 2.9),
]
anot = ""
for (x, y, w, h, titulo, valor, d) in ANOT:
    anot += (f'<div data-d="{d}" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px;'
             f' border:1.5px solid rgba(255,92,80,.9); background:rgba(220,38,38,.12); border-radius:6px; z-index:8"></div>'
             f'<div data-d="{d}" class="mono" style="position:absolute; left:{x}px; top:{y - 36}px; font-size:16px;'
             f' color:#ffd9d4; letter-spacing:.02em; z-index:8; background:rgba(14,3,3,.85);'
             f' padding:5px 10px; border-left:2px solid #ff5d4f; border-radius:3px">{titulo} · {valor}</div>')

slides["02-hueco"] = ("carmesi", 19, "2", "the gap",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:150px; color:#ff7a6c">02 — the gap</div>'
'<h1 class="h1" data-d="0.1" style="position:absolute; left:104px; top:200px; font-size:104px">Nobody<br>checked it.</h1>'
'<div data-d="1.2" style="position:absolute; left:110px; top:420px; font-size:26px; color:rgba(255,255,255,.55); max-width:520px; line-height:1.5">'
'It looks right. That is not the same as being right.</div>'
+ portal(700, 110, 860, 680, '<img src="img/landing.png" data-ken="1.05" style="position:absolute; inset:0; width:100%;'
         ' height:100%; object-fit:cover; object-position:top left; filter:brightness(.52) saturate(.65)">'
         + anot
         + '<div class="mono" data-claim="3.9,0.5" style="position:absolute; right:44px; bottom:54px; z-index:9;'
           ' color:#ff5d4f; border:3px solid #ff5d4f; padding:12px 22px; font-size:38px; font-weight:700;'
           ' letter-spacing:.10em; transform:rotate(-7deg); background:rgba(10,2,2,.55)">UNVERIFIED</div>',
         cls="z-index:2"))

# ── 03 · EL CONTRATO ───────────────────────────────────────────────────────────
filas = [
    ("01", "CENSUS", "Every object, every class, the real markup.", "2,223 classes · 417 families", 1.15),
    ("02", "JUDGE", "Proves a page against it. Zero failures, or it ships nothing.", "4 checks · milliseconds", 2.35),
    ("03", "SKILLS", "Teach the agent the procedure, not the vibe.", "4 skills · 2 tools", 3.55),
]
doc = ""
for i, (n, t, d, m, dd) in enumerate(filas):
    top = 120 + i * 152
    doc += (f'<div data-d="{dd}" style="position:absolute; left:56px; right:56px; top:{top}px">'
            f'<div class="mono" style="float:left; width:56px; font-size:22px; color:#6b9dff">{n}</div>'
            f'<div style="margin-left:64px">'
            f'<div style="font:800 30px/1.1 \'Inter var\'; letter-spacing:-.02em; color:#fff">{t}</div>'
            f'<div style="margin-top:9px; font-size:19px; color:rgba(255,255,255,.55); line-height:1.35">{d}</div>'
            f'<div class="mono" style="margin-top:11px; font-size:15px; color:{MARCAS["aurora"][1]}">{m}</div>'
            f'</div></div>')
    if i < 2:
        doc += f'<div style="position:absolute; left:56px; right:56px; top:{top + 118}px; height:1px; background:rgba(255,255,255,.10)"></div>'

slides["03-contrato"] = ("aurora", 23, "3", "the contract",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:170px; color:#7fb0ff">03 — the contract</div>'
'<h1 class="h1 pz" style="position:absolute; left:104px; top:216px; font-size:100px">A contract,<br><span class="dim">not a prompt.</span></h1>'
'<div class="sub" data-d="1.0" style="position:absolute; left:110px; top:452px; font-size:25px; line-height:1.5; max-width:560px">'
'Three pieces. Any design system can ship them — that is the whole point.</div>'
+ portal(780, 130, 720, 640, '<div class="chip" style="inset:16px; border-radius:22px"></div>' + doc
         + '<div class="mono" data-d="4.4" style="position:absolute; left:56px; bottom:38px; font-size:15px; color:rgba(255,255,255,.35)">census.json · judge.py · SKILL.md</div>',
         cls="z-index:3"))

# ── 04 · EL CENSO ──────────────────────────────────────────────────────────────
SALIDA4 = """<div style="margin-top:18px">
  {<br>
  &nbsp;&nbsp;<span style="color:#8fb3ff">"familia"</span>:&nbsp;<span style="color:#a8e6b8">"nz-table"</span>,<br>
  &nbsp;&nbsp;<span style="color:#8fb3ff">"pack"</span>:&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#a8e6b8">"packs/p8-data.css"</span>,<br>
  &nbsp;&nbsp;<span style="color:#8fb3ff">"clases"</span>:&nbsp;&nbsp;[<span style="color:#a8e6b8">"nz-table"</span>, <span style="color:#a8e6b8">"nz-table--apilable"</span>, …],<br>
  &nbsp;&nbsp;<span style="color:#8fb3ff">"markup"</span>:&nbsp;<span style="color:#a8e6b8">"&lt;div class=\\'nz-table-wrap\\'&gt;…"</span><br>
}</div>"""

slides["04-censo"] = ("aurora", 29, "4", "the census",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:96px; color:#7fb0ff">04 — the census</div>'
'<div data-d="1.3" style="position:absolute; right:110px; top:82px; text-align:right">'
'  <span class="mono" data-count="1.3,1.5,0,2223" style="font-size:64px; font-weight:700; color:#fff">2,223</span>'
'  <div class="k" style="color:rgba(255,255,255,.40); margin-top:6px">classes · 417 families · 18 packs</div></div>'
+ portal(100, 190, 1400, 520, '<div class="chip" style="inset:14px; border-radius:20px"></div>'
         '<div class="txt mono" style="position:absolute; left:58px; top:48px; z-index:6; font-size:24px; color:#e9eefb; line-height:1.55">'
         '  <span style="color:#ff8c4e; font-weight:700">›</span> '
         '  <span data-tipea="aurora_search(&quot;table that stacks on mobile&quot;)" data-d="0.85">aurora_search("table that stacks on mobile")</span>'
         '  <span style="display:inline-block;width:12px;height:1em;background:#ff8c4e;vertical-align:text-bottom"></span>'
         '  <div class="fantasma" data-d="2.55" data-out="3.9,1.0" style="position:absolute; left:0; top:66px; width:97%; z-index:7">' + SALIDA4 + '</div>'
         '  <div data-d="3.2" style="position:relative; z-index:6">' + SALIDA4 + '</div>'
         '</div>'
         '<div data-d="5.4" class="tag" style="position:absolute; right:44px; bottom:38px; z-index:8;'
         ' background:rgba(37,99,235,.18); color:#a9c8ff; border:1px solid rgba(120,170,255,.35)">real markup, not memory</div>',
         cls="z-index:2")
+ '<div style="position:absolute; left:0; top:748px; width:1600px; overflow:hidden; height:34px; opacity:.42">'
'<div class="strip-in mono" style="white-space:nowrap; font-size:24px; color:#cfe0ff">'
'.nz-table &nbsp; .nz-card &nbsp; .nz-nav &nbsp; .nz-appshell &nbsp; .nz-chat &nbsp; .nz-kanban &nbsp; .nz-chart &nbsp; .nz-dash-grid &nbsp; .nz-split &nbsp; .nz-bento &nbsp; .nz-form &nbsp; .nz-modal &nbsp; .nz-table--apilable &nbsp; .nz-btn--solid &nbsp; .nz-field &nbsp; .nz-tabs &nbsp; .nz-toast &nbsp; .nz-badge &nbsp; .nz-avatar &nbsp; .nz-progress &nbsp;'
'</div></div>')

# ── 05 · UNA MARCA, CUALQUIER MARCA ────────────────────────────────────────────
def vitrina(x, y, w, h, img, marca, color, zoom="1.04"):
    return portal(x, y, w, h,
        f'<img src="img/{img}" data-ken="{zoom}" style="position:absolute; inset:0; width:100%; height:100%;'
        f' object-fit:cover; object-position:top left">'
        f'<div class="tag" style="position:absolute; left:16px; top:16px; z-index:8; background:{color}; color:#fff">{marca}</div>',
        cls="z-index:2")

slides["05-marcas"] = ("esmeralda", 31, "5", "one system · any brand",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:86px; color:#63c39a">05 — one system · any brand</div>'
'<h1 class="h1" data-d="0.1" style="position:absolute; left:104px; top:118px; font-size:54px">Four brands. Three products. Zero redesign.</h1>'
+ vitrina(90, 206, 700, 600, "landing.png", "ntizar", "#0057ff", "1.05")
+ vitrina(830, 206, 700, 288, "dashboard-esm.png", "esmeralda", "#00875e", "1.03")
+ vitrina(830, 518, 700, 288, "login.png", "violeta", "#7c3aed", "1.03"))

# ── 06 · EL JUEZ ───────────────────────────────────────────────────────────────
FALLOS = [
    ("unknown class", "nz-card--glass", "not in the census", 1.5),
    ("banned gradient", "linear-gradient(…)", "the contract forbids it", 2.15),
    ("hand-written colour", "#3b82f6 ×3", "use --nz-* tokens", 2.8),
    ("missing attribution", "footer", "required in every page", 3.45),
]
fallos = ""
for i, (titulo, token, nota, d) in enumerate(FALLOS):
    fallos += (f'<div data-d="{d}" style="position:absolute; left:56px; right:56px; top:{182 + i * 74}px; z-index:7">'
               f'<span class="mono" style="color:#ff6b5e; font-size:24px; font-weight:700">✗</span> '
               f'<span style="font-size:24px; color:#fff; font-weight:600">{titulo}</span>'
               f'<span class="mono" style="font-size:21px; color:#ff9c92; margin-left:16px">{token}</span>'
               f'<span class="mono" style="font-size:16px; color:rgba(255,255,255,.38); margin-left:16px">{nota}</span></div>')

slides["06-juez"] = ("carmesi", 37, "6", "the judge",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:100px; color:#ff7a6c">06 — the judge</div>'
+ portal(90, 152, 1420, 580, '<div class="chip" style="inset:14px; border-radius:20px"></div>'
         '<div class="mono" style="position:absolute; left:56px; top:52px; z-index:7; font-size:23px; color:#f2e9e8">'
         '  <span style="color:#ff6b5e; font-weight:700">›</span> '
         '  <span data-tipea="aurora_validate(&quot;page.html&quot;)" data-d="0.7">aurora_validate("page.html")</span>'
         '  <span style="display:inline-block;width:11px;height:1em;background:#ff6b5e;vertical-align:text-bottom"></span>'
         '</div>' + fallos
         + '<div data-d="4.2" class="mono" style="position:absolute; left:56px; bottom:44px; z-index:7; font-size:15px; color:rgba(255,255,255,.38)">'
           'scanned page.html · 1,204 lines · 2,223 known classes · 0 network</div>'
         + '<div data-claim="4.1,0.45" style="position:absolute; right:52px; top:34px; z-index:9; text-align:right">'
           '<div class="mono" style="font-size:86px; font-weight:700; color:#ff5d4f; line-height:1">4</div>'
           '<div class="k" style="color:#ff8b7f; margin-top:4px">violations</div></div>'
         + '<div class="mono" data-claim="4.9,0.4" style="position:absolute; right:44px; bottom:44px; z-index:9;'
           ' color:#ff5d4f; border:3px solid #ff5d4f; padding:10px 20px; font-size:34px; font-weight:700;'
           ' letter-spacing:.10em; transform:rotate(-5deg); background:rgba(12,2,2,.5)">BLOCKED</div>',
         cls="z-index:2 border-color:rgba(255,92,80,.35)")
+ '<div data-d="5.5" style="position:absolute; left:0; top:770px; width:100%; text-align:center; font-size:29px; font-weight:600; color:#fff">Caught in <span style="color:#ff6b5e; font-weight:800">milliseconds</span>. Before you ever see it.</div>')

# ── 07 · EL BUCLE ──────────────────────────────────────────────────────────────
RUNS = [
    ("run 2", "4 failures", "#ff6b5e", 1.0),
    ("run 3", "1 failure",  "#ffb36b", 2.15),
    ("run 4", "0 failures", "#8fe3a6", 3.3),
]
runs = ""
for i, (r, f, c, d) in enumerate(RUNS):
    runs += (f'<div data-d="{d}" class="mono" style="position:absolute; left:52px; top:{186 + i * 84}px; z-index:7; font-size:25px">'
             f'<span style="color:rgba(255,255,255,.45)">{r}</span>'
             f'<span style="color:rgba(255,255,255,.20); margin:0 18px">→</span>'
             f'<span style="color:{c}; font-weight:700">{f}</span></div>')

slides["07-bucle"] = ("esmeralda", 41, "7", "the loop",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:96px; color:#63c39a">07 — the loop</div>'
+ portal(90, 150, 820, 560, '<div class="chip" style="inset:14px; border-radius:20px"></div>'
         '<div class="mono" style="position:absolute; left:52px; top:48px; z-index:7; font-size:21px; color:#e6f5ec">'
         '  <span style="color:#34d399; font-weight:700">›</span> while failures &gt; 0: fix · re-run</div>' + runs
         + '<div data-claim="4.3,0.5" class="mono" style="position:absolute; left:52px; bottom:40px; z-index:8;'
           ' font-size:25px; color:#9ff0bb; font-weight:700">✓ PASSED — ok: true · 0 failures · 8 packs linked</div>',
         cls="z-index:2 border-color:rgba(52,211,153,.32)")
+ '<div data-claim="4.35,0.6" style="position:absolute; right:96px; top:150px; text-align:right; z-index:8">'
'  <div class="mono" data-count="4.35,0.5,4,0" style="font-size:300px; font-weight:700; line-height:.82; color:#34d399;'
'       text-shadow:0 0 80px rgba(52,211,153,.35)">0</div>'
'  <div class="k" style="color:#8fe3a6; margin-top:10px">failures left</div></div>'
+ portal(1000, 556, 510, 230, '<img src="img/dashboard-esm.png" style="position:absolute; inset:0; width:100%; height:100%;'
         ' object-fit:cover; object-position:top left">', cls="z-index:2"))

# ── 08 · UN ATRIBUTO ───────────────────────────────────────────────────────────
slides["08-tema"] = ("violeta", 43, "8", "one attribute",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:88px; color:#b79cff">08 — one attribute</div>'
'<h1 class="h1" data-d="0.1" style="position:absolute; left:104px; top:120px; font-size:66px">Light and dark. Both designed.</h1>'
'<div class="mono" style="position:absolute; left:110px; top:208px; font-size:20px; color:#c9b6ff">'
'  <span data-tipea="data-nz-theme=&quot;dark&quot;" data-d="0.9">data-nz-theme="dark"</span>'
'  <span style="display:inline-block;width:10px;height:1em;background:#905dff;vertical-align:text-bottom"></span></div>'
+ portal(110, 262, 660, 470, '<img src="img/dashboard.png" data-ken="1.04" style="position:absolute; inset:0; width:100%; height:100%;'
         ' object-fit:cover; object-position:top left">'
         '<div class="tag" style="position:absolute; left:16px; top:16px; z-index:8; background:#2563eb; color:#fff">light</div>',
         cls="z-index:2")
+ portal(830, 262, 660, 470, '<img src="img/dashboard-dark.png" data-ken="1.04" style="position:absolute; inset:0; width:100%; height:100%;'
         ' object-fit:cover; object-position:top left">'
         '<div class="tag" style="position:absolute; left:16px; top:16px; z-index:8; background:#f97316; color:#111">dark</div>',
         cls="z-index:2")
+ '<div style="position:absolute; left:796px; top:240px; width:2px; height:512px; background:linear-gradient(180deg,transparent,rgba(255,255,255,.45),transparent); z-index:9"></div>'
+ '<div style="position:absolute; left:786px; top:444px; width:22px; height:104px; border-radius:11px; z-index:10;'
' background:linear-gradient(180deg,rgba(255,255,255,.65),rgba(255,255,255,.18)); border:1px solid rgba(255,255,255,.6);'
' box-shadow:0 8px 30px rgba(0,0,0,.6)"></div>'
+ '<div class="mono" data-d="4.2" style="position:absolute; left:0; top:762px; width:100%; text-align:center; font-size:20px; color:rgba(255,255,255,.42)">same markup · one attribute · zero re-exports</div>')

# ── 09 · LA RECETA ─────────────────────────────────────────────────────────────
receta = [
    ("census.json", "what exists — machine-readable", "JSON", 1.15),
    ("judge.py", "what is allowed — proven, not promised", "PY", 2.3),
    ("SKILL.md", "how to build it — step by step", "MD", 3.45),
]
filas9 = ""
for i, (f, d, tipo, dd) in enumerate(receta):
    top = 96 + i * 140
    filas9 += (f'<div class="file" data-d="{dd}" style="top:{top}px">'
               f'<div class="mono" style="position:absolute; left:0; top:24px; font-size:26px; color:#fff">{f}</div>'
               f'<div style="position:absolute; left:0; top:66px; font-size:17px; color:rgba(255,255,255,.48)">{d}</div>'
               f'<div class="mono" style="position:absolute; right:0; top:26px; font-size:15px; color:#8fa8ff;'
               f' border:1px solid rgba(130,160,255,.35); border-radius:6px; padding:4px 9px">{tipo}</div></div>')

slides["09-receta"] = ("indigo", 47, "9", "the recipe",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:168px; color:#8f9dff">09 — the recipe</div>'
'<h1 class="h1 pz" style="position:absolute; left:104px; top:212px; font-size:104px">Steal the<br>recipe.</h1>'
'<div class="sub" data-d="1.0" style="position:absolute; left:110px; top:452px; font-size:25px; max-width:540px; line-height:1.5">'
'Aurora is one implementation. Yours can be the next — same three pieces, your tokens.</div>'
'<div class="mono" data-d="4.0" style="position:absolute; left:110px; top:566px; font-size:18px; color:rgba(255,255,255,.40)">'
'  MIT · fork it · ship it</div>'
+ portal(760, 150, 740, 600, '<div class="chip" style="inset:16px; border-radius:22px"></div>'
         '<div style="position:absolute; left:52px; right:52px; top:66px; bottom:64px; z-index:6">' + filas9 + '</div>'
         '<div data-d="4.3" class="mono" style="position:absolute; left:52px; bottom:34px; font-size:19px; color:#a9b8ff">'
         '  → your design system</div>',
         cls="z-index:3"))

# ── 10 · CIERRE ────────────────────────────────────────────────────────────────
letras = [("#3a7aff", "A"), ("#6261ff", "U"), ("#417eff", "R"), ("#2f9e74", "O"), ("#ff8c4e", "R"), ("#a78bfa", "A")]
word = "".join(f'<span data-d="{0.15 + i * 0.07}">{l}</span>' for i, (c, l) in enumerate(letras))

slides["10-cierre"] = ("ntizar", 53, "10", "the close",
'<div class="h1 pz" style="position:absolute; left:0; top:158px; width:100%; text-align:center; font-size:152px; letter-spacing:.02em">'
'  <span style="white-space:nowrap">'
+ "".join(f'<span style="color:{c}">{l}</span>' for c, l in [("#3a7aff","A"),("#6261ff","U"),("#417eff","R"),("#2f9e74","O"),("#ff8c4e","R"),("#a78bfa","A")])
+ '</span></div>'
'<div data-d="0.8" style="position:absolute; left:0; top:352px; width:100%; text-align:center; font-size:36px; color:#fff; font-weight:500">'
'  Any agent. Any brand. <span style="color:#ff8c4e; font-weight:700">Zero guessing.</span></div>'
+ portal(310, 440, 980, 96,
         '<div class="chip" style="inset:8px; border-radius:22px; background:rgba(10,14,28,.62)"></div>'
         '<div class="mono" style="position:absolute; left:34px; top:31px; z-index:7; font-size:23px; color:#eef2ff">'
         '<span style="color:#ff6a00; font-weight:700">$</span> hermes plugins install aurora-design-system</div>',
         cls="z-index:3", radio="border-radius:22px")
+ '<div data-d="2.0" style="position:absolute; left:0; top:580px; width:100%; text-align:center; font-size:21px; color:rgba(255,255,255,.52)">'
'  github.com/Ntizar/hermes-aurora &nbsp;·&nbsp; ntizar.github.io/hermes-aurora</div>'
'<div data-d="2.6" style="position:absolute; left:0; top:628px; width:100%; text-align:center; font-size:17px; color:rgba(255,255,255,.32)">'
'  2 tools · 4 skills · 0 network · MIT</div>'
'<div data-d="3.2" style="position:absolute; left:0; bottom:76px; width:100%; text-align:center; font-size:17px; color:rgba(255,255,255,.26)">'
'  Hecho con ❤️ por David Antizar</div>'
'<div class="hud" style="left:64px; bottom:46px">10 · the close</div>')

for nombre, (marca, seed, act, etiqueta, cuerpo) in slides.items():
    (OUT / f"{nombre}.html").write_text(escena(nombre, marca, seed, cuerpo, act, etiqueta), encoding="utf-8")
    print("slide v8", nombre, marca, act or "—")
print("ok", len(slides))
