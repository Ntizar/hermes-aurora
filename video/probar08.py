#!/usr/bin/env python3
"""08-dark por http y file:// — el único slide que sigue negro."""
import subprocess

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
pruebas = [
    ("http", "http://127.0.0.1:8641/08-dark.html"),
    ("file", "file:///home/nan/Projects/hermes-aurora/video/slides/08-dark.html"),
]
for nombre, url in pruebas:
    out = "/tmp/vq2/ocho-%s.png" % nombre
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000", "--screenshot=" + out, url],
                   capture_output=True, text=True, timeout=110)
    from PIL import Image
    img = Image.open(out).convert("L")
    px = list(img.getdata())
    print(nombre, round(sum(px) / len(px), 1))
