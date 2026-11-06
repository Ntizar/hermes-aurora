#!/usr/bin/env python3
"""Monta el vídeo v5 (10 escenas) → demo5-sin-subtitulos.mp4."""
import json, subprocess, sys
from pathlib import Path

FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
RAIZ = Path(__file__).resolve().parent
FRAMES = RAIZ / "frames5"
AUDIO = RAIZ / "audio4"   # mismas voces salvo 00-three (sin voz: intro instrumental muda)
SEG = RAIZ / "segments5"
FPS = 20
MANIFEST = json.loads((RAIZ / "manifest-v5.json").read_text())

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:], file=sys.stderr); sys.exit(1)

def main():
    SEG.mkdir(exist_ok=True)
    for i, (nombre, dur) in enumerate(MANIFEST.items(), 1):
        seg = SEG / ("seg%02d.mp4" % i)
        audio = AUDIO / (nombre + ".mp3")
        if audio.exists():
            filtros = "[1:a]adelay=200:all=1,apad[a]"
            mapa_a = "[a]"
        else:
            filtros = "anullsrc=channel_layout=mono:sample_rate=44100[a]"
            mapa_a = "[a]"
        cmd = [FF, "-y", "-v", "error",
               "-framerate", str(FPS), "-i", str(FRAMES / nombre / "%04d.png")]
        if audio.exists():
            cmd += ["-i", str(audio)]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100"]
        cmd += ["-filter_complex", filtros + ";[0:v]scale=1600:900,format=yuv420p[v]",
                "-map", "[v]", "-map", mapa_a, "-t", str(dur),
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-r", str(FPS),
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100", str(seg)]
        run(cmd)
        print("segmento", seg.name, dur)
    lista = RAIZ / "concat-v5.txt"
    lista.write_text("".join("file 'segments5/seg%02d.mp4'\n" % i
                             for i in range(1, len(MANIFEST) + 1)))
    run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
         "-c", "copy", str(RAIZ / "demo5-sin-subtitulos.mp4")])
    print("listo")

if __name__ == "__main__":
    main()
