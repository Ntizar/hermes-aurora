#!/usr/bin/env python3
"""Captura 08-dark y mide brillo (la prueba definitiva del fix de fuentes)."""
import subprocess

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000",
                    "--screenshot=/tmp/vq2/m08-new.png",
                    "http://127.0.0.1:8641/08-dark.html"],
                   capture_output=True, text=True, timeout=110)
from PIL import Image
img = Image.open("/tmp/vq2/m08-new.png").convert("L")
px = list(img.getdata())
print("brillo tras fuentes:", round(sum(px) / len(px), 1))
