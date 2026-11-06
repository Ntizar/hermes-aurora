#!/usr/bin/env python3
"""Aísla: el body de 08 por partes (solo título / solo imágenes / ambos)."""
import re
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
s8 = (SLIDES / "08-dark.html").read_text()
head = s8.split("</head>")[0] + "</head>"
body = re.search(r"<body[^>]*>(.*)</body>", s8, re.S).group(1)

partes = {
    "solo-titulo": '<div class="slide"><h1 class="beat nz-push" style="font-size:72px">Light and dark,<br><span class="dim">both designed.</span></h1></div>',
    "solo-imgs": body.split("<div class=\"half\">")[0] + '<div class="half"><div class="shot-wrap ken nz-reveal" style="--d:.5s; --ken:5.4s"><img class="shot" src="dashboard.png"></div><div class="shot-wrap ken nz-reveal" style="--d:.7s; --ken:5.4s"><img class="shot" src="dashboard-dark.png"></div></div></div>',
}
for nombre, cuerpo in partes.items():
    (SLIDES / ("diag-%s.html" % nombre)).write_text(head + "\n<body class=\"nz\">\n" + cuerpo + "\n</body>\n</html>\n")
    out = "/tmp/vq2/%s.png" % nombre
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000", "--screenshot=" + out,
                    (SLIDES / ("diag-%s.html" % nombre)).resolve().as_uri()],
                   capture_output=True, timeout=110)
    from PIL import Image
    img = Image.open(out).convert("L")
    px = list(img.getdata())
    print(nombre, round(sum(px) / len(px), 1))
