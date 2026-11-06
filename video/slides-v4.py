#!/usr/bin/env python3
"""Slides v4 — CDN local (sin parpadeos), 12 escenas, más diseño en pantalla.
Beats negros + productos, tríptico de páginas, y el salto claro→oscuro del mismo dashboard."""
from __future__ import annotations
import shutil
from pathlib import Path

AURORA = Path("/home/nan/Projects/Aurora")
OUT = Path(__file__).resolve().parent / "slides"
TMP = Path("/tmp/vq2/aurora-css")

# Copia LOCAL de los packs que usan las slides: los file:// con recursos locales
# no dependen de la red → cero parpadeos por CDN.
if TMP.exists(): shutil.rmtree(TMP)
TMP.mkdir(parents=True)
for p in ["tokens.css", "marcas/monocromo.css", "packs/p1-layout.css", "packs/p3-typography.css",
          "packs/p4-actions.css", "packs/p6-feedback.css", "packs/p8-data.css", "packs/all.css"]:
    src = AURORA / p
    if src.exists():
        (TMP / src.name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, TMP / src.name)

CSS_LOCAL = "".join(f'<link rel="stylesheet" href="aurora-css/{Path(p).name}">\n'
                    for p in ["tokens.css", "marcas/monocromo.css", "packs/p1-layout.css",
                              "packs/p3-typography.css", "packs/p4-actions.css",
                              "packs/p6-feedback.css", "packs/p8-data.css"])

HEAD_DARK = f"""<!DOCTYPE html>
<html lang="en" data-nz-theme="dark" data-nz-marca="monocromo">
<head>
<meta charset="utf-8">
<title>{{t}}</title>
{CSS_LOCAL}<style>
  html, body {{ height: 100%; background: #000; }}
  body {{ display: grid; place-items: center; overflow: hidden; }}
  .slide {{ width: 1600px; height: 900px; padding: 90px 110px 150px; box-sizing: border-box;
            display: flex; flex-direction: column; justify-content: center; gap: 44px; position: relative; }}
  .beat {{ font-size: 96px; font-weight: 800; letter-spacing: -0.03em; line-height: 1.04; color: #fff; max-width: 1250px; }}
  .beat .dim {{ color: #6f6f6f; }}
  .mono {{ font-family: ui-monospace, "SFMono-Regular", Menlo, monospace; }}
  .nz-reveal {{ opacity: 0; animation: nzIn .55s var(--d, 0s) cubic-bezier(.2,.7,.2,1) both; }}
  .nz-push {{ opacity: 0; animation: nzPush 1.1s cubic-bezier(.16,.84,.3,1) both; }}
  @keyframes nzIn {{ from {{ opacity: 0; transform: translateY(26px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes nzPush {{ from {{ opacity: 0; transform: scale(.96); }} to {{ opacity: 1; transform: none; }} }}
  .ken {{ animation: nzKen var(--ken, 5s) linear both; }}
  @keyframes nzKen {{ from {{ transform: scale(1); }} to {{ transform: scale(1.05); }} }}
  .term {{ border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,.12); box-shadow: 0 24px 80px rgba(0,0,0,.55); }}
  .term__bar {{ display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: #1a1a1e; }}
  .term__bar i {{ width: 12px; height: 12px; border-radius: 50%; background: #3a3a40; }}
  .term__bar i:first-child {{ background: #e8e8e8; }}
  .term__bar span {{ margin-left: 8px; color: #7a7a85; font-size: 15px; font-family: ui-monospace, Menlo, monospace; }}
  .term__body {{ padding: 44px 48px; background: #0a0a0d; color: #f2f2f5; font-size: 30px; line-height: 1.5; }}
  .term__body pre {{ margin: 0; }}
  .prompt {{ color: #f0c75e; font-weight: 700; }}
  .cursor {{ display: inline-block; width: 14px; height: 1.05em; background: #f0c75e; vertical-align: text-bottom; }}
  .k {{ color: #9db8ff; }} .s {{ color: #bfe3c0; }} .bad {{ color: #ff9d87; }} .ok7 {{ color: #bfe3c0; }}
  .eyebrow {{ color: #8a8a8a; font-size: 20px; letter-spacing: .22em; text-transform: uppercase; }}
  .foot {{ position: absolute; bottom: 54px; left: 110px; right: 110px; display: flex; justify-content: space-between; color: #6f6f6f; font-size: 21px; }}
  .trio {{ display: flex; gap: 28px; }}
  .trio .shot-wrap {{ flex: 1; }}
  .shot-wrap {{ border-radius: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,.12); box-shadow: 0 30px 90px rgba(0,0,0,.5); }}
  .shot {{ width: 100%; height: 520px; object-fit: cover; object-position: top left; display: block; }}
  .trio .shot {{ height: 460px; }}
</style>
</head>
<body class="nz">
"""

HEAD_LIGHT = f"""<!DOCTYPE html>
<html lang="en" data-nz-theme="light" data-nz-marca="monocromo">
<head>
<meta charset="utf-8">
<title>{{t}}</title>
{CSS_LOCAL}<style>
  html, body {{ height: 100%; }}
  body {{ display: grid; place-items: center; overflow: hidden; background: #fff; }}
  .slide {{ width: 1600px; height: 900px; padding: 90px 110px 150px; box-sizing: border-box;
            display: flex; flex-direction: column; justify-content: center; gap: 40px; position: relative; }}
  .beat {{ font-size: 96px; font-weight: 800; letter-spacing: -0.03em; line-height: 1.04; color: #000; max-width: 1250px; }}
  .beat .dim {{ color: #9a9a9a; }}
  .mono {{ font-family: ui-monospace, "SFMono-Regular", Menlo, monospace; }}
  .nz-reveal {{ opacity: 0; animation: nzIn .55s var(--d, 0s) cubic-bezier(.2,.7,.2,1) both; }}
  .nz-push {{ opacity: 0; animation: nzPush 1.1s cubic-bezier(.16,.84,.3,1) both; }}
  @keyframes nzIn {{ from {{ opacity: 0; transform: translateY(26px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes nzPush {{ from {{ opacity: 0; transform: scale(.96); }} to {{ opacity: 1; transform: none; }} }}
  .ken {{ animation: nzKen var(--ken, 5s) linear both; }}
  @keyframes nzKen {{ from {{ transform: scale(1); }} to {{ transform: scale(1.05); }} }}
  .term {{ border-radius: 14px; overflow: hidden; border: 1px solid rgba(0,0,0,.14); box-shadow: 0 24px 80px rgba(0,0,0,.10); }}
  .term__bar {{ display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: #10182b; }}
  .term__bar i {{ width: 12px; height: 12px; border-radius: 50%; background: #3a4a6b; }}
  .term__bar i:first-child {{ background: #d8d8d8; }}
  .term__bar span {{ margin-left: 8px; color: #8a96b5; font-size: 15px; font-family: ui-monospace, Menlo, monospace; }}
  .term__body {{ padding: 44px 48px; background: #0d1526; color: #e8ecf5; font-size: 30px; line-height: 1.5; }}
  .term__body pre {{ margin: 0; }}
  .prompt {{ color: #f0c75e; font-weight: 700; }}
  .cursor {{ display: inline-block; width: 14px; height: 1.05em; background: #f0c75e; vertical-align: text-bottom; }}
  .k {{ color: #9db8ff; }} .s {{ color: #bfe3c0; }} .bad {{ color: #ff9d87; }} .ok7 {{ color: #bfe3c0; }}
  .eyebrow {{ color: #6a6a6a; font-size: 20px; letter-spacing: .22em; text-transform: uppercase; }}
  .trio {{ display: flex; gap: 28px; }}
  .trio .shot-wrap {{ flex: 1; }}
  .shot-wrap {{ border-radius: 16px; overflow: hidden; border: 1px solid rgba(0,0,0,.12); box-shadow: 0 30px 90px rgba(0,0,0,.14); }}
  .shot {{ width: 100%; height: 520px; object-fit: cover; object-position: top left; display: block; }}
  .trio .shot {{ height: 460px; }}
  .half {{ display: flex; gap: 28px; align-items: stretch; }}
  .half .shot-wrap {{ flex: 1; }}
  .half .shot {{ height: 500px; }}
</style>
</head>
<body class="nz">
"""

FOOT = "</body>\n</html>\n"

slides = {}

slides["01-beat1"] = ("dark", """
<div class="slide">
  <h1 class="beat nz-push">Every agent can<br>build a page.</h1>
  <div class="foot nz-reveal" style="--d:1.6s"><span>Aurora</span><span>Hermes Agent</span></div>
</div>
""")

slides["02-beat2"] = ("dark", """
<div class="slide">
  <h1 class="beat nz-push">Almost none<br><span class="dim">can prove it.</span></h1>
  <div class="foot nz-reveal" style="--d:1.4s"><span>Aurora</span><span>Hermes Agent</span></div>
</div>
""")

slides["03-nombre"] = ("light", """
<div class="slide">
  <h1 class="beat nz-push" style="font-size:150px">Aurora.</h1>
  <p class="beat nz-reveal" style="--d:.9s; font-size:40px; font-weight:500">A design system your agent can't fake.</p>
</div>
""")

slides["04-buscar"] = ("light", """
<div class="slide">
  <span class="eyebrow nz-reveal" style="--d:.1s">aurora_search</span>
  <div class="term nz-reveal" style="--d:.35s">
    <div class="term__bar"><i></i><i></i><i></i><span>census — 2,223 objects</span></div>
    <div class="term__body"><pre><code><span class="prompt">›</span> <span id="c1"></span><span class="cursor"></span>
<span class="nz-reveal" style="--d:2.6s">{
  <span class="k">"family"</span>:  <span class="s">"nz-table"</span>,
  <span class="k">"pack"</span>:    <span class="s">"packs/p8-data.css"</span>,
  <span class="k">"classes"</span>: [<span class="s">"nz-table"</span>, <span class="s">"nz-table--apilable"</span>, <span class="s">"nz-table--striped"</span>, …],
  <span class="k">"markup"</span>:  <span class="s">"&lt;div class=\\"nz-table-wrap\\"&gt;…"</span>
}</span></code></pre></div>
  </div>
  <p class="beat nz-reveal" style="--d:4.2s; font-size:34px; font-weight:600">Real objects. Real markup. Every class.</p>
</div>
<script>
  const T1 = 'aurora_search("table that stacks on mobile")';
  const e1 = document.getElementById('c1'); let i = 0;
  (function t(){ if (i < T1.length) { e1.textContent = T1.slice(0, ++i); setTimeout(t, 40); } })();
</script>
""")

slides["05-trio"] = ("light", """
<div class="slide">
  <span class="eyebrow nz-reveal" style="--d:.1s">one system · three products</span>
  <div class="trio">
    <div class="shot-wrap ken nz-reveal" style="--d:.25s; --ken:6.4s"><img class="shot" src="../../docs/screenshots/landing.png" alt="Landing"></div>
    <div class="shot-wrap ken nz-reveal" style="--d:.45s; --ken:6.4s"><img class="shot" src="../../docs/screenshots/dashboard.png" alt="Dashboard"></div>
    <div class="shot-wrap ken nz-reveal" style="--d:.65s; --ken:6.4s"><img class="shot" src="../../docs/screenshots/login.png" alt="Login"></div>
  </div>
</div>
""")

slides["06-validar"] = ("dark", """
<div class="slide">
  <span class="eyebrow nz-reveal" style="--d:.1s">aurora_validate</span>
  <div class="term nz-reveal" style="--d:.35s">
    <div class="term__bar"><i></i><i></i><i></i><span>report</span></div>
    <div class="term__body"><pre><code><span class="prompt">›</span> <span id="c2"></span><span class="cursor"></span>
<span class="nz-reveal" style="--d:2.4s">ok: <span class="bad">false</span>
 <span class="bad">-</span> unknown class: nz-card--glass
 <span class="bad">-</span> gradient in page CSS
 <span class="bad">-</span> 3 hand-written colours
 <span class="bad">-</span> missing attribution footer</span></code></pre></div>
  </div>
</div>
<script>
  const T2 = 'aurora_validate(path="page.html")';
  const e2 = document.getElementById('c2'); let j = 0;
  (function t(){ if (j < T2.length) { e2.textContent = T2.slice(0, ++j); setTimeout(t, 40); } })();
</script>
""")

slides["07-limpio"] = ("dark", """
<div class="slide">
  <span class="eyebrow nz-reveal" style="--d:.1s">two iterations later</span>
  <div class="nz-callout nz-callout--success nz-reveal" style="--d:.4s">
    <p class="mono" style="font-size:26px">ok: true · 0 failures · 8 packs linked</p>
  </div>
  <div class="shot-wrap ken nz-reveal" style="--d:.8s; --ken:5.4s">
    <img class="shot" src="../../docs/screenshots/dashboard-dark.png" alt="Dashboard in dark theme">
  </div>
</div>
""")

slides["08-dark"] = ("dark", """
<div class="slide">
  <span class="eyebrow nz-reveal" style="--d:.1s">same markup · one attribute</span>
  <h1 class="beat nz-push" style="font-size:72px">Light and dark,<br><span class="dim">both designed.</span></h1>
  <div class="half">
    <div class="shot-wrap ken nz-reveal" style="--d:.5s; --ken:5.4s"><img class="shot" src="../../docs/screenshots/dashboard.png" alt="Dashboard light"></div>
    <div class="shot-wrap ken nz-reveal" style="--d:.7s; --ken:5.4s"><img class="shot" src="../../docs/screenshots/dashboard-dark.png" alt="Dashboard dark"></div>
  </div>
</div>
""")

slides["09-instalar"] = ("dark", """
<div class="slide">
  <h1 class="beat nz-push" style="font-size:84px">Aurora <span class="dim">for</span> Hermes.</h1>
  <div class="term nz-reveal" style="--d:.6s; max-width:1100px">
    <div class="term__bar"><i></i><i></i><i></i><span>terminal</span></div>
    <div class="term__body"><pre><code><span class="prompt">$</span> <span id="c3"></span><span class="cursor"></span>
<span class="ok7 nz-reveal" style="--d:3.0s">✓ installed · 2 tools, 4 skills, 0 network</span></code></pre></div>
  </div>
  <p class="nz-reveal" style="--d:3.8s; color:#8a8a8a; font-size:26px">github.com/Ntizar/hermes-aurora</p>
</div>
<script>
  const T3 = 'hermes plugins install aurora-design-system';
  const e3 = document.getElementById('c3'); let k = 0;
  (function t(){ if (k < T3.length) { e3.textContent = T3.slice(0, ++k); setTimeout(t, 42); } })();
</script>
""")

for name, (tema, body) in slides.items():
    head = (HEAD_DARK if tema == "dark" else HEAD_LIGHT).replace("{t}", name)
    (OUT / f"{name}.html").write_text(head + body + FOOT, encoding="utf-8")
    print("slide", name, tema)
