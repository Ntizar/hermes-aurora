#!/usr/bin/env python3
"""La imagen del dashboard mata el render: prueba SIN las imágenes, con divs color."""
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
s8 = (SLIDES / "08-dark.html").read_text()
head = s8.split("</head>")[0] + "</head>"
# igual que solo-imgs pero con bloques de color en vez de <img>
cuerpo = ('<div class="slide"><h1 class="beat nz-push" style="font-size:72px">Light and dark,<br>'
          '<span class="dim">both designed.</span></h1>'
          '<div class="half">'
          '<div class="shot-wrap ken nz-reveal" style="--d:.5s"><div class="shot" style="background:#f5f5f5"></div></div>'
          '<div class="shot-wrap ken nz-reveal" style="--d:.7s"><div class="shot" style="background:#16181d"></div></div>'
          '</div></div>')
(SLIDES / "diag-sinimg.html").write_text(head + "\n<body class=\"nz\">\n" + cuerpo + "\n</body>\n</html>\n")
out = "/tmp/vq2/sinimg.png"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                "--use-gl=angle", "--use-angle=swiftshader",
                "--window-size=1600,900", "--hide-scrollbars",
                "--virtual-time-budget=3000", "--screenshot=" + out,
                (SLIDES / "diag-sinimg.html").resolve().as_uri()],
               capture_output=True, timeout=110)
from PIL import Image
img = Image.open(out).convert("L")
px = list(img.getdata())
print("sin-imgs divs color:", round(sum(px) / len(px), 1))
