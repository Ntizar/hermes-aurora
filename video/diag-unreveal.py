#!/usr/bin/env python3
"""Script OK, eyebrow OK. El culpable solo puede ser data-reveal+JS: el JS pone
opacity a los shot-wrap CON <img>. Prueba el JS con un solo data-reveal."""
import re
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
from PIL import Image

base = (SLIDES / "diag-08-estatico.html").read_text()
orig = (SLIDES / "08-dark.html").read_text()
script_js = re.search(r"<script>.*?</script>", orig, re.S).group(0)
# data-reveal solo en el primer shot-wrap
v = base.replace('<div class="shot-wrap"><img class="shot" src="dashboard.png"',
                 '<div class="shot-wrap" data-reveal=".5"><img class="shot" src="dashboard.png"')
v = v.replace("</body>", script_js + "\n</body>")
f = SLIDES / "diag-unreveal.html"
f.write_text(v)
out = "/tmp/vq2/unreveal.png"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                "--use-gl=angle", "--use-angle=swiftshader", "--window-size=1600,900",
                "--hide-scrollbars", "--virtual-time-budget=3000", "--screenshot=" + out,
                f.resolve().as_uri()], capture_output=True, timeout=110)
img = Image.open(out).convert("L"); px = list(img.getdata())
print("un-reveal-js:", round(sum(px) / len(px), 1))
