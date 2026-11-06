#!/usr/bin/env python3
"""06-validar negro: descarta la fuente, prueba tokens SOLO (sin monocromo) y
una versión sin data-nz-marca. Tres variantes en paralelo."""
import subprocess
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
base = (SLIDES / "06-validar.html").read_text()

variantes = {
    "sin-marca": base.replace(' data-nz-marca="monocromo"', ""),
    "solo-tokens": base.replace('<link rel="stylesheet" href="aurora-css/marcas/monocromo.css">\n', ""),
    "sin-fontface": base,  # mismo html, pero servimos tokens.css sin @font-face
}
for nombre, cuerpo in variantes.items():
    (SLIDES / ("diag-%s.html" % nombre)).write_text(cuerpo)

# variante de css sin @font-face
tokens = (Path("/home/nan/Projects/Aurora/tokens.css")).read_text()
import re
tokens_sin = re.sub(r"@font-face\s*\{[^}]*\}", "/* font-face fuera */", tokens)
import shutil
TMP = Path("/tmp/vq2/aurora-css-nofont")
if TMP.exists():
    shutil.rmtree(TMP)
shutil.copytree(SLIDES / "aurora-css", TMP)
(TMP / "tokens.css").write_text(tokens_sin)
shutil.copy(SLIDES / "diag-sin-fontface.html", TMP / "diag-sin-fontface.html")

from PIL import Image
for nombre, url in [
    ("sin-marca", SLIDES / "diag-sin-marca.html"),
    ("solo-tokens", SLIDES / "diag-solo-tokens.html"),
    ("sin-fontface", TMP / "diag-sin-fontface.html"),
]:
    out = "/tmp/vq2/d-%s.png" % nombre
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000", "--screenshot=" + out,
                    url.as_uri()], capture_output=True, text=True, timeout=110)
    img = Image.open(out).convert("L")
    px = list(img.getdata())
    print(nombre, "brillo:", round(sum(px) / len(px), 1))
