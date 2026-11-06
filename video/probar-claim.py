#!/usr/bin/env python3
"""Prueba el claim con la config GL ganadora a t=6s."""
import subprocess

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=6000",
                    "--screenshot=/tmp/vq2/gl-6s.png",
                    "http://127.0.0.1:8641/00-three.html"],
                   capture_output=True, text=True, timeout=110)
print("salida", r.returncode)
