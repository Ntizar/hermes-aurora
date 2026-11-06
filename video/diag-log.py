#!/usr/bin/env python3
"""08-dark negro: consola del navegador (dump-dom no muestra errores JS; usar devtools via --enable-logging y -v=1)."""
import subprocess

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=3000",
                    "--enable-logging=stderr", "--v=1",
                    "--screenshot=/tmp/vq2/m08-log.png",
                    "http://127.0.0.1:8641/08-dark.html"],
                   capture_output=True, text=True, timeout=110)
lineas = [l for l in r.stderr.splitlines()
          if "CONSOLE" in l or "stylesheet" in l.lower() or "css" in l.lower()]
for l in lineas[:12]:
    print(l[:200])
print("total lineas stderr:", len(r.stderr.splitlines()))
