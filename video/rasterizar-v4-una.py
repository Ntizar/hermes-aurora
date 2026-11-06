#!/usr/bin/env python3
"""Rasteriza UNA escena v4: python3 rasterizar-v4-una.py 04-buscar"""
import json, shutil, sys
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames4"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
FPS = 20
HOLGURA = {"01-beat1": 0.9, "02-beat2": 0.9, "03-nombre": 0.9, "04-buscar": 1.3,
           "05-trio": 1.7, "06-validar": 0.9, "07-limpio": 1.0, "08-dark": 1.0,
           "09-instalar": 1.0}
MANIFEST = json.loads((RAIZ / "manifest-v4.json").read_text())

nombre = sys.argv[1]
dur = round(MANIFEST[nombre] + HOLGURA.get(nombre, 1.0), 2)
total = round(dur * FPS)
destino = FRAMES / nombre
shutil.rmtree(destino, ignore_errors=True)
destino.mkdir(parents=True)
html = (SLIDES / (nombre + ".html")).resolve()
for i in range(total):
    t = round(i / FPS, 3)
    r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                        "--window-size=1600,900", "--hide-scrollbars",
                        "--virtual-time-budget=" + str(int(t * 1000) + 1),
                        "--screenshot=" + str(destino / ("%04d.png" % i)), html.as_uri()],
                       capture_output=True, text=True)
    if not (destino / ("%04d.png" % i)).exists():
        print("FALLO f%d: %s" % (i, r.stderr[:200]), file=sys.stderr); sys.exit(1)
print("ok", nombre, total)
