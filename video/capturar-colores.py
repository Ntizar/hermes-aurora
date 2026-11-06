#!/usr/bin/env python3
"""Capturas de producto CON COLOR para el v6: cada demo en una marca de Aurora.

  landing    → marca ntizar   (azul #0057ff + naranja #ff6a00)
  dashboard  → marca aurora   (azul #2563eb + naranja #f97316)
  login      → marca violeta  (violeta #7c3aed + rosa #ec4899)
  dashboard  → marca esmeralda (para el tríptico/color extra)

Se guardan en video/slides/img/ (no tocan docs/screenshots, que siguen monocromo).
El demo enlaza la marca por CDN @v10: se cambia el atributo data-nz-marca y el <link>
de marcas/monocromo.css por la marca pedida (el orden tokens→marca ya es correcto).
"""
import re, shutil, subprocess
from pathlib import Path

DEMO = Path("/home/nan/Projects/hermes-aurora/demo")
OUT = Path("/home/nan/Projects/hermes-aurora/video/slides/img")
TMP = Path("/tmp/vq2/capcol")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"

PEDIDOS = [
    ("landing.html",    "landing.png",        "ntizar",  "light", 1440, 1780),
    ("dashboard.html",  "dashboard.png",      "aurora",  "light", 1440, 1900),
    ("dashboard.html",  "dashboard-esm.png",  "esmeralda", "light", 1440, 1900),
    ("login.html",      "login.png",          "violeta", "light", 1000, 1250),
    ("dashboard.html",  "dashboard-dark.png", "aurora",  "dark",  1440, 1900),
]

def preparar(fuente, marca, tema):
    src = (DEMO / fuente).read_text()
    # marca en el atributo y en el <link> de la marca
    src = re.sub(r'data-nz-marca="[^"]*"', f'data-nz-marca="{marca}"', src, count=1)
    src = src.replace("marcas/monocromo.css", f"marcas/{marca}.css")
    src = re.sub(r'data-nz-theme="[^"]*"', f'data-nz-theme="{tema}"', src, count=1)
    return src

TMP.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
for fuente, destino, marca, tema, w, h in PEDIDOS:
    html = TMP / (destino.replace(".png", "") + ".html")
    html.write_text(preparar(fuente, marca, tema))
    r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                        f"--window-size={w},{h}", "--hide-scrollbars",
                        "--virtual-time-budget=6000",
                        f"--screenshot={OUT}/{destino}", html.as_uri()],
                       capture_output=True, text=True, timeout=120)
    ok = (OUT / destino).exists()
    print(destino, marca, tema, "OK" if ok else "FALLO: " + r.stderr[-200:])

# El login del demo centra el formulario: queda una franja vacía de ~390 px entre la
# navbar (y 0-70) y el form (y 430-950). Se corta y se solda: la tarjeta del tríptico
# se ve llena en vez de un tercio blanco.
from PIL import Image
lp = OUT / "login.png"
im = Image.open(lp)
rec = Image.new("RGB", (im.width, 70 + 575), "white")
rec.paste(im.crop((0, 0, im.width, 70)), (0, 0))
rec.paste(im.crop((0, 415, im.width, 990)), (0, 70))
rec.save(lp)
print("login recortado:", rec.size)
print("listo")
