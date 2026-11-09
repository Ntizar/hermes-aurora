#!/usr/bin/env python3
"""Sonda v8 — captura fotogramas sueltos para revisar composición antes del render largo."""
import os, subprocess, sys
from pathlib import Path
import importlib.util as _u
_spec=_u.spec_from_file_location('r9', Path(__file__).with_name('rasterizar-v10.py'))
R=_u.module_from_spec(_spec); _spec.loader.exec_module(R)

OUT = Path(__file__).resolve().parent / "probe9"
OUT.mkdir(exist_ok=True)
CHROME = R.CHROME
LIBS = R.LIBS

CASOS = [
    ("00-open", 2.9), ("01-acabada", 3.8), ("02-inventa", 5.0), ("03-llano", 7.0),
    ("04-tecnico", 4.6), ("05-planos", 4.2), ("06-juez", 5.2), ("07-bucle", 4.2),
    ("08-tema", 3.2), ("09-receta", 5.0), ("10-cierre", 3.6),
]

def main():
    env = dict(os.environ, LD_LIBRARY_PATH=LIBS)
    for nombre, t in CASOS:
        html = OUT / f"_{nombre}.html"
        html.write_text(R.pagina(nombre, t), encoding="utf-8")
        png = OUT / f"{nombre}_{t}.png"
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                        "--window-size=1600,900", "--hide-scrollbars",
                        "--virtual-time-budget=2000", "--screenshot=" + str(png),
                        html.resolve().as_uri()], capture_output=True, text=True, env=env)
        print(png, png.stat().st_size if png.exists() else "FALLO")

if __name__ == "__main__":
    main()
