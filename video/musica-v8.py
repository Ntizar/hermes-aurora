#!/usr/bin/env python3
"""Música v8 — cama cinematográfica + SFX, sintetizada con numpy (sin samples, sin licencias).

70,0 s a 100 BPM. Un acorde cada 2,4 s; la energía sigue los actos del guion.
Salida: audio8/cama.wav (48 kHz, estéreo, 16 bit) — el montaje la mezcla con ducking.
"""
import wave
from pathlib import Path
import numpy as np

SR = 48000
DUR = 70.0
N = int(SR * DUR)
t = np.arange(N) / SR
RAIZ = Path(__file__).resolve().parent
OUT = RAIZ / "audio8" / "cama.wav"

def f(m):
    return 440.0 * 2 ** ((m - 69) / 12)

AC = {
    "Am": [45, 57, 60, 64], "F": [41, 57, 60, 65], "C": [48, 55, 60, 64],
    "G": [43, 55, 59, 62], "Dm": [38, 57, 62, 65], "E": [40, 56, 59, 64],
    "A": [45, 57, 61, 64, 69], "Bb": [46, 58, 62, 65],
}
# (inicio, acorde, energía 0-1)
PLAN = [
    (0.0, "Am", .45), (3.8, "Am", .60), (6.2, "C", .65),
    (10.4, "Dm", .60), (13.9, "E", .60),
    (17.7, "F", .68), (20.6, "C", .70),
    (23.5, "Am", .70), (27.3, "F", .72),
    (31.15, "C", .75), (34.3, "G", .74),
    (37.4, "Dm", .72), (41.2, "E", .78),
    (44.95, "F", .80), (48.6, "C", .80),
    (52.4, "Am", .72), (55.8, "G", .74),
    (59.35, "F", .82), (62.3, "G", .85),
    (65.35, "A", .95),
]
FIN = 70.0

def envolvente(t0, t1, atk=0.45, rel=0.7):
    e = np.zeros(N, dtype=np.float32)
    i0, i1 = int(t0 * SR), min(int(t1 * SR), N)
    seg = np.ones(i1 - i0, dtype=np.float32)
    na, nr = min(int(atk * SR), len(seg)), min(int(rel * SR), len(seg))
    if na: seg[:na] = np.linspace(0, 1, na) ** 1.5
    if nr: seg[-nr:] *= np.linspace(1, 0, nr) ** 1.2
    e[i0:i1] = seg
    return e

def pad_nota(midi, env, e, detune=0.0012):
    base = f(midi)
    x = np.zeros(N, dtype=np.float32)
    for h in range(1, 6):
        amp = 1.0 / (h ** 1.7)
        x += (np.sin(2*np.pi*base*h*t) * amp).astype(np.float32)
        x += (np.sin(2*np.pi*base*h*(1+detune)*t + h) * amp * 0.5).astype(np.float32)
    return x * env * (0.030 * e)

def filtro_fft(x, lo=32, hi=5200):
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1/SR)
    m = np.ones_like(fr)
    m[fr < lo] = np.clip(fr[fr < lo] / lo, 0, 1)
    m[fr > hi] = np.clip(1 - (fr[fr > hi] - hi) / (hi * 1.4), 0.02, 1)
    return np.fft.irfft(X * m, n=len(x)).astype(np.float32)

def main():
    L = np.zeros(N, dtype=np.float32)
    R = np.zeros(N, dtype=np.float32)
    for i, (t0, ac, e) in enumerate(PLAN):
        t1 = PLAN[i + 1][0] if i + 1 < len(PLAN) else FIN
        env = envolvente(t0, t1 + 0.5, 0.5, 0.9)
        for j, m in enumerate(AC[ac]):
            v = pad_nota(m, env, e, detune=0.0012 + j * 0.0004)
            pan = 0.5 + (0.10 if j % 2 else -0.10)
            L += v * (1 - pan) * 1.2
            R += v * pan * 1.2
        # sub
        sub = np.sin(2*np.pi*f(AC[ac][0]-12)*t).astype(np.float32) * env * (0.085 * e)
        L += sub; R += sub

    # pulso cardíaco desde el censo
    for tb in np.arange(20.0, 64.0, 1.2):
        i0 = int(tb * SR); ln = int(0.5 * SR)
        if i0 + ln >= N: break
        tt = np.arange(ln) / SR
        golpe = (np.sin(2*np.pi*(58 - 26*tt)*tt) * np.exp(-tt*9)).astype(np.float32) * 0.11
        L[i0:i0+ln] += golpe; R[i0:i0+ln] += golpe

    # risers antes de cada acto
    for tr in [3.0, 9.6, 16.9, 22.7, 30.3, 36.6, 44.1, 51.6, 58.5, 64.5]:
        i0 = int(tr * SR); ln = int(1.0 * SR)
        if i0 + ln >= N: continue
        tt = np.arange(ln) / SR
        ruido = np.random.default_rng(int(tr*10)).normal(0, 1, ln).astype(np.float32)
        ruido = filtro_fft(ruido, 900, 7000)
        L[i0:i0+ln] += ruido * (tt/1.0) ** 2 * 0.055
        R[i0:i0+ln] += ruido * (tt/1.0) ** 2 * 0.055

    # impacto final (wordmark)
    i0 = int(65.35 * SR); ln = min(int(2.0 * SR), N - i0)
    tt = np.arange(ln) / SR
    imp = (np.sin(2*np.pi*(46 - 14*tt)*tt) * np.exp(-tt*3.2)).astype(np.float32) * 0.30
    br = np.random.default_rng(7).normal(0, 1, ln).astype(np.float32)
    br = filtro_fft(br, 2000, 9000) * np.exp(-tt*26) * 0.10
    L[i0:i0+ln] += imp + br; R[i0:i0+ln] += imp + br

    L = filtro_fft(L, 30, 6000)
    R = filtro_fft(R, 30, 6000)
    # anchura: 6 ms de retardo en R (Haas suave)
    d = int(0.006 * SR)
    R = np.concatenate([np.zeros(d, dtype=np.float32), R[:-d]])
    pico = max(np.abs(L).max(), np.abs(R).max())
    L *= 0.86 / pico; R *= 0.86 / pico
    est = np.stack([L, R], axis=1)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((est * 32767).astype(np.int16).tobytes())
    print("cama →", OUT, f"{DUR}s", "pico", round(float(np.abs(est).max()), 3))

if __name__ == "__main__":
    main()
