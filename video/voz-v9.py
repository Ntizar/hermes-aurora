import os
#!/usr/bin/env python3
"""Voz v9 — «catalogue & inspector». Solo voz: no hay música ni SFX en este film."""
import json, subprocess, sys, time
from pathlib import Path
from urllib import request

RAIZ = Path(__file__).resolve().parent
AUDIO = RAIZ / "audio9"
AUDIO.mkdir(exist_ok=True)
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"

GUION = {
    "01-acabada": "This page looks finished. It isn't. Three things are wrong, and you can't see them.",
    "02-inventa": "Your agent doesn't know your system, so it invents classes, gradients and colours nobody approved.",
    "03-llano":   "In plain words: a parts catalogue and a building inspector. The catalogue says what exists; the inspector proves what you built.",
    "04-tecnico": "For engineers: a census, a validator that fails the build, and skills that teach the procedure.",
    "05-planos":  "You start from pages that already work: landing, dashboard, login, shop, chat, app. The agent fills them in.",
    "06-juez":    "The inspector runs: unknown class, banned gradient, hand-written colour. Caught in milliseconds.",
    "07-bucle":   "The agent fixes them, runs it again. Zero failures, or it doesn't ship.",
    "08-tema":    "One attribute re-themes everything. Light and dark, both designed.",
    "09-receta":  "Aurora is the proof. The recipe is yours: your catalogue, your inspector, your skills.",
    "10-cierre":  "Any agent. Any brand. Zero guessing. Aurora, for Hermes.",
}
MAQUINA = ("00-open", "Build me a landing page.")

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
