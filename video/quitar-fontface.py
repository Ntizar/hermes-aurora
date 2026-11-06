#!/usr/bin/env python3
"""Quita los @font-face de la copia local de tokens.css usada por las slides."""
import re
from pathlib import Path

f = Path("/home/nan/Projects/hermes-aurora/video/slides/aurora-css/tokens.css")
css = f.read_text()
css2, n = re.subn(r"@font-face\s*\{[^}]*\}", "/* fuente local fuera en el render de video */", css)
f.write_text(css2)
print("bloques font-face quitados:", n)
fuentes = Path("/home/nan/Projects/hermes-aurora/video/slides/aurora-css/fuentes")
if fuentes.exists():
    import shutil
    shutil.rmtree(fuentes)
    print("carpeta fuentes eliminada")
