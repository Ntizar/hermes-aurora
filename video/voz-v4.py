#!/usr/bin/env python3
"""Voz v4 — kokoro am_michael (NaN), un fichero por escena → audio4/ + manifest.json."""
import json, subprocess, sys, time
from pathlib import Path
from urllib import request

RAIZ = Path(__file__).resolve().parent
AUDIO = RAIZ / "audio4"
AUDIO.mkdir(exist_ok=True)

GUION = {
    "01-beat1": "Every agent can build a page.",
    "02-beat2": "Almost none can prove it.",
    "03-nombre": "Aurora. A design system your agent cannot fake.",
    "04-buscar": "It doesn't guess. It asks the census: two thousand two hundred twenty three real objects, real markup, every class.",
    "05-trio": "One system, any product. Landing pages, dashboards, full apps.",
    "06-validar": "Then it proves the page. Invented classes, missing packs, hand written colors. Caught in milliseconds.",
    "07-limpio": "Iterate until it's clean. Ship it.",
    "08-dark": "Light and dark. Same markup, one attribute. Both designed.",
    "09-instalar": "Aurora for Hermes. Two tools. Four skills. Zero network.",
}

def clave():
    for linea in Path("/home/nan/.hermes/.env").read_text().splitlines():
        if linea.startswith("OPENAI_API_KEY="):
            return linea.split("=", 1)[1].strip().strip('"')
    sys.exit("no OPENAI_API_KEY")

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

manifest = {}
for nombre, texto in GUION.items():
    destino = AUDIO / f"{nombre}.mp3"
    for intento in range(3):
        try:
            tts(texto, destino); break
        except Exception as e:
            print(f"intento {intento+1} fallido {nombre}: {e}", file=sys.stderr); time.sleep(4)
    else:
        sys.exit(f"sin voz para {nombre}")
    d = duracion(destino)
    manifest[nombre] = round(d, 2)
    print(f"{nombre}: {d:.2f}s")
(RAIZ / "manifest-v4.json").write_text(json.dumps(manifest, indent=1))
print("manifest ok")
