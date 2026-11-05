#!/usr/bin/env python3
"""Rasteriza cada slide a una secuencia de PNG (30 fps) respetando el timeline
de CSS definido en cada HTML. Los fotogramas de un slide sin animación son el
último render repetido: ffmpeg los recibe como entrada de imagen."""
import subprocess, sys, shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames-dyn"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
FPS = 20

DUR = {  # segundos por slide (duración del audio + 0,5)
    "01-titulo": 5.1, "02-problema": 8.1, "03-buscar": 11.4,
    "04-pagina": 6.4, "05-validar": 11.4, "06-limpio": 7.6, "07-cierre": 7.2,
}
TL = {  # timeline de animación de cada slide (los HTML ya lo llevan)
    "01-titulo": 0.0, "02-problema": 5.5, "03-buscar": 7.5, "04-pagina": 4.5,
    "05-validar": 8.5, "06-limpio": 5.0, "07-cierre": 4.0,
}

def main():
    if FRAMES.exists(): shutil.rmtree(FRAMES)
    FRAMES.mkdir()
    for name, dur in DUR.items():
        total = round(dur * FPS)
        tl = TL[name]
        html = (SLIDES / f"{name}.html").resolve()
        destino = FRAMES / name
        destino.mkdir()
        for i in range(total):
            t = round(i / FPS + tl, 3)          # tiempo virtual: frame + desfase del timeline
            flag = f"--virtual-time-budget={int(t * 1000) + 1}"
            cmd = [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                   "--window-size=1600,900", "--hide-scrollbars", flag,
                   f"--screenshot={destino / f'{i:04d}.png'}",
                   html.as_uri()]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if not (destino / f"{i:04d}.png").exists():
                print(f"FALLO {name} f{i}: {r.stderr[:300]}", file=sys.stderr); sys.exit(1)
        print(f"ok {name}: {total} fotogramas")

if __name__ == "__main__":
    main()
