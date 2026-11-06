#!/usr/bin/env python3
"""08-dark mínimo: SOLO las dos <img> en un body pelado (sin slide, sin nz-reveal)."""
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>body{background:#111;margin:0}</style></head>
<body><img src="dashboard.png" width="800"><img src="dashboard-dark.png" width="800"></body></html>
"""
(SLIDES / "diag-img-pelado.html").write_text(html)
out = "/tmp/vq2/img-pelado.png"
r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000", "--screenshot=" + out,
                    (SLIDES / "diag-img-pelado.html").resolve().as_uri()],
                   capture_output=True, timeout=110)
from PIL import Image
img = Image.open(out).convert("L")
px = list(img.getdata())
print("imgs peladas:", round(sum(px) / len(px), 1))
# y con cada png sola
for png in ["dashboard.png", "dashboard-dark.png"]:
    html2 = html.replace('src="dashboard.png" width="800"><img src="dashboard-dark.png" width="800"',
                         'src="%s" width="800"' % png)
    (SLIDES / "diag-una.html").write_text(html2)
    out2 = "/tmp/vq2/una-%s.png" % png.replace(".png", "")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000", "--screenshot=" + out2,
                    (SLIDES / "diag-una.html").resolve().as_uri()],
                   capture_output=True, timeout=110)
    img = Image.open(out2).convert("L")
    px = list(img.getdata())
    print(png, round(sum(px) / len(px), 1))
