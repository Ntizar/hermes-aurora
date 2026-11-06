#!/usr/bin/env python3
"""Estático pinta (124). Añadimos piezas una a una: script / eyebrow / data-reveal."""
import re
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
from PIL import Image

base = (SLIDES / "diag-08-estatico.html").read_text()
script = re.search(r"\n?<script>.*?</script>", base, re.S)
# el estático quedó SIN script; lo sacamos del 08 original
orig = (SLIDES / "08-dark.html").read_text()
script_js = re.search(r"<script>.*?</script>", orig, re.S).group(0)

variantes = {
    "con-script": base.replace("</body>", script_js + "\n</body>"),
    "con-eyebrow-reveal": base.replace('<span class="eyebrow">same markup',
                                       '<span class="eyebrow nz-reveal" style="--d:.1s">same markup'),
}
for nombre, cuerpo in variantes.items():
    f = SLIDES / ("diag-%s.html" % nombre)
    f.write_text(cuerpo)
    out = "/tmp/vq2/%s.png" % nombre
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader", "--window-size=1600,900",
                    "--hide-scrollbars", "--virtual-time-budget=3000", "--screenshot=" + out,
                    f.resolve().as_uri()], capture_output=True, timeout=110)
    img = Image.open(out).convert("L"); px = list(img.getdata())
    print(nombre, round(sum(px) / len(px), 1))
