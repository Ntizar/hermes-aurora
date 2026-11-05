#!/usr/bin/env python3
"""Monta el vídeo demo: segmentos por escena (fotogramas dinámicos + audio) y concat.
Salida: video/demo-sin-subtitulos.mp4 y copia en docs/video/demo.mp4 para la web."""
import subprocess, sys
from pathlib import Path

FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
RAIZ = Path(__file__).resolve().parent
DYN = RAIZ / "frames-dyn"
AUDIO = RAIZ / "audio"
SEG = RAIZ / "segments"
FPS = 20

ESCENAS = [  # (carpeta, audio, duración — MISMA que rasterizar.py)
    ("01-titulo", "01.mp3", 5.1), ("02-problema", "02.mp3", 8.1),
    ("03-buscar", "03.mp3", 11.4), ("04-pagina", "04.mp3", 6.4),
    ("05-validar", "05.mp3", 11.4), ("06-limpio", "06.mp3", 7.6),
    ("07-cierre", "07.mp3", 7.2),
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:], file=sys.stderr); sys.exit(1)

def main():
    SEG.mkdir(exist_ok=True)
    for i, (carpeta, audio, dur) in enumerate(ESCENAS, 1):
        seg = SEG / f"seg{i:02d}.mp4"
        cmd = [FF, "-y", "-v", "error",
               "-framerate", str(FPS), "-i", str(DYN / carpeta / "%04d.png"),
               "-i", str(AUDIO / audio),
               "-filter_complex",
               "[1:a]adelay=250:all=1,apad[a]",
               "-map", "0:v", "-map", "[a]", "-t", str(dur),
               "-c:v", "libx264", "-preset", "medium", "-crf", "20",
               "-pix_fmt", "yuv420p", "-r", str(FPS),
               "-c:a", "aac", "-b:a", "128k", "-ar", "44100", str(seg)]
        run(cmd)
        print("segmento", seg.name)
    lista = RAIZ / "concat-dyn.txt"
    lista.write_text("".join(f"file 'segments/seg{i:02d}.mp4'\n" for i in range(1, len(ESCENAS) + 1)))
    salida = RAIZ / "demo-sin-subtitulos.mp4"
    run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
         "-c", "copy", str(salida)])
    (RAIZ.parent / "docs" / "video").mkdir(exist_ok=True)
    print("listo:", salida)

if __name__ == "__main__":
    main()
