#!/usr/bin/env python3
"""Rasteriza el vídeo v5 (10 escenas): 00-three vía HTTP + 9 locales, 20 fps.
Uso: python3 rasterizar-v5.py [escena]   (sin argumento = todas)"""
import json, math, shutil, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames5"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
FPS = 20
GL = ["--use-gl=angle", "--use-angle=swiftshader"]
MANIFEST = json.loads((RAIZ / "manifest-v5.json").read_text())  # nombre → duración
ORIGEN = {"00-three": "http://127.0.0.1:8641/00-three.html"}

def capturar(nombre, total):
    destino = FRAMES / nombre
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)
    url = ORIGEN.get(nombre) or (SLIDES / (nombre + ".html")).resolve().as_uri()
    for i in range(total):
        t = round(i / FPS, 3)
        r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", *GL,
                            "--window-size=1600,900", "--hide-scrollbars",
                            "--virtual-time-budget=" + str(int(t * 1000) + 1),
                            "--screenshot=" + str(destino / ("%04d.png" % i)), url],
                           capture_output=True, text=True, timeout=90)
        if not (destino / ("%04d.png" % i)).exists():
            print("FALLO %s f%d: %s" % (nombre, i, r.stderr[:200]), file=sys.stderr); sys.exit(1)
    print("ok", nombre, total)

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(MANIFEST)
    FRAMES.mkdir(exist_ok=True)
    for nombre in pedidos:
        capturar(nombre, round(MANIFEST[nombre] * FPS))
