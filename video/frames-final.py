#!/usr/bin/env python3
"""Fotogramas del vídeo final con subtítulos trilingües para revisión visual."""
import subprocess

FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
V = "/home/nan/Projects/hermes-aurora/video/demo5-final.mp4"
for t in [7, 13, 25, 40, 50]:
    subprocess.run([FF, "-y", "-v", "error", "-ss", str(t), "-i", V,
                    "-frames:v", "1", "/tmp/vq2/final%d.png" % t], timeout=60)
print("fotogramas listos")
