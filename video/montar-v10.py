#!/usr/bin/env python3
"""Montaje v9 — SOLO VOZ. Sin música, sin risers, sin impactos.

· Cada línea entra 0,15 s después del corte de su escena.
· Los huecos entre escenas son silencio digital (se comprueba en qa-v10).
· Voz normalizada a −16 LUFS; el vídeo lleva fade final de 1 s.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parent
FRAMES = RAIZ / "frames9"
AUDIO = RAIZ / "audio9"
TMP = RAIZ / "tmp9"
FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
MANIFEST = json.loads((RAIZ / "manifest-v9.json").read_text())
OFFSETS = json.loads((RAIZ / "offsets-v9.json").read_text())
SR = 48000
TOTAL = 70.0
LEAD = 0.15

def decodifica(mp3, wav):
    subprocess.run([FF, "-y", "-v", "error", "-i", str(mp3), "-ar", str(SR), "-ac", "1",
                    "-c:a", "pcm_s16le", str(wav)], check=True)

def lee_wav(p):
    with wave.open(str(p), "rb") as w:
        n = w.getnframes()
        d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2:
            d = d.reshape(-1, 2).mean(axis=1)
    return d

def mezcla_audio():
    TMP.mkdir(exist_ok=True)
    voz = np.zeros(int(SR * TOTAL), dtype=np.float32)
    for nombre, t0 in OFFSETS.items():
        mp3 = AUDIO / f"{nombre}.mp3"
        wav = TMP / f"{nombre}.wav"
        decodifica(mp3, wav)
        x = lee_wav(wav)
        if nombre == "00-open":
            X = np.fft.rfft(x)
            fr = np.fft.rfftfreq(len(x), 1 / SR)
            m = np.ones_like(fr)
            m[fr < 420] = np.clip(fr[fr < 420] / 420, 0, 1)
            m[fr > 3000] = np.clip(1 - (fr[fr > 3000] - 3000) / 4000, 0, 1)
            x = np.fft.irfft(X * m, n=len(x)).astype(np.float32) * 0.9
            ini = 0.45
        else:
            ini = t0 + LEAD
        i0 = int(ini * SR)
        n = min(len(x), len(voz) - i0)
        x = x[:n]
        fade = min(int(0.012 * SR), n // 2)
        if fade:
            x[:fade] *= np.linspace(0, 1, fade)
            x[-fade:] *= np.linspace(1, 0, fade)
        voz[i0:i0 + n] += x
    pico = np.abs(voz).max() or 1
    voz = voz / pico * 0.89
    out = TMP / "voz.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((voz * 32767).astype(np.int16).tobytes())
    norm = TMP / "voz_norm.wav"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(out), "-af",
                    "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2",
                    "-c:a", "pcm_s16le", str(norm)], check=True)
    print("voz →", norm, "pico", round(float(np.abs(voz).max()), 3))

def video():
    SEG = TMP / "seg"
    SEG.mkdir(parents=True, exist_ok=True)
    ultimo = list(OFFSETS)[-1]
    i = 0
    for nombre in OFFSETS:
        dur = MANIFEST[nombre]
        i += 1
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
    mudo = TMP / "video_mudo.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", str(mudo)], check=True)
    final = RAIZ / "demo9.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(mudo), "-i", str(TMP / "voz_norm.wav"),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", str(final)], check=True)
    print("listo →", final)

if __name__ == "__main__":
    mezcla_audio()
    if "--solo-audio" not in sys.argv:
        video()
