#!/usr/bin/env python3
"""Montaje v11 — demo light, 60 s, SIN audio (el vídeo no lleva pista de sonido).

Escenas de frames11/ → segmentos x264 → concat → demo11.mp4 (vídeo solo).
"""
import json, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FRAMES = RAIZ / "frames11"
TMP = RAIZ / "tmp11"
FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
MANIFEST = json.loads((RAIZ / "manifest-v11.json").read_text())
OFFSETS = json.loads((RAIZ / "offsets-v11.json").read_text())

def video():
    SEG = TMP / "seg"; SEG.mkdir(parents=True, exist_ok=True)
    ultimo = list(OFFSETS)[-1]
    i = 0
    for nombre in OFFSETS:
        dur = MANIFEST[nombre]; i += 1
        sale = SEG / f"seg{i:02d}.mp4"
        n = len(list((FRAMES / nombre).glob("*.png")))
        esperado = round(dur * 20)
        if n != esperado:
            sys.exit(f"{nombre}: {n} frames, esperaba {esperado}")
        vf = "scale=1600:900,format=yuv420p"
        if nombre == ultimo:
            vf += f",fade=t=out:st={dur-1.0}:d=1.0"
        subprocess.run([FF, "-y", "-v", "error", "-framerate", "20",
                        "-i", str(FRAMES / nombre / "%04d.png"), "-vf", vf,
                        "-t", str(dur), "-c:v", "libx264", "-preset", "medium",
                        "-crf", "19", "-pix_fmt", "yuv420p", "-r", "20", str(sale)], check=True)
        print("segmento", sale.name, dur)
    lista = TMP / "concat.txt"
    lista.write_text("".join(f"file 'seg/seg{i:02d}.mp4'\n" for i in range(1, i + 1)))
    final = RAIZ / "demo11.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", "-movflags", "+faststart", str(final)], check=True)
    print("listo →", final)

if __name__ == "__main__":
    video()
