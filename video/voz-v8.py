import os
#!/usr/bin/env python3
"""Voz v8 — «The recipe». kokoro vía api.nan.builders.

Una línea por escena → audio8/ + duraciones reales en manifest-v8.json.
La 00 lleva además la voz de máquina (af_heart) que da la orden.
"""
import json, subprocess, sys, time
from pathlib import Path
from urllib import request

RAIZ = Path(__file__).resolve().parent
AUDIO = RAIZ / "audio8"
AUDIO.mkdir(exist_ok=True)
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"

GUION = {
    "01-hook":    "Your AI agent can build a page in seconds. Beautiful, fast, and completely improvised.",
    "02-hueco":   "It doesn't know your system. It invents class names, paints gradients nobody approved, and calls it done.",
    "03-contrato":"The fix isn't a better prompt. It's a contract: a census, a judge, and skills.",
    "04-censo":   "The census is what exists: every object, every class, the real markup. Machine-readable. No guessing.",
    "05-marcas":  "One system, four brands, three products: landing, dashboard, login. All audited.",
    "06-juez":    "The judge checks the page: invented classes, banned gradients, hand-written colours. Caught in milliseconds.",
    "07-bucle":   "The agent fixes it, re-runs it. Zero failures, or it doesn't ship. That's the loop that kills slop.",
    "08-tema":    "One attribute, and the whole product re-themes. Light and dark, both designed, nothing improvised.",
    "09-receta":  "Aurora is the proof. The recipe is yours: your census, your judge, your skills.",
    "10-cierre":  "Any agent. Zero guessing. Aurora, for Hermes.",
}
MAQUINA = ("00-three", "Build me a landing page.")

def clave():
    # Sin secretos en el repo: la clave llega por entorno (el .env lo carga tu shell).
    for var in ("OPENAI_API_KEY", "NAN_API_KEY"):
        v = os.environ.get(var)
        if v:
            return v.strip().strip('"')
    sys.exit("exporta OPENAI_API_KEY antes de generar la voz")

def tts(texto, destino, voz):
    peticion = request.Request(
        "https://api.nan.builders/v1/audio/speech",
        data=json.dumps({"model": "kokoro", "voice": voz, "input": texto,
                         "response_format": "mp3"}).encode(),
        headers={"Authorization": f"Bearer {clave()}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0"})
    with request.urlopen(peticion, timeout=120) as r:
        destino.write_bytes(r.read())

def duracion(f):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(out.stdout.strip())

def genera(nombre, texto, voz="am_michael"):
    destino = AUDIO / f"{nombre}.mp3"
    for intento in range(4):
        try:
            tts(texto, destino, voz); break
        except Exception as e:
            print(f"  intento {intento+1} {nombre}: {e}", file=sys.stderr); time.sleep(4)
    else:
        sys.exit(f"sin voz para {nombre}")
    print(f"{nombre}: {duracion(destino):.2f}s")

if __name__ == "__main__":
    for nombre, texto in GUION.items():
        genera(nombre, texto)
    genera(MAQUINA[0], MAQUINA[1], voz="af_heart")
    print("voces listas")
