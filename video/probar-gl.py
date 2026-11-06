#!/usr/bin/env python3
"""Prueba 3 configuraciones de GL para el canvas three.js y reporta brillo medio."""
import subprocess
from pathlib import Path

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
URL = "http://127.0.0.1:8641/00-three.html"
CONFIGS = [
    ["--use-gl=angle", "--use-angle=swiftshader"],
    ["--use-gl=swiftshader"],
    ["--enable-unsafe-swiftshader"],
]
for cfg in CONFIGS:
    out = "/tmp/vq2/gl-test.png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", *cfg,
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3500", "--screenshot=" + out, URL],
                   capture_output=True, text=True, timeout=90)
    try:
        from PIL import Image
        img = Image.open(out).convert("L")
        px = list(img.getdata())
        brillo = sum(px) / len(px)
        print(cfg, "brillo:", round(brillo, 1))
    except Exception as e:
        print(cfg, "fallo:", e)
