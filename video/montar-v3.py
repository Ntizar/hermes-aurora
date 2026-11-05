#!/usr/bin/env python3
"""Monta el vídeo v3: segmentos por escena + concat → demo3-sin-subtitulos.mp4."""
import subprocess, sys
from pathlib import Path

FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
RAIZ = Path(__file__).resolve().parent
FRAMES = RAIZ / "frames3"
AUDIO = RAIZ / "audio3"
SEG = RAIZ / "segments3"
FPS = 20
ESCENAS = [
    ("01-beat1", 3.2), ("02-beat2", 2.8), ("03-nombre", 4.3), ("04-buscar", 9.2),
    ("05-pagina", 2.9), ("06-validar", 7.6), ("07-limpio", 3.4), ("08-instalar", 5.4),
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:], file=sys.stderr); sys.exit(1)

def main():
    SEG.mkdir(exist_ok=True)
    for i, (carpeta, dur) in enumerate(ESCENAS, 1):
        seg = SEG / f"seg{i:02d}.mp4"
        run([FF, "-y", "-v", "error",
             "-framerate", str(FPS), "-i", str(FRAMES / carpeta / "%04d.png"),
             "-i", str(AUDIO / f"{carpeta}.mp3"),
             "-filter_complex", "[1:a]adelay=200:all=1,apad[a]",
             "-map", "0:v", "-map", "[a]", "-t", str(dur),
             "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-pix_fmt", "yuv420p", "-r", str(FPS),
             "-c:a", "aac", "-b:a", "128k", "-ar", "44100", str(seg)])
        print("segmento", seg.name)
    lista = RAIZ / "concat-v3.txt"
    lista.write_text("".join(f"file 'segments3/seg{i:02d}.mp4'\n" for i in range(1, len(ESCENAS) + 1)))
    run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
         "-c", "copy", str(RAIZ / "demo3-sin-subtitulos.mp4")])
    print("listo")

if __name__ == "__main__":
    main()
