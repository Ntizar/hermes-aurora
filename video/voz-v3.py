import os
#!/usr/bin/env python3
"""Voz del vídeo v3 con kokoro (NaN, /v1/audio/speech, voz am_michael).
Un fichero por escena en video/audio3/. Mide duración y escribe manifest.json."""
import json, subprocess, sys, time
from pathlib import Path
from urllib import request

RAIZ = Path(__file__).resolve().parent
AUDIO = RAIZ / "audio3"
AUDIO.mkdir(exist_ok=True)

GUION = {
    "01-beat1": "Every agent can build a page.",
    "02-beat2": "Almost none can prove it.",
    "03-nombre": "Aurora. A design system your agent cannot fake.",
    "04-buscar": "It doesn't guess. It asks the census: two thousand two hundred and twenty three real objects. Real markup. Every class.",
    "05-pagina": "Compose with what exists.",
    "06-validar": "Then it proves the page. Invented classes, missing packs, hand written colors. Caught in milliseconds.",
    "07-limpio": "Iterate until it's clean. Ship it.",
    "08-instalar": "Aurora for Hermes. Two tools. Four skills. Zero network.",
}

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

def main():
    manifest = {}
    for nombre, texto in GUION.items():
        destino = AUDIO / f"{nombre}.mp3"
        for intento in range(3):
            try:
                tts(texto, destino); break
            except Exception as e:
                print(f"intento {intento+1} fallido {nombre}: {e}", file=sys.stderr)
                time.sleep(4)
        else:
            sys.exit(f"sin voz para {nombre}")
        d = duracion(destino)
        manifest[nombre] = round(d, 2)
        print(f"{nombre}: {d:.2f}s")
    (RAIZ / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print("manifest escrito")

if __name__ == "__main__":
    main()
