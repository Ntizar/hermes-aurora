#!/usr/bin/env python3
"""Monta el vídeo v7 portal de cristal (11 escenas, frames7 + audio5) → demo7.mp4."""
import json, subprocess, sys
from pathlib import Path

FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
RAIZ = Path(__file__).resolve().parent
FRAMES = RAIZ / "frames7"
AUDIO = RAIZ / "audio5"
SEG = RAIZ / "segments7"
FPS = 20
MANIFEST = json.loads((RAIZ / "manifest-v6.json").read_text())

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:], file=sys.stderr); sys.exit(1)

def main():
    SEG.mkdir(exist_ok=True)
    for i, (nombre, dur) in enumerate(MANIFEST.items(), 1):
        seg = SEG / ("seg%02d.mp4" % i)
        audio = AUDIO / (nombre + ".mp3")
        cmd = [FF, "-y", "-v", "error",
               "-framerate", str(FPS), "-i", str(FRAMES / nombre / "%04d.png")]
        if audio.exists():
            cmd += ["-i", str(audio)]
            filtros = "[1:a]adelay=200:all=1,apad[a]"
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100"]
            filtros = "[1:a]apad[a]"
        cmd += ["-filter_complex", filtros + ";[0:v]scale=1600:900,format=yuv420p[v]",
                "-map", "[v]", "-map", "[a]", "-t", str(dur),
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-r", str(FPS),
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100", str(seg)]
        run(cmd)
        print("segmento", seg.name, dur)
    lista = RAIZ / "concat-v7.txt"
    lista.write_text("".join("file 'segments7/seg%02d.mp4'\n" % i
                             for i in range(1, len(MANIFEST) + 1)))
    run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
         "-c", "copy", str(RAIZ / "demo7.mp4")])
    print("listo → demo7.mp4")

if __name__ == "__main__":
    main()
