#!/usr/bin/env python3
"""Re-rasteriza UNA escena: python3 rasterizar-una.py 07-cierre"""
import subprocess, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames-dyn"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
FPS = 20
DUR = {"01-titulo": 5.1, "02-problema": 8.1, "03-buscar": 11.4, "04-pagina": 6.4,
       "05-validar": 11.4, "06-limpio": 7.6, "07-cierre": 7.2}
TL = {"01-titulo": 0.0, "02-problema": 5.5, "03-buscar": 7.5, "04-pagina": 4.5,
      "05-validar": 8.5, "06-limpio": 5.0, "07-cierre": 4.0}

nombre = sys.argv[1]
total = round(DUR[nombre] * FPS)
tl = TL[nombre]
destino = FRAMES / nombre
shutil.rmtree(destino, ignore_errors=True)
destino.mkdir(parents=True)
html = (SLIDES / f"{nombre}.html").resolve()
for i in range(total):
    t = round(i / FPS + tl, 3)
    r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                        "--window-size=1600,900", "--hide-scrollbars",
                        f"--virtual-time-budget={int(t * 1000) + 1}",
                        f"--screenshot={destino / f'{i:04d}.png'}", html.as_uri()],
                       capture_output=True, text=True)
    if not (destino / f"{i:04d}.png").exists():
        print(f"FALLO f{i}: {r.stderr[:200]}", file=sys.stderr); sys.exit(1)
print(f"ok {nombre}: {total} fotogramas")
