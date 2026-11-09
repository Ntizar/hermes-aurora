#!/usr/bin/env python3
"""QA v11 — demo light: 60 s, 1600x900, 20 fps, SIN pista de audio, 7 escenas."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parent
VIDEO = RAIZ / "demo11.mp4"
FRAMES = RAIZ / "frames11"
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"
OFFSETS = json.loads((RAIZ / "offsets-v11.json").read_text())
MANIFEST = json.loads((RAIZ / "manifest-v11.json").read_text())
fallos = []
def check(ok, t):
    print(("  ok  " if ok else "  FALLO ") + t)
    if not ok: fallos.append(t)

def main():
    info = json.loads(subprocess.run([FFPROBE, "-v", "error", "-show_streams", "-show_format",
                                      "-of", "json", str(VIDEO)], capture_output=True, text=True).stdout)
    dur = float(info["format"]["duration"])
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    aud = [s for s in info["streams"] if s["codec_type"] == "audio"]
    print("== contenedor ==")
    check(abs(dur - 60.0) <= 0.5, f"duración {dur:.2f}s (60 ±0,5)")
    check(v["width"] == 1600 and v["height"] == 900, f"{v['width']}x{v['height']}")
    check(v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p", f"{v['codec_name']} {v.get('pix_fmt')}")
    check(len(aud) == 0, f"{len(aud)} pista(s) de audio (debe ser 0)")
    print("== escenas ==")
    for n in OFFSETS:
        fs = sorted((FRAMES / n).glob("*.png"))
        esp = round(MANIFEST[n] * 20)
        if len(fs) != esp:
            check(False, f"{n}: {len(fs)}/{esp}"); continue
        luma = float(np.asarray(Image.open(fs[len(fs)//2]).convert("L")).mean())
        a0 = np.asarray(Image.open(fs[0]).convert("L").resize((200,113)), dtype=np.float32)
        a1 = np.asarray(Image.open(fs[min(len(fs)-1,10)]).convert("L").resize((200,113)), dtype=np.float32)
        mov = float(np.abs(a1-a0).mean())
        check(luma > 25 and mov > 0.4, f"{n}: luma {luma:.0f} · mov {mov:.2f}")
    print("== datos reales ==")
    sal = json.loads((RAIZ / "demo-v10" / "salidas.json").read_text())
    html = "".join((RAIZ / "slides11" / f"{n}.html").read_text() for n in OFFSETS)
    check(len(sal["rota"]["failures"]) == 4, "la página rota devuelve 4 fallos")
    check(sal["fija"]["ok"] is True, "la página corregida devuelve ok:true")
    for f in sal["rota"]["failures"]:
        frag = f.split(":")[0][:28]
        check(frag.lower() in html.lower(), f'fallo real en pantalla: "{frag}"')
    check("#0057ff" in html and "#ff6a00" in html, "azul + naranja")
    print()
    if fallos:
        print(f"RESULTADO: FALLO ({len(fallos)})"); sys.exit(1)
    print("RESULTADO: VÁLIDO")

if __name__ == "__main__":
    main()
