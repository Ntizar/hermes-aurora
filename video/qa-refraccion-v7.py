#!/usr/bin/env python3
"""QA de refracción del v7: ¿los cristales refringen de verdad (desplazan) o solo difuminan?

Sonda: rayas saturadas de 100px + una LENTE con url(#lg) (feDisplacementMap scale 24) y un
panel con BLUR puro (mismo blur base 1.2px). Firma de la refracción: la frontera entre rayas
está ONDULADA — su x cambia fila a fila (desviación típica > 3 px). Un blur deja la frontera
RECTA (std ~0): si el test aprobara un blur, sería mentira.
Salida 0 si la lente ondula las fronteras (refringe).
"""
import subprocess, sys
from statistics import pstdev
from PIL import Image

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
URL = "file:///home/nan/Projects/hermes-aurora/video/slides/sonda-v7.html"
OUT = "/tmp/sonda-v7-qa.png"

subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                "--window-size=1600,900", "--hide-scrollbars",
                "--virtual-time-budget=1500", f"--screenshot={OUT}", URL],
               capture_output=True, text=True, timeout=60)
im = Image.open(OUT).convert("RGB")
px = im.load()

def x_frontera(x0, x1, y):
    """x del mayor salto horizontal de color en la fila y dentro de [x0,x1)."""
    prev = px[x0, y]
    mx, mxi = 0, None
    for x in range(x0 + 1, x1):
        cur = px[x, y]
        d = sum(abs(a - b) for a, b in zip(prev, cur))
        if d > mx:
            mx, mxi = d, x
        prev = cur
    return mxi if mx > 80 else None

def ondulacion(x0, x1):
    xs = [x for y in range(250, 640, 6) if (x := x_frontera(x0, x1, y)) is not None]
    return pstdev(xs), len(xs)

std_lente, n_l = ondulacion(450, 1150)      # dentro de la lente (fronteras 500..1100)
std_blur, n_b = ondulacion(1280, 1520)      # panel de blur puro (frontera a 1300/1400/1500)
print(f"lente: std de frontera = {std_lente:.2f}px ({n_l} filas)")
print(f"blur:  std de frontera = {std_blur:.2f}px ({n_b} filas)")
ok = std_lente > 3.0 and std_lente > std_blur * 3 and n_l > 30
print("RESULTADO:", "REFRINGE ✓ (las fronteras ondulan dentro del vidrio)" if ok
      else "NO refringe / sonda no distingue")
sys.exit(0 if ok else 1)
