#!/usr/bin/env python3
"""Compara 06-validar servido por HTTP vs file:// (mismo instante t=3 s)."""
import subprocess

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
SLIDES = "/home/nan/Projects/hermes-aurora/video/slides"
pruebas = [
    ("http", "http://127.0.0.1:8641/06-validar.html"),
    ("file", "file://" + SLIDES + "/06-validar.html"),
]
for nombre, url in pruebas:
    out = "/tmp/vq2/cmp-%s.png" % nombre
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000", "--screenshot=" + out, url],
                   capture_output=True, text=True, timeout=110)
    from PIL import Image
    img = Image.open(out).convert("L")
    px = list(img.getdata())
    print(nombre, "brillo:", round(sum(px) / len(px), 1))
