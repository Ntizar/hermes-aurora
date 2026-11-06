#!/usr/bin/env python3
"""08-dark completo PERO con img de altura fija distinta: sospecha de object-fit +
ken + reveal sobre <img> con PNG de 1440x1900 en contenedor de 520px de alto."""
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
s8 = (SLIDES / "08-dark.html").read_text()
head = s8.split("</head>")[0] + "</head>"
variantes = {
    "sin-ken": s8.replace(" class=\"shot-wrap ken nz-reveal\"", " class=\"shot-wrap nz-reveal\""),
    "sin-reveal": s8.replace(" class=\"shot-wrap ken nz-reveal\"", " class=\"shot-wrap ken\""),
    "sin-ambos": s8.replace(" class=\"shot-wrap ken nz-reveal\"", " class=\"shot-wrap\""),
}
from PIL import Image
for nombre, cuerpo in variantes.items():
    f = SLIDES / ("diag08-%s.html" % nombre)
    f.write_text(cuerpo)
    out = "/tmp/vq2/%s.png" % nombre
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000", "--screenshot=" + out,
                    f.resolve().as_uri()], capture_output=True, timeout=110)
    img = Image.open(out).convert("L")
    px = list(img.getdata())
    print(nombre, round(sum(px) / len(px), 1))
