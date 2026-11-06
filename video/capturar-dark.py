#!/usr/bin/env python3
"""Recaptura dashboard.png y dashboard-dark.png (1440x1900) desde demo/dashboard.html."""
import shutil, subprocess
from pathlib import Path

DEMO = Path("/home/nan/Projects/hermes-aurora/demo")
TMP = Path("/tmp/vq2/dd")
SHOTS = Path("/home/nan/Projects/hermes-aurora/docs/screenshots")
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
DOCS = Path("/home/nan/Projects/hermes-aurora/docs")

TMP.mkdir(parents=True, exist_ok=True)
for f in DEMO.iterdir():
    if f.is_file():
        shutil.copy(f, TMP / f.name)
# CSS local si lo usa
if (DOCS / "index.html").exists() and not (TMP / "tokens.css").exists():
    pass  # el demo usa jsdelivr, sin assets locales

src = (DEMO / "dashboard.html").read_text()
(TMP / "dash-light.html").write_text(src)
(TMP / "dash-dark.html").write_text(src.replace('data-nz-theme="light"', 'data-nz-theme="dark"'))

for nombre, fichero in [("dashboard.png", "dash-light.html"), ("dashboard-dark.png", "dash-dark.html")]:
    out = f"/tmp/vq2/{nombre}"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--window-size=1440,1900", "--hide-scrollbars",
                    "--virtual-time-budget=4000", f"--screenshot={out}",
                    (TMP / fichero).as_uri()], capture_output=True, text=True)
    shutil.copy(out, SHOTS / nombre)
    from PIL import Image
    print(nombre, Image.open(out).size)
