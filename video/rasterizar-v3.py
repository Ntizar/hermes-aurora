#!/usr/bin/env python3
"""Rasteriza las 8 slides v3 a fotogramas (20 fps). Animaciones todas arrancan en t=0."""
import subprocess, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames3"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
FPS = 20
DUR = {  # duración del audio (manifest.json) + holgura
    "01-beat1": 3.2, "02-beat2": 2.8, "03-nombre": 4.3, "04-buscar": 9.2,
    "05-pagina": 2.9, "06-validar": 7.6, "07-limpio": 3.4, "08-instalar": 5.4,
}

def main():
    if FRAMES.exists(): shutil.rmtree(FRAMES)
    FRAMES.mkdir()
    for nombre, dur in DUR.items():
        total = round(dur * FPS)
        destino = FRAMES / nombre
        destino.mkdir()
        html = (SLIDES / f"{nombre}.html").resolve()
        for i in range(total):
            t = round(i / FPS, 3)
            r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                                "--window-size=1600,900", "--hide-scrollbars",
                                f"--virtual-time-budget={int(t * 1000) + 1}",
                                f"--screenshot={destino / f'{i:04d}.png'}", html.as_uri()],
                               capture_output=True, text=True)
            if not (destino / f"{i:04d}.png").exists():
                print(f"FALLO {nombre} f{i}: {r.stderr[:200]}", file=sys.stderr); sys.exit(1)
        print(f"ok {nombre}: {total}")
    print("rasterizado completo")

if __name__ == "__main__":
    main()
