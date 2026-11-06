#!/usr/bin/env python3
"""08-dark: prueba A) sin CSS de Aurora, B) solo el head de 01 (que SÍ funciona)
con el body de 08. Aísla si el problema es el head o el body."""
import re
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"

body08 = re.search(r"<body[^>]*>(.*)</body>", (SLIDES / "08-dark.html").read_text(), re.S).group(1)
head01 = re.search(r"(.*</head>)", (SLIDES / "01-beat1.html").read_text(), re.S).group(1)
(SLIDES / "diag-08-head01.html").write_text(head01 + "\n<body class=\"nz\">\n" + body08 + "</body>\n</html>\n")

sin_aurora = re.sub(r"<link rel=\"stylesheet\" href=\"aurora-css/[^\"]*\">\n", "",
                    (SLIDES / "08-dark.html").read_text())
(SLIDES / "diag-08-noaurora.html").write_text(sin_aurora)

for nombre in ["diag-08-head01", "diag-08-noaurora"]:
    out = "/tmp/vq2/%s.png" % nombre
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000", "--screenshot=" + out,
                    (SLIDES / (nombre + ".html")).resolve().as_uri()],
                   capture_output=True, text=True, timeout=110)
    from PIL import Image
    img = Image.open(out).convert("L")
    px = list(img.getdata())
    print(nombre, round(sum(px) / len(px), 1))
