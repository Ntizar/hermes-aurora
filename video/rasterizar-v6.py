#!/usr/bin/env python3
"""Rasterizador v6: 11 escenas. Las de <img> (05,07,08) llevan reveal calculado:
el script inyecta inline style opacity al shot-wrap según t (idéntico easing)."""
import json, math, re, shutil, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames5"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
FPS = 20
GL = ["--use-gl=angle", "--use-angle=swiftshader"]
MANIFEST = json.loads((RAIZ / "manifest-v5.json").read_text())
ORIGEN = {"00-three": "http://127.0.0.1:8641/00-three.html"}
REVEAL = {"05-trio": [0.25, 0.45, 0.65], "07-limpio": [0.4, 0.8], "08-dark": [0.5, 0.7]}

def capturar(nombre, dur):
    total = round(dur * FPS)
    destino = FRAMES / nombre
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)
    html = (SLIDES / (nombre + ".html")).read_text()
    wraps = html.count('class="shot-wrap"')
    delays = REVEAL.get(nombre, [])
    url = ORIGEN.get(nombre) or (SLIDES / (nombre + ".html")).resolve().as_uri()
    for i in range(total):
        t = round(i / FPS, 3)
        cuerpo = html
        if wraps and delays:
            for w, d in enumerate(delays):
                k = min(max((t - d) / 0.9, 0), 1)
                op = round(1 - math.pow(1 - k, 3), 3)
                cuerpo = cuerpo.replace('class="shot-wrap"',
                                        'class="shot-wrap" style="opacity:%s"' % op, 1)
        (SLIDES / (nombre + ".html")).write_text(cuerpo)
        # usar file:// siempre (con el css local, no hay red que compita)
        url_local = (SLIDES / (nombre + ".html")).resolve().as_uri()
        r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", *GL,
                            "--window-size=1600,900", "--hide-scrollbars",
                            "--virtual-time-budget=" + str(int(t * 1000) + 1),
                            "--screenshot=" + str(destino / ("%04d.png" % i)), url_local],
                           capture_output=True, text=True, timeout=90)
        if not (destino / ("%04d.png" % i)).exists():
            print("FALLO %s f%d: %s" % (nombre, i, r.stderr[:200]), file=sys.stderr); sys.exit(1)
    # restaurar el html base
    (SLIDES / (nombre + ".html")).write_text(html)
    print("ok", nombre, total)

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(MANIFEST)
    FRAMES.mkdir(exist_ok=True)
    for nombre in pedidos:
        capturar(nombre, MANIFEST[nombre])
