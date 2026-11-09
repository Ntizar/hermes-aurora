#!/usr/bin/env python3
"""Montaje v8 — frames8 + voz + cama → demo8.mp4 (70,0 s).

· Voz: cada línea entra 0,30 s después del corte de su escena (la 00 lleva la voz de máquina).
· Música: cama sintetizada, con DUCKING por envolvente de voz (−9 dB bajo la narración).
· Vídeo: un segmento por escena (20 fps) → concat → fundido final → AAC 192k.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parent
FRAMES = RAIZ / "frames8"
AUDIO = RAIZ / "audio8"
TMP = RAIZ / "tmp8"
FF = "/home/nan/Projects/subtitulador-brutal/bin/ffmpeg"
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"
MANIFEST = json.loads((RAIZ / "manifest-v8.json").read_text())
OFFSETS = json.loads((RAIZ / "offsets-v8.json").read_text())
SR = 48000
TOTAL = 70.0

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
        if not mp3.exists() and nombre == "00-open":
            mp3 = AUDIO / "00-three.mp3"
        wav = TMP / f"{nombre}.wav"
        decodifica(mp3, wav)
        x = lee_wav(wav)
        if nombre == "00-open":
            # voz de máquina: banda estrecha, como un altavoz
            X = np.fft.rfft(x)
            fr = np.fft.rfftfreq(len(x), 1 / SR)
            m = np.ones_like(fr)
            m[fr < 420] = np.clip(fr[fr < 420] / 420, 0, 1)
            m[fr > 3000] = np.clip(1 - (fr[fr > 3000] - 3000) / 4000, 0, 1)
            x = np.fft.irfft(X * m, n=len(x)).astype(np.float32) * 0.9
            ini = 0.55
        else:
            ini = t0 + 0.20
        i0 = int(ini * SR)
        n = min(len(x), len(voz) - i0)
        x = x[:n]
        fade = min(int(0.012 * SR), n // 2)
        if fade:
            x[:fade] *= np.linspace(0, 1, fade)
            x[-fade:] *= np.linspace(1, 0, fade)
        voz[i0:i0 + n] += x
    # envolvente para ducking
    ventana = int(0.05 * SR)
    env = np.convolve(np.abs(voz), np.ones(ventana) / ventana, mode="same")
    p95 = np.percentile(env, 99.5) or 1
    env = np.clip(env / p95, 0, 1)
    env = np.convolve(env, np.ones(int(0.18 * SR)) / int(0.18 * SR), mode="same")
    duck = (1 - 0.62 * env).astype(np.float32)

    cama = lee_wav(AUDIO / "cama.wav")
    if len(cama) < len(voz):
        cama = np.pad(cama, (0, len(voz) - len(cama)))
    cama = cama[:len(voz)]
    mix = voz * 0.98 + cama * 0.42 * duck
    # fundido final de audio
    fin = int(1.6 * SR)
    mix[-fin:] *= np.linspace(1, 0, fin) ** 1.4
    pico = np.abs(mix).max() or 1
    mix = mix / pico * 0.89
    out = TMP / "mezcla.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    # loudness normalizada a −16 LUFS
    norm = TMP / "mezcla_norm.wav"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(out), "-af",
                    "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2",
                    "-c:a", "pcm_s16le", str(norm)], check=True)
    print("mezcla →", norm, "pico", round(float(np.abs(mix).max()), 3))

def video():
    SEG = TMP / "seg"
    SEG.mkdir(parents=True, exist_ok=True)
    i = 0
    for nombre in OFFSETS:  # orden real del film (00 → 10)
        dur = MANIFEST[nombre]
        i += 1
        sale = SEG / f"seg{i:02d}.mp4"
        n = len(list((FRAMES / nombre).glob("*.png")))
        esperado = round(dur * 20)
        if n != esperado:
            sys.exit(f"{nombre}: {n} frames, esperaba {esperado}")
        subprocess.run([FF, "-y", "-v", "error", "-framerate", "20",
                        "-i", str(FRAMES / nombre / "%04d.png"),
                        "-vf", "scale=1600:900,format=yuv420p" + (f",fade=t=out:st={dur-1.0}:d=1.0" if nombre == list(OFFSETS)[-1] else ""),
                        "-t", str(dur), "-c:v", "libx264", "-preset", "medium",
                        "-crf", "19", "-pix_fmt", "yuv420p", "-r", "20", str(sale)], check=True)
        print("segmento", sale.name, dur)
    lista = TMP / "concat.txt"
    lista.write_text("".join(f"file 'seg/seg{i:02d}.mp4'\n" for i in range(1, i + 1)))
    mudo = TMP / "video_mudo.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", str(mudo)], check=True)
    final = RAIZ / "demo8.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(mudo), "-i", str(TMP / "mezcla_norm.wav"),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-af", "afade=t=out:st=68.95:d=1.05", "-shortest", "-movflags", "+faststart",
                    str(final)], check=True)
    print("listo →", final)

if __name__ == "__main__":
    mezcla_audio()
    if "--solo-audio" not in sys.argv:
        video()
