#!/usr/bin/env python3
"""07-limpio y 08-dark aún negros: quita también .ken (la otra animación sobre <img>)
y cualquier .nz-reveal residual que envuelva imágenes. Test A/B del .ken solo."""
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
from PIL import Image

for nombre in ["07-limpio", "08-dark"]:
    f = SLIDES / (nombre + ".html")
    src = f.read_text()
    src = src.replace(' class="shot-wrap ken" data-reveal', ' class="shot-wrap" data-reveal')
    f.write_text(src)
    out = "/tmp/vq2/noke-%s.png" % nombre
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader", "--window-size=1600,900",
                    "--hide-scrollbars", "--virtual-time-budget=3000", "--screenshot=" + out,
                    f.resolve().as_uri()], capture_output=True, timeout=110)
    img = Image.open(out).convert("L"); px = list(img.getdata())
    print(nombre, round(sum(px) / len(px), 1))
