#!/usr/bin/env python3
"""Slides v9 — «CATALOGUE & INSPECTOR» (70 s). Reorganización completa.

Reglas de esta versión:
  · Logo = azul #3a7aff + naranja #ff6a00 (AURORA + punto). Nada de multicolor.
  · Doble explicación: 03 en palabras llanas (catálogo + inspector), 04 en ingeniería
    (census.json · aurora_validate · SKILL.md).
  · 05: seis planos de página dibujados (no capturas vacías de esqueletos).
  · Sin música: el film respira con voz y silencio.
"""
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent / "slides"
RAIZ = Path(__file__).resolve().parent
MANIFEST = json.loads((RAIZ / "manifest-v9.json").read_text())
OFFSETS = json.loads((RAIZ / "offsets-v9.json").read_text())
TOTAL = 70.0
AZUL, NARANJA = "#3a7aff", "#ff6a00"

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
  .tarjeta { position:absolute; border-radius:26px; overflow:hidden; }
  .tcol { position:absolute; top:0; left:0; width:100%; will-change:transform; }
  .fila { position:absolute; left:0; right:0; height:132px; border-top:1px solid rgba(255,255,255,.10); }
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
document.querySelectorAll('.tcol').forEach((el, i) => {
  const v = 34 + i * 13;
  const y = ((t0 * v) % (el.scrollHeight || 700));
  el.style.transform = 'translateY(' + (-y) + 'px)';
});
"""

def portal(x, y, w, h, interior="", ref=False, cls="", radio=""):
    vidrio = (f'<div class="vidrio"><div class="clon" style="transform:translate(-{x}px,-{y}px)">'
              + CIELO + '</div></div><div class="tinte"></div><div class="grano"></div>')
    refc = " ref" if ref else ""
    return (f'<div class="portal{refc}" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px;'
            f' {radio} {cls}">' + vidrio + interior + '</div>')

def marca(tam):
    return (f'<span style="color:{AZUL}">AURORA</span>'
            f'<span style="color:{NARANJA}">.</span>')

def hud(n, etiqueta):
    return (f'<div class="hud" style="left:64px; top:50px"><span class="punto" style="background:#5b8cff;box-shadow:0 0 12px #5b8cff"></span>'
            f'<span style="letter-spacing:.14em;color:#5b8cff">AURORA<span style="color:{NARANJA}">.</span></span>'
            f' <span class="dim" style="letter-spacing:.06em">/ hermes-aurora</span></div>'
            f'<div class="hud" style="right:64px; top:50px">ACT <b>{n}</b> <span class="dim">/ 10</span></div>'
            f'<div class="hud low" style="left:64px; bottom:46px">{etiqueta}</div>'
            '<div class="prog"><div class="prog-fill"></div></div>'
            '<div class="esq" style="left:30px; top:30px; border-left-width:1px; border-top-width:1px"></div>'
            '<div class="esq" style="right:30px; bottom:30px; border-right-width:1px; border-bottom-width:1px"></div>')

def escena(nombre, marca_n, seed, cuerpo, act, etiqueta):
    css = (BASE_CSS.replace("__GRANO__", GRANO).replace("__BRAND__", MARCAS[marca_n][1]))
    js = (JS_CIELO.replace("__SKY__", json.dumps(MARCAS[marca_n]))
          .replace("__SEED__", str(seed)).replace("__TOTAL__", str(TOTAL)))
    t0 = OFFSETS[nombre]
    sac = {"02-inventa": "6.2,0.4,5", "06-juez": "4.9,0.45,7", "07-bucle": "3.6,0.35,4"}.get(nombre, "")
    sac = f' data-shake="{sac}"' if sac else ""
    return (f'<!DOCTYPE html>\n<html lang="en" data-nz-marca="{marca_n}"><head><meta charset="utf-8">'
            f'<title>{nombre}</title>\n<style>{css}</style>{FILTRO}</head>\n'
            f'<body data-t0="{t0}"><div class="marco"{sac}>\n{CIELO}<div class="vineta"></div>\n'
            f'{hud(act, etiqueta) if act else ""}\n{cuerpo}\n</div>'
            f'<script>{js}</script></body></html>\n')

slides = {}

# ── 00 · OPEN ──────────────────────────────────────────────────────────────────
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
<div class="chip" data-d="0.55,0.3" style="left:{X0 + 42}px; top:{Y0 + H0 - 86}px; height:56px; width:540px;
     border-radius:14px; background:rgba(4,6,14,.82); z-index:9"></div>
<div class="mono" style="position:absolute; left:{X0 + 64}px; top:{Y0 + H0 - 68}px; z-index:10; font-size:22px; color:#dfe6f5">
  <span style="color:{NARANJA}; font-weight:700">›</span>
  <span data-tipea="build me a landing page" data-d="0.75">build me a landing page</span>
  <span style="display:inline-block;width:11px;height:1em;background:{NARANJA};vertical-align:text-bottom"></span>
</div>
<div class="hud" style="left:64px; bottom:46px">a film about proof</div>
<div class="prog"><div class="prog-fill"></div></div>""")

# ── 01 · LOOKS FINISHED ────────────────────────────────────────────────────────
fallos1 = ""
for i, (t, d, dd) in enumerate([
        ("unknown class", "nz-card--glass", 1.5),
        ("banned gradient", "linear-gradient(#fff0…)", 2.3),
        ("hand-written colour", "#3b82f6 ×3", 3.1)]):
    y = 480 + i * 66
    fallos1 += (f'<div data-d="{dd}" style="position:absolute; left:110px; top:{y}px; z-index:8">'
                f'<span style="display:inline-block; width:9px; height:9px; border-radius:50%;'
                f' background:#ff5d4f; box-shadow:0 0 12px #ff5d4f; margin-right:14px"></span>'
                f'<span style="font-size:22px; font-weight:600; color:#fff">{t}</span>'
                f'<span class="mono" style="font-size:17px; color:#ff9c92; margin-left:16px">{d}</span></div>')

slides["01-acabada"] = ("ntizar", 13, "1", "looks finished",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:176px; color:#6b9dff">01 — the gap</div>'
'<h1 class="h1 pz" style="position:absolute; left:104px; top:196px; font-size:100px">Looks<br>finished.</h1>'
'<div class="h1" data-d="1.0" style="position:absolute; left:110px; top:400px; font-size:44px; color:#ff6b5e">It isn\'t.</div>'
+ fallos1
+ portal(880, 60, 800, 780, '<img src="img/landing.png" data-ken="1.05" style="position:absolute; inset:0;'
         ' width:100%; height:100%; object-fit:cover; object-position:top left">', cls="z-index:2"))

# ── 02 · IT GUESSES ────────────────────────────────────────────────────────────
TOKENS_A = ["nz-card--glass", "hero-gradient", "btn-primary", "text-xl", "shadow-lg",
            ".nz-hero", "rounded-2xl", "#3b82f6", "bg-white/80", "gap-6"]
TOKENS_B = ["nz-btn--glow", "card-shadow", "px-8", "font-black", ".nz-panel", "#2563eb",
            "linear-gradient(90deg,…)", "tracking-tight", "hover:scale-105", "z-50"]
def columna(tokens, x, dop, color_strike=True):
    filas = ""
    for i, tk in enumerate(tokens * 3):
        tachado = color_strike and (i % 5 == 3)
        estilo = ("text-decoration:line-through; color:#ff8b7f; font-weight:700" if tachado
                  else "color:rgba(255,255,255,.86)")
        filas += (f'<div class="mono" style="font-size:19px; line-height:2.15; white-space:nowrap; {estilo}">{tk}</div>')
    return (f'<div style="position:absolute; left:{x}px; top:0; width:410px; height:900px; overflow:hidden; z-index:4;'
            f' opacity:.92; mask-image:linear-gradient(180deg,transparent,#000 18%,#000 82%,transparent)">'
            f'<div class="tcol" data-speed="{dop}" style="position:relative">{filas}</div></div>')

slides["02-inventa"] = ("carmesi", 19, "2", "the guess",
'<div style="position:absolute; inset:0; z-index:1">'
+ portal(0, 0, 1600, 900, '<img src="img/dashboard.png" style="position:absolute; inset:0; width:100%; height:100%;'
         ' object-fit:cover; object-position:top left; filter:brightness(.30) saturate(.5)">', cls="border-radius:0; border:0")
+ '</div><div style="position:absolute; inset:0; background:rgba(4,5,12,.38); z-index:2"></div>'
+ columna(TOKENS_A, 24, 40) + columna(TOKENS_B, 1176, 55)
+ '<div style="position:absolute; left:468px; top:280px; width:680px; z-index:6">'
'  <h1 class="h1" data-d="0.1" style="font-size:92px">So it<br><span style="color:#ff6b5e">guesses.</span></h1>'
'  <p class="sub" data-d="1.6" style="font-size:26px; line-height:1.45; margin-top:26px; max-width:640px">'
'  Names, gradients and colours that were never in your system.</p></div>'
+ '<div class="hud" style="left:64px; bottom:46px">02 · the guess</div>')

# ── 03 · PLAIN WORDS ───────────────────────────────────────────────────────────
def tarjeta_llano(x, num, titulo, claim, puntos, color):
    lista = ""
    for i, p in enumerate(puntos):
        lista += (f'<div style="display:flex; gap:12px; margin-top:14px; align-items:flex-start">'
                  f'<span style="color:{color}; font-weight:800; font-size:18px; line-height:1.3">·</span>'
                  f'<span style="font-size:20px; color:rgba(255,255,255,.80); line-height:1.35">{p}</span></div>')
    return portal(x, 360, 660, 390,
        f'<div class="chip" style="inset:14px; border-radius:20px"></div>'
        f'<div style="position:absolute; left:38px; right:34px; top:36px; z-index:7">'
        f'<div class="mono" style="font-size:15px; color:{color}">{num}</div>'
        f'<div style="margin-top:10px; font:800 34px/1.1 \'Inter var\'; color:#fff">{titulo}</div>'
        f'<div style="margin-top:10px; font-size:18px; color:rgba(255,255,255,.52); line-height:1.4">{claim}</div>'
        f'{lista}</div>', cls="z-index:3")

slides["03-llano"] = ("aurora", 23, "3", "in plain words",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:126px; color:#7fb0ff">03 — in plain words</div>'
'<h1 class="h1 pz" style="position:absolute; left:104px; top:150px; font-size:72px">A parts catalogue,<br>and a building inspector.</h1>'
'<div class="sub" data-d="1.2" style="position:absolute; left:110px; top:300px; font-size:23px; max-width:1320px">'
'  Two everyday ideas. That is the whole system.</div>'
+ tarjeta_llano(110, "01 · THE CATALOGUE", "Everything you already have.",
               "The real parts, with their real names.", [
                   "2,223 parts — the real list, not a screenshot",
                   "The AI reads it; it doesn't invent names"], AZUL)
+ tarjeta_llano(830, "02 · THE INSPECTOR", "Nothing goes live unchecked.",
               "It checks the page against that list.", [
                   "Four rules: names, effects, colours, credit",
                   "Zero faults, or the page doesn't go live"], NARANJA))

# ── 04 · FOR ENGINEERS ─────────────────────────────────────────────────────────
filas4 = [
    ("census.json", "Every object, class and modifier, machine-readable.", "2,223 classes · 417 families", 1.0),
    ("aurora_validate", "Fails the build when the page leaves the census.", "4 rules · milliseconds", 2.0),
    ("SKILL.md × 4", "The procedure and the traps, written for the agent.", "when to use what", 3.0),
]
doc4 = ""
for i, (f, d, m, dd) in enumerate(filas4):
    top = 96 + i * 138
    doc4 += (f'<div data-d="{dd}" style="position:absolute; left:56px; right:52px; top:{top}px">'
             f'<div class="mono" style="font-size:25px; color:#fff">{f}</div>'
             f'<div style="margin-top:8px; font-size:18px; color:rgba(255,255,255,.55); line-height:1.35">{d}</div>'
             f'<div class="mono" style="margin-top:9px; font-size:14px; color:#7fb0ff">{m}</div></div>')
    if i < 2:
        doc4 += f'<div style="position:absolute; left:56px; right:52px; top:{top + 112}px; height:1px; background:rgba(255,255,255,.09)"></div>'

slides["04-tecnico"] = ("aurora", 29, "4", "for engineers",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:158px; color:#7fb0ff">04 — for engineers</div>'
'<h1 class="h1 pz" style="position:absolute; left:104px; top:204px; font-size:92px">The same three<br>pieces. As files.</h1>'
'<div class="sub" data-d="1.1" style="position:absolute; left:110px; top:412px; font-size:23px; max-width:560px; line-height:1.5">'
'  No new toolchain, no service, no network. Three artefacts your repo can own.</div>'
+ portal(780, 130, 720, 620, '<div class="chip" style="inset:14px; border-radius:20px"></div>' + doc4
         + '<div data-d="4.0" class="mono" style="position:absolute; left:56px; right:40px; bottom:42px; z-index:8;'
           ' font-size:16px; color:#a9c8ff; line-height:1.5">→ aurora_validate("page.html")<br>'
           '&nbsp;&nbsp;{ ok: false, fallos: 4 }</div>',
         cls="z-index:3"))

# ── 05 · SIX PAGE SKELETONS ────────────────────────────────────────────────────
def wire(tipo, color):
    b = f'rgba(255,255,255,.16)'
    c = f'{color}44'
    def blk(x, y, w, h, bg=b, r=4):
        return (f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px;'
                f' background:{bg}; border-radius:{r}px"></div>')
    if tipo == "landing":
        return blk(16,14,368,10) + blk(16,38,368,64,c) + blk(16,116,112,34) + blk(144,116,112,34) + blk(272,116,112,34)
    if tipo == "dashboard":
        return blk(16,14,78,136,c) + blk(108,14,276,12) + blk(108,38,86,34) + blk(206,38,86,34) + blk(304,38,80,34) + blk(108,86,276,64)
    if tipo == "login":
        return blk(120,26,160,112,c) + blk(136,44,128,10) + blk(136,64,128,10) + blk(136,84,128,10) + blk(136,108,60,14,f'rgba(255,255,255,.34)')
    if tipo == "shop":
        return blk(16,14,368,10) + blk(16,40,172,56,c) + blk(200,40,184,56,c) + blk(16,104,172,44) + blk(200,104,184,44)
    if tipo == "chat":
        return blk(16,20,190,30) + blk(200,60,184,30,c) + blk(16,100,150,26) + blk(180,134,204,24,c)
    return blk(16,14,90,136,c) + blk(118,14,266,10) + blk(118,36,210,26) + blk(118,70,240,26) + blk(118,104,180,26)

PLANOS = [
    ("landing.html", "Landing", "landing", 0),
    ("dashboard.html", "Dashboard", "dashboard", 1),
    ("login-form.html", "Login", "login", 2),
    ("e-commerce.html", "Shop", "shop", 3),
    ("chat-ia.html", "AI chat", "chat", 4),
    ("escritorio-app.html", "App shell", "app", 5),
]
tarjetas = ""
for i, (fich, nom, tipo, idx) in enumerate(PLANOS):
    x = 90 + (i % 3) * 505
    y = 268 + (i // 3) * 268
    color = AZUL if idx % 2 == 0 else NARANJA
    tarjetas += portal(x, y, 460, 240,
        f'<div class="chip" style="inset:10px; border-radius:16px"></div>'
        f'<div style="position:absolute; left:24px; right:24px; top:22px; height:158px; z-index:6">{wire(tipo, color)}</div>'
        f'<div style="position:absolute; left:26px; bottom:18px; z-index:7; font:700 19px/1 \'Inter var\'; color:#fff">{nom}</div>'
        f'<div class="mono" style="position:absolute; right:24px; bottom:18px; z-index:7; font-size:13px; color:rgba(255,255,255,.42)">{fich}</div>',
        cls="z-index:3")

slides["05-planos"] = ("indigo", 31, "5", "six page skeletons",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:96px; color:#8f9dff">05 — don\'t start from zero</div>'
'<h1 class="h1 pz" style="position:absolute; left:104px; top:132px; font-size:64px">Six pages that already work.</h1>'
'<div class="sub" data-d="1.0" style="position:absolute; left:110px; top:208px; font-size:21px">'
'  Real skeletons in the system: the agent fills them, it does not reinvent them.</div>'
+ tarjetas)

# ── 06 · THE INSPECTOR ─────────────────────────────────────────────────────────
FALLOS6 = [
    ("unknown class", "nz-card--glass", "not in the census", 1.15),
    ("banned gradient", "linear-gradient(…)", "forbidden by contract", 1.75),
    ("hand-written colour", "#3b82f6 ×3", "use --nz-* tokens", 2.35),
    ("missing attribution", "footer", "required in every page", 2.95),
]
fallos6 = ""
for i, (titulo, token, nota, d) in enumerate(FALLOS6):
    fallos6 += (f'<div data-d="{d}" style="position:absolute; left:56px; right:56px; top:{176 + i * 74}px; z-index:7">'
                f'<span class="mono" style="color:#ff6b5e; font-size:24px; font-weight:700">✗</span> '
                f'<span style="font-size:24px; color:#fff; font-weight:600">{titulo}</span>'
                f'<span class="mono" style="font-size:21px; color:#ff9c92; margin-left:16px">{token}</span>'
                f'<span class="mono" style="font-size:16px; color:rgba(255,255,255,.38); margin-left:16px">{nota}</span></div>')

slides["06-juez"] = ("carmesi", 37, "6", "the inspector",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:96px; color:#ff7a6c">06 — the inspector</div>'
+ portal(90, 148, 1420, 570, '<div class="chip" style="inset:14px; border-radius:20px"></div>'
         '<div class="mono" style="position:absolute; left:56px; top:46px; z-index:7; font-size:23px; color:#f2e9e8">'
         '  <span style="color:#ff6b5e; font-weight:700">›</span> '
         '  <span data-tipea="aurora_validate(&quot;page.html&quot;)" data-d="0.55">aurora_validate("page.html")</span>'
         '  <span style="display:inline-block;width:11px;height:1em;background:#ff6b5e;vertical-align:text-bottom"></span>'
         '</div>' + fallos6
         + '<div data-d="3.4" class="mono" style="position:absolute; left:56px; bottom:40px; z-index:7; font-size:15px; color:rgba(255,255,255,.38)">'
           'scanned page.html · 1,204 lines · 2,223 known classes · 0 network</div>'
         + '<div data-claim="3.55,0.4" style="position:absolute; right:52px; top:30px; z-index:9; text-align:right">'
           '<div class="mono" data-count="3.55,0.35,0,4" style="font-size:80px; font-weight:700; color:#ff5d4f; line-height:1">4</div>'
           '<div class="k" style="color:#ff8b7f; margin-top:4px">violations</div></div>'
         + '<div class="mono" data-claim="4.15,0.35" style="position:absolute; right:44px; bottom:38px; z-index:9;'
           ' color:#ff5d4f; border:3px solid #ff5d4f; padding:10px 20px; font-size:32px; font-weight:700;'
           ' letter-spacing:.10em; transform:rotate(-5deg); background:rgba(12,2,2,.5)">BLOCKED</div>',
         cls="z-index:2 border-color:rgba(255,92,80,.35)")
+ '<div data-d="4.7" style="position:absolute; left:0; top:760px; width:100%; text-align:center; font-size:28px; font-weight:600; color:#fff">Caught in <span style="color:#ff6b5e; font-weight:800">milliseconds</span>.</div>')

# ── 07 · THE LOOP ──────────────────────────────────────────────────────────────
RUNS7 = [("run 2", "4 failures", "#ff6b5e", 0.9), ("run 3", "1 failure", "#ffb36b", 1.75), ("run 4", "0 failures", "#8fe3a6", 2.6)]
runs7 = ""
for i, (r, f, c, d) in enumerate(RUNS7):
    runs7 += (f'<div data-d="{d}" class="mono" style="position:absolute; left:52px; top:{180 + i * 84}px; z-index:7; font-size:25px">'
              f'<span style="color:rgba(255,255,255,.45)">{r}</span>'
              f'<span style="color:rgba(255,255,255,.20); margin:0 18px">→</span>'
              f'<span style="color:{c}; font-weight:700">{f}</span></div>')

slides["07-bucle"] = ("esmeralda", 41, "7", "the loop",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:96px; color:#63c39a">07 — the loop</div>'
+ portal(90, 150, 820, 560, '<div class="chip" style="inset:14px; border-radius:20px"></div>'
         '<div class="mono" style="position:absolute; left:52px; top:48px; z-index:7; font-size:21px; color:#e6f5ec">'
         '  <span style="color:#34d399; font-weight:700">›</span> while failures &gt; 0: fix · re-run</div>' + runs7
         + '<div data-claim="3.65,0.45" class="mono" style="position:absolute; left:52px; bottom:40px; z-index:8;'
           ' font-size:24px; color:#9ff0bb; font-weight:700">✓ PASSED — ok: true · 0 failures</div>',
         cls="z-index:2 border-color:rgba(52,211,153,.32)")
+ '<div data-claim="3.65,0.5" style="position:absolute; right:100px; top:200px; text-align:right; z-index:8">'
'  <div class="tag" style="background:rgba(52,211,153,.16); color:#8fe3a6; border:1px solid rgba(52,211,153,.4); margin-bottom:14px">passed</div><br>'
'  <div class="mono" data-count="3.65,0.4,4,0" style="font-size:230px; font-weight:700; line-height:.86; color:#34d399;'
'       text-shadow:0 0 80px rgba(52,211,153,.35)">0</div>'
'  <div class="k" style="color:#8fe3a6; margin-top:8px">failures left</div></div>'
+ portal(1000, 548, 510, 230, '<img src="img/dashboard-esm.png" style="position:absolute; inset:0; width:100%; height:100%;'
         ' object-fit:cover; object-position:top left">', cls="z-index:2"))

# ── 08 · ONE ATTRIBUTE ─────────────────────────────────────────────────────────
slides["08-tema"] = ("violeta", 43, "8", "one attribute",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:88px; color:#b79cff">08 — one attribute</div>'
'<h1 class="h1" data-d="0.1" style="position:absolute; left:104px; top:120px; font-size:66px">Light and dark. Both designed.</h1>'
'<div class="mono" style="position:absolute; left:110px; top:208px; font-size:20px; color:#c9b6ff">'
'  <span data-tipea="data-nz-theme=&quot;dark&quot;" data-d="0.85">data-nz-theme="dark"</span>'
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
+ '<div class="mono" data-d="3.6" style="position:absolute; left:0; top:762px; width:100%; text-align:center; font-size:20px; color:rgba(255,255,255,.42)">same markup · one attribute</div>')

# ── 09 · STEAL THE RECIPE ──────────────────────────────────────────────────────
RECETA = [
    ("Your catalogue", "census.json", "what exists, machine-readable", 0.9),
    ("Your inspector", "validator", "what is allowed, proven", 1.9),
    ("Your skills", "SKILL.md", "how to build it, step by step", 2.9),
]
filas9 = ""
for i, (t, f, d, dd) in enumerate(RECETA):
    top = 100 + i * 140
    filas9 += (f'<div class="fila" data-d="{dd}" style="top:{top}px">'
               f'<div style="position:absolute; left:0; top:22px; font:800 27px/1 \'Inter var\'; color:#fff">{t}</div>'
               f'<div class="mono" style="position:absolute; left:0; top:60px; font-size:15px; color:rgba(255,255,255,.42)">{f} · {d}</div>'
               f'<div class="mono" style="position:absolute; right:0; top:24px; font-size:20px; color:#8fa8ff">0{i+1}</div></div>')

slides["09-receta"] = ("indigo", 47, "9", "the recipe",
'<div class="k" data-d="0.05" style="position:absolute; left:110px; top:168px; color:#8f9dff">09 — the recipe</div>'
'<h1 class="h1 pz" style="position:absolute; left:104px; top:212px; font-size:104px">Steal the<br>recipe.</h1>'
'<div class="sub" data-d="1.0" style="position:absolute; left:110px; top:452px; font-size:25px; max-width:540px; line-height:1.5">'
'Aurora is the proof. The same three pieces work for your brand.</div>'
'<div class="mono" data-d="4.0" style="position:absolute; left:110px; top:560px; font-size:18px; color:rgba(255,255,255,.40)">MIT · fork it · ship it</div>'
+ portal(760, 150, 740, 600, '<div class="chip" style="inset:16px; border-radius:22px"></div>'
         '<div style="position:absolute; left:52px; right:52px; top:70px; bottom:64px; z-index:6">' + filas9 + '</div>'
         '<div data-d="4.3" class="mono" style="position:absolute; left:52px; bottom:34px; font-size:19px; color:#a9b8ff">'
         '  → your design system</div>', cls="z-index:3"))

# ── 10 · CLOSE ─────────────────────────────────────────────────────────────────
slides["10-cierre"] = ("ntizar", 53, "10", "the close",
f'<div class="h1 pz" style="position:absolute; left:0; top:170px; width:100%; text-align:center; font-size:150px; letter-spacing:.01em">'
f'  {marca(150)}</div>'
'<div data-d="0.8" style="position:absolute; left:0; top:356px; width:100%; text-align:center; font-size:36px; color:#fff; font-weight:500">'
'  Any agent. Any brand. <span style="color:#ff6a00; font-weight:700">Zero guessing.</span></div>'
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
'  Hecho con ❤️ por David Antizar</div>')

for nombre, (marca_n, seed, act, etiqueta, cuerpo) in slides.items():
    (OUT / f"{nombre}.html").write_text(escena(nombre, marca_n, seed, cuerpo, act, etiqueta), encoding="utf-8")
    print("slide v9", nombre, marca_n, act or "—")
print("ok", len(slides))
