#!/usr/bin/env python3
"""Arregla los f-string con JS: convierte los 3 slides con <script> a cuerpos limpios."""
import re
from pathlib import Path

F = Path("/home/nan/Projects/hermes-aurora/video/slides-v3.py")
src = F.read_text()
for sid in ["04-buscar", "06-validar", "08-instalar"]:
    pat = re.compile(r'slides\["' + sid + r'"\] = \(("(?:dark|light)"), f"""\n(.*?)"""\)', re.S)
    m = pat.search(src)
    assert m, sid
    cuerpo = m.group(2).replace("{{", "{").replace("}}", "}")
    nuevo = f'slides["{sid}"] = ({m.group(1)}, """\n{cuerpo}""")'
    src = src[:m.start()] + nuevo + src[m.end():]
F.write_text(src)
import ast
ast.parse(src)
print("sintaxis ok")
