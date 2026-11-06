#!/usr/bin/env python3
"""Monta el vídeo v4: segmentos + concat → demo4-sin-subtitulos.mp4."""
import json, subprocess, sys
from pathlib import Path

FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
RAIZ = Path(__file__).resolve().parent
FRAMES = RAIZ / "frames4"
AUDIO = RAIZ / "audio4"
SEG = RAIZ / "segments4"
FPS = 20
HOLGURA = {"01-beat1": 0.9, "02-beat2": 0.9, "03-nombre": 0.9, "04-buscar": 1.3,
           "05-trio": 1.7, "06-validar": 0.9, "07-limpio": 1.0, "08-dark": 1.0,
           "09-instalar": 1.0}
MANIFEST = json.loads((RAIZ / "manifest-v4.json").read_text())

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:], file=sys.stderr); sys.exit(1)

def main():
    SEG.mkdir(exist_ok=True)
    for i, (nombre, voz) in enumerate(MANIFEST.items(), 1):
        dur = round(voz + HOLGURA.get(nombre, 1.0), 2)
        seg = SEG / ("seg%02d.mp4" % i)
        run([FF, "-y", "-v", "error",
             "-framerate", str(FPS), "-i", str(FRAMES / nombre / "%04d.png"),
             "-i", str(AUDIO / (nombre + ".mp3")),
             "-filter_complex", "[1:a]adelay=200:all=1,apad[a]",
             "-map", "0:v", "-map", "[a]", "-t", str(dur),
             "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-pix_fmt", "yuv420p", "-r", str(FPS),
             "-c:a", "aac", "-b:a", "128k", "-ar", "44100", str(seg)])
        print("segmento", seg.name, dur)
    lista = RAIZ / "concat-v4.txt"
    lista.write_text("".join("file 'segments4/seg%02d.mp4'\n" % i
                             for i in range(1, len(MANIFEST) + 1)))
    run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
         "-c", "copy", str(RAIZ / "demo4-sin-subtitulos.mp4")])
    print("listo")

if __name__ == "__main__":
    main()
