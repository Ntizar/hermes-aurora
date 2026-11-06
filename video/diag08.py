#!/usr/bin/env python3
"""Diagnóstico DOM de 08-dark: qué elemento queda visible a t=2,5 s."""
import subprocess

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
URL = "http://127.0.0.1:8641/08-dark.html"
r = subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=2500", "--dump-dom", URL],
                   capture_output=True, text=True, timeout=110)
dom = r.stdout
import re
# estilos inline del h1 y de los shot-wrap
for m in re.finditer(r'<(h1|div|img|p|span)[^>]*style="([^"]*)"[^>]*>', dom):
    print(m.group(1), "→", m.group(2)[:90])
print("---")
# estilos computados de Aurora: ¿.nz-push y .nz-reveal existen en los packs?
for pack in ["p1-layout", "p3-typography", "p4-actions", "p6-feedback", "p8-data"]:
    css = open("/home/nan/Projects/hermes-aurora/video/slides/aurora-css/packs/%s.css" % pack).read()
    if "nz-push" in css or "nz-reveal" in css:
        print(pack, "DEFINE las clases de animación")
