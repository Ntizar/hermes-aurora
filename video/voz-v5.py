import os
#!/usr/bin/env python3
"""Voz v5 — guion nuevo, más llamativo, sin subtítulos en el montaje.
kokoro am_michael (NaN), un fichero por escena → audio5/ + manifest-v6.json.
La duración de cada escena sale de su propio audio (nada hardcodeado)."""
import json, subprocess, sys, time
from pathlib import Path
from urllib import request

RAIZ = Path(__file__).resolve().parent
AUDIO = RAIZ / "audio5"
AUDIO.mkdir(exist_ok=True)

# Guion nuevo (video/GUION-v6.md AUDIOS = estas mismas frases).
GUION = {
    "01-beat1":  "Every AI agent can build you a page.",
    "02-beat2":  "Almost none can prove the page is real.",
    "03-nombre": "Aurora. A design system your agent cannot fake.",
    "04-buscar": "It never guesses. It asks the census: two thousand two hundred twenty three real objects, real markup, every class.",
    "05-trio":   "The same system behind a landing, a dashboard, a login. Four brands. Light and dark. All of it audited.",
    "06-validar": "Then the auditor strikes. Invented classes. Fake gradients. Hand written colors. Caught in milliseconds.",
    "07-limpio": "The agent fixes. The agent iterates. Until the report is spotless: zero failures.",
    "08-dark":   "And here's the magic trick. One attribute. The whole product, re-themed. Both designed, nothing improvised.",
    "09-instalar": "Aurora for Hermes. Two tools. Four skills. Zero network.",
    "10-cierre":  "Stop admiring screenshots. Start shipping proof. Aurora, for Hermes.",
}
# 00-three: intro muda (instrumental three.js) — sin voz.

def clave():
    # Sin secretos en el repo: la clave llega por entorno (el .env lo carga tu shell).
    for var in ("OPENAI_API_KEY", "NAN_API_KEY"):
        v = os.environ.get(var)
        if v:
            return v.strip().strip('"')
    sys.exit("exporta OPENAI_API_KEY antes de generar la voz")

def tts(texto, destino):
    peticion = request.Request(
        "https://api.nan.builders/v1/audio/speech",
        data=json.dumps({"model": "kokoro", "voice": "am_michael",
                         "input": texto, "response_format": "mp3"}).encode(),
        headers={"Authorization": f"Bearer {clave()}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0"})
    with request.urlopen(peticion, timeout=120) as r:
        destino.write_bytes(r.read())

def duracion(fichero):
    ff = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"
    out = subprocess.run([ff, "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(fichero)], capture_output=True, text=True)
    return float(out.stdout.strip())

for nombre, texto in GUION.items():
    destino = AUDIO / f"{nombre}.mp3"
    for intento in range(3):
        try:
            tts(texto, destino); break
        except Exception as e:
            print(f"intento {intento+1} fallido {nombre}: {e}", file=sys.stderr); time.sleep(4)
    else:
        sys.exit(f"sin voz para {nombre}")
    print(f"{nombre}: {duracion(destino):.2f}s")
print("voces listas")
