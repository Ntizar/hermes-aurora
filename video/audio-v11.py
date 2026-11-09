#!/usr/bin/env python3
"""Audio v11 — pega la narración sobre la demo muda y remuxea sin tocar el vídeo."""
import json, subprocess, wave
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parent
FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
AUDIO = RAIZ / "audio11"
TMP = RAIZ / "tmp11"; TMP.mkdir(exist_ok=True)
OFFSETS = json.loads((RAIZ / "offsets-v11.json").read_text())
SR, TOTAL, LEAD = 48000, 60.0, 0.35

def decodifica(mp3, wav):
    subprocess.run([FF, "-y", "-v", "error", "-i", str(mp3), "-ar", str(SR), "-ac", "1",
                    "-c:a", "pcm_s16le", str(wav)], check=True)

def lee(p):
    with wave.open(str(p), "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768

def main():
    pista = np.zeros(int(SR * TOTAL), dtype=np.float32)
    for nombre, t0 in OFFSETS.items():
        decodifica(AUDIO / f"{nombre}.mp3", TMP / f"{nombre}.wav")
        x = lee(TMP / f"{nombre}.wav")
        i0 = int((t0 + LEAD) * SR)
        n = min(len(x), len(pista) - i0)
        x = x[:n]
        f = min(int(0.012 * SR), n // 2)
        if f:
            x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        pista[i0:i0+n] += x
    pista = pista / (np.abs(pista).max() or 1) * 0.89
    crudo = TMP / "voz11.wav"
    with wave.open(str(crudo), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((pista * 32767).astype(np.int16).tobytes())
    norm = TMP / "voz11_norm.wav"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(crudo), "-af",
                    "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2",
                    "-c:a", "pcm_s16le", str(norm)], check=True)
    mudo = RAIZ / "demo11-mudo.mp4"
    if not mudo.exists():
        (RAIZ / "demo11.mp4").rename(mudo)
    subprocess.run([FF, "-y", "-v", "error", "-i", str(mudo), "-i", str(norm),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-af", "afade=t=out:st=58.6:d=1.4", "-shortest", "-movflags", "+faststart",
                    str(RAIZ / "demo11.mp4")], check=True)
    print("listo → demo11.mp4 con voz")

if __name__ == "__main__":
    main()
