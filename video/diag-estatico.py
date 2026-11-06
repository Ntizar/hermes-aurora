#!/usr/bin/env python3
"""08-dark sigue negro. Aísla el body pelado CON el head propio pero SIN script ni data-reveal,
ni eyebrow nz-reveal. Todo estático."""
import re
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
from PIL import Image

src = (SLIDES / "08-dark.html").read_text()
# 1) sin eyebrow (única nz-reveal restante sobre texto)
# 2) sin script
# 3) shot-wrap sin data-reveal (estático, opacidad 1)
estatico = src.replace('<span class="eyebrow nz-reveal" style="--d:.1s">same markup · one attribute</span>',
                       '<span class="eyebrow">same markup · one attribute</span>')
estatico = re.sub(r'<script>.*?</script>', '', estatico, flags=re.S)
estatico = estatico.replace(' data-reveal=".5"', '').replace(' data-reveal=".7"', '')
(SLIDES / "diag-08-estatico.html").write_text(estatico)
out = "/tmp/vq2/estatico08.png"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                "--use-gl=angle", "--use-angle=swiftshader", "--window-size=1600,900",
                "--hide-scrollbars", "--virtual-time-budget=3000", "--screenshot=" + out,
                (SLIDES / "diag-08-estatico.html").resolve().as_uri()],
               capture_output=True, timeout=110)
img = Image.open(out).convert("L"); px = list(img.getdata())
print("estatico:", round(sum(px) / len(px), 1))
