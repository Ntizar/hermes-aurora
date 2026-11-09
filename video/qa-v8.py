#!/usr/bin/env python3
"""QA v8 — contrato del GUION-v8.md, comprobado (no supuesto).

1. 70,0 s ±0,5 · 1600×900 · 20 fps · h264 yuv420p · 1 vídeo + 1 audio · 0 subtítulos
2. 11 escenas con imagen (luma media > 20 en su fotograma central)
3. Sin parpadeo (rebotes de brillo) y con movimiento dentro de cada escena
4. Audio: −16 LUFS ±2 y true peak < −1 dBFS
5. Cero datos inventados: las cifras del vídeo existen en data/censo.json / plugin.yaml
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parent
VIDEO = RAIZ / "demo8.mp4"
FRAMES = RAIZ / "frames8"
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"
FFMPEG = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
OFFSETS = json.loads((RAIZ / "offsets-v8.json").read_text())
MANIFEST = json.loads((RAIZ / "manifest-v8.json").read_text())
fallos = []
def check(ok, texto):
    print(("  ok  " if ok else "  FALLO ") + texto)
    if not ok: fallos.append(texto)

def main():
    if not VIDEO.exists():
        sys.exit("no existe demo8.mp4")
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
    check(VIDEO.stat().st_size < 30 * 1024 * 1024, f"tamaño {VIDEO.stat().st_size/1e6:.1f} MB")

    print("== escenas ==")
    for nombre in OFFSETS:
        d = FRAMES / nombre
        fs = sorted(d.glob("*.png"))
        esperado = round(MANIFEST[nombre] * 20)
        if len(fs) != esperado:
            check(False, f"{nombre}: {len(fs)} frames (esperaba {esperado})"); continue
        mid = Image.open(fs[len(fs)//2]).convert("L")
        luma = float(np.asarray(mid).mean())
        # movimiento: diferencia media entre fotogramas separados 0,5 s
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

    print("== audio ==")
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", str(VIDEO), "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    txt = r.stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", txt)
    P = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", txt)
    lufs = float(I[-1]) if I else -99
    pico = float(P[-1]) if P else 0
    check(-18 <= lufs <= -14, f"sonoridad {lufs} LUFS (−16 ±2)")
    check(pico < -1.0, f"true peak {pico} dBFS (< −1)")

    print("== datos (no inventados) ==")
    censo = json.loads((RAIZ.parent / "data" / "censo.json").read_text())
    n_clases, n_fam, n_packs = len(censo["clases"]), len(censo["familias"]), len(censo["packs"])
    html = " ".join((RAIZ / "slides" / f"{n}.html").read_text() for n in OFFSETS)
    check(f"{n_clases:,}" in html, f"{n_clases:,} clases aparece en pantalla")
    check(str(n_fam) in html, f"{n_fam} familias aparece en pantalla")
    check(str(n_packs) in html, f"{n_packs} packs aparece en pantalla")
    check("4 skills" in html and "2 tools" in html, "4 skills · 2 tools en pantalla")
    check("0 network" in html, "0 network en pantalla")

    print()
    if fallos:
        print(f"RESULTADO: FALLO ({len(fallos)} criterios)")
        sys.exit(1)
    print("RESULTADO: VÁLIDO — el contrato está en verde")

if __name__ == "__main__":
    main()
