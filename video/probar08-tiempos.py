#!/usr/bin/env python3
"""08-dark: capturas con distintos virtual-time (0.5s, 2s, 3s) + PNG de un solo color?
Diagnóstico del negro: quizá el <style> con .trio/.half roto anula el render."""
import subprocess

CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
URL = "http://127.0.0.1:8641/08-dark.html"
for t in [500, 2000, 3000]:
    out = "/tmp/vq2/ocho-t%d.png" % t
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--use-gl=angle", "--use-angle=swiftshader",
                    "--window-size=1600,900", "--hide-scrollbars",
                    "--virtual-time-budget=%d" % t, "--screenshot=" + out, URL],
                   capture_output=True, text=True, timeout=110)
    from PIL import Image
    img = Image.open(out)
    colores = img.convert("RGB").getcolors(1600 * 900)
    print("t=%d brillo=%.1f colores_unicos=%d" % (
        t, sum(c * v for c, v in [(cnt, px[0]) for cnt, px in [(n, (0, 0, 0))] for n in []]) if False else 0,
        len(colores) if colores else 99999))
    # brillo simple
    g = img.convert("L")
    px = list(g.getdata())
    print("   brillo:", round(sum(px) / len(px), 1))
