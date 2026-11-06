#!/usr/bin/env python3
"""Sirve diag-sin-fontface con su CSS (el que SÍ funcionó) desde /tmp y compara
el brillo con 06-validar servida de slides/ — mismo HTML, otro directorio de assets."""
import subprocess
from pathlib import Path

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"

# 1) diag-sin-fontface.html referenciaba aurora-css/ relativo al /tmp/vq2/
#    (donde vive el CSS sin fonts). La version actual de slides/aurora-css
#    tiene el mismo CSS (font-face fuera). Prueba directa:
SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
out = "/tmp/vq2/re-test.png"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                "--use-gl=angle", "--use-angle=swiftshader",
                "--window-size=1600,900", "--hide-scrollbars",
                "--virtual-time-budget=3000", "--screenshot=" + out,
                (SLIDES / "diag-sin-fontface.html").as_uri()],
               capture_output=True, text=True, timeout=110)
from PIL import Image
img = Image.open(out).convert("L")
px = list(img.getdata())
print("diag-sin-fontface desde slides/:", round(sum(px) / len(px), 1))
# y el 06 actual por file://
out2 = "/tmp/vq2/re-test06.png"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                "--use-gl=angle", "--use-angle=swiftshader",
                "--window-size=1600,900", "--hide-scrollbars",
                "--virtual-time-budget=3000", "--screenshot=" + out2,
                (SLIDES / "06-validar.html").as_uri()],
               capture_output=True, text=True, timeout=110)
img = Image.open(out2).convert("L")
px = list(img.getdata())
print("06-validar desde slides/:", round(sum(px) / len(px), 1))
