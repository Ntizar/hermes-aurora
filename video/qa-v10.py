#!/usr/bin/env python3
"""QA v10 — contrato del GUION-v9.md, comprobado.

Además de contenedor/escenas/parpadeo:
  · SILENCIO real entre escenas (no hay música ni SFX): RMS < −60 dB en los huecos.
  · LOGO azul + naranja: el cierre no contiene los colores del arcoíris anterior.
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parent
VIDEO = RAIZ / "demo9.mp4"
FRAMES = RAIZ / "frames9"
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"
FFMPEG = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
OFFSETS = json.loads((RAIZ / "offsets-v9.json").read_text())
MANIFEST = json.loads((RAIZ / "manifest-v9.json").read_text())
fallos = []
def check(ok, texto):
    print(("  ok  " if ok else "  FALLO ") + texto)
    if not ok: fallos.append(texto)

def main():
    if not VIDEO.exists():
        sys.exit("no existe demo9.mp4")
    info = json.loads(subprocess.run([FFPROBE, "-v", "error", "-show_streams", "-show_format",
                                      "-of", "json", str(VIDEO)], capture_output=True, text=True).stdout)
    dur = float(info["format"]["duration"])
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in info["streams"] if s["codec_type"] == "audio"]
    subs = [s for s in info["streams"] if s["codec_type"] == "subtitle"]
    print("== contenedor ==")
    check(abs(dur - 70.0) <= 0.5, f"duración {dur:.2f}s (70,0 ±0,5)")
    check(v["width"] == 1600 and v["height"] == 900, f"resolución {v['width']}x{v['height']}")
    check(v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p", f"códec {v['codec_name']} {v.get('pix_fmt')}")
    check(v["r_frame_rate"] == "20/1", f"fps {v['r_frame_rate']}")
    check(len(a) == 1, f"{len(a)} stream(s) de audio")
    check(len(subs) == 0, f"{len(subs)} stream(s) de subtítulos")

    print("== escenas ==")
    for nombre in OFFSETS:
        fs = sorted((FRAMES / nombre).glob("*.png"))
        esperado = round(MANIFEST[nombre] * 20)
        if len(fs) != esperado:
            check(False, f"{nombre}: {len(fs)} frames (esperaba {esperado})"); continue
        luma = float(np.asarray(Image.open(fs[len(fs)//2]).convert("L")).mean())
        a0 = np.asarray(Image.open(fs[0]).convert("L").resize((200, 113)), dtype=np.float32)
        a1 = np.asarray(Image.open(fs[min(len(fs)-1, 10)]).convert("L").resize((200, 113)), dtype=np.float32)
        mov = float(np.abs(a1 - a0).mean())
        check(luma > 20 and mov > 0.4, f"{nombre}: luma {luma:.0f} · movimiento {mov:.2f}")

    print("== parpadeo ==")
    for nombre in OFFSETS:
        fs = sorted((FRAMES / nombre).glob("*.png"))[::2]
        vals = [float(np.asarray(Image.open(f).convert("L").resize((100, 57))).mean()) for f in fs]
        rebotes = 0
        for i in range(len(vals) - 1):
            if abs(vals[i+1] - vals[i]) <= 8: continue
            for j in range(i + 2, min(i + 9, len(vals))):
                if abs(vals[j] - vals[i]) < 8 and abs(vals[i+1] - vals[i]) > 16:
                    rebotes += 1; break
        check(rebotes == 0, f"{nombre}: {rebotes} rebotes")

    print("== audio (solo voz) ==")
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", str(VIDEO), "-ac", "1", "-ar", "48000",
                          "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    silencios = [(3.0, 3.85), (9.55, 9.75), (41.05, 41.30)]
    for a0, a1 in silencios:
        seg = x[int(a0*48000):int(a1*48000)]
        rms = 20*np.log10(np.sqrt((seg**2).mean())+1e-12)
        check(rms < -60, f"silencio {a0:.1f}-{a1:.1f}s: {rms:.0f} dB")
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", str(VIDEO), "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    P = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    check(-18 <= float(I[-1]) <= -14, f"sonoridad {I[-1]} LUFS (−16 ±2)")
    check(float(P[-1]) < -1.0, f"true peak {P[-1]} dBFS (< −1)")

    print("== logo y datos ==")
    html10 = (RAIZ / "slides" / "10-cierre.html").read_text()
    check("#3a7aff" in html10 and "#ff6a00" in html10, "cierre con azul #3a7aff y naranja #ff6a00")
    check("#6261ff" not in html10 and "#a78bfa" not in html10, "sin letras arcoíris en el wordmark")
    censo = json.loads((RAIZ.parent / "data" / "censo.json").read_text())
    check(f"{len(censo['clases']):,}" in (RAIZ/"slides"/"03-llano.html").read_text(), "2,223 en el catálogo")
    check("4 skills" in html10 and "2 tools" in html10 and "0 network" in html10, "4 skills · 2 tools · 0 network")

    print()
    if fallos:
        print(f"RESULTADO: FALLO ({len(fallos)} criterios)"); sys.exit(1)
    print("RESULTADO: VÁLIDO — el contrato está en verde")

if __name__ == "__main__":
    main()
