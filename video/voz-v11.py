#!/usr/bin/env python3
"""Voz v11 — narración de la demo light (60 s). Solo voz, sin música.

Cada línea entra 0,35 s después del corte de su escena y debe caber en la ventana
(duración de escena − 0,7 s). audio11/ + comprobación de encaje.
"""
import json, subprocess, sys, time
from pathlib import Path
from urllib import request

RAIZ = Path(__file__).resolve().parent
AUDIO = RAIZ / "audio11"
AUDIO.mkdir(exist_ok=True)
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"
MANIFEST = json.loads((RAIZ / "manifest-v11.json").read_text())

GUION = {
    "00-title":    "Aurora for Hermes. Two offline tools. One real page.",
    "01-ask":      "Step one. The agent asks in plain words. The catalogue answers with the family, the pack and the real markup.",
    "02-compose":  "Step two. It composes with classes that already exist: plans, price table, buttons. No invented names.",
    "03-mobile":   "Step three. It measures at three hundred ninety pixels. The table stacks, and nothing overflows.",
    "04-validate": "Step four. The validator checks the page against the census: invented class, gradient, hand-written colours, missing footer. Four failures.",
    "05-fix":      "Step five. The agent fixes them and runs it again. Zero failures. Now it ships.",
    "06-close":    "Two tools. Four skills. Zero network. Aurora, for Hermes.",
}

def clave():
    import os
    for var in ("OPENAI_API_KEY", "NAN_API_KEY"):
        v = os.environ.get(var)
        if v: return v.strip().strip('"')
    sys.exit("exporta OPENAI_API_KEY")

def tts(texto, destino):
    peticion = request.Request(
        "https://api.nan.builders/v1/audio/speech",
        data=json.dumps({"model": "kokoro", "voice": "am_michael", "input": texto,
                         "response_format": "mp3"}).encode(),
        headers={"Authorization": f"Bearer {clave()}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0"})
    with request.urlopen(peticion, timeout=120) as r:
        destino.write_bytes(r.read())

def dur(f):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(out.stdout.strip())

if __name__ == "__main__":
    for nombre, texto in GUION.items():
        destino = AUDIO / f"{nombre}.mp3"
        for intento in range(4):
            try:
                tts(texto, destino); break
            except Exception as e:
                print(f"  intento {intento+1}: {e}", file=sys.stderr); time.sleep(4)
        else:
            sys.exit(f"sin voz para {nombre}")
        d = dur(destino)
        ventana = MANIFEST[nombre] - 0.7
        print(f"{nombre:12s} voz {d:5.2f}s · ventana {ventana:5.2f}s · {'OK' if d <= ventana else 'NO CABE'}")
    print("voces listas")
