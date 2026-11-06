#!/usr/bin/env python3
"""Misterio 08: head=01 (pinta) + body=08 (no pinta) daba 0. Probamos
body de 08 CON head de 01 otra vez pero capturado SIN virtual-time (solo sleep interno
no existe en headless; usar --run-all-compositor-stages-before-draw)."""
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
out = "/tmp/vq2/ocho-full.png"
r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=4000",
                    "--run-all-compositor-stages-before-draw",
                    "--screenshot=" + out,
                    (SLIDES / "08-dark.html").resolve().as_uri()],
                   capture_output=True, timeout=110)
from PIL import Image
img = Image.open(out).convert("L")
px = list(img.getdata())
print("con compositor stages:", round(sum(px) / len(px), 1))
