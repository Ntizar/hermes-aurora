#!/usr/bin/env python3
"""Plan v8 — cierra el manifiesto a 70,0 s exactos con las duraciones REALES de la voz.

Cada escena = voz + respiro (0,45 s). El sobrante/faltante se reparte en el cierre y en
el contrato (las dos escenas que aguantan aire). Nada hardcodeado: se lee de audio8/.
"""
import json, subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
AUDIO = RAIZ / "audio8"
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"
TOTAL = 70.0
ORDEN = ["00-open", "01-hook", "02-hueco", "03-contrato", "04-censo",
         "05-marcas", "06-juez", "07-bucle", "08-tema", "09-receta", "10-cierre"]

def dur(f):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(out.stdout.strip())

def main():
    durs = {n: round(dur(AUDIO / f"{n}.mp3") + 0.45, 3) for n in ORDEN[1:]}
    durs["00-open"] = 3.80
    total = sum(durs.values())
    diff = round(TOTAL - total, 2)
    durs["10-cierre"] = round(durs["10-cierre"] + diff, 2)
    # a múltiplos de 0,05 (20 fps → frames enteros sin resto)
    for n in durs:
        durs[n] = round(round(durs[n] / 0.05) * 0.05, 2)
    durs["10-cierre"] = round(durs["10-cierre"] + (TOTAL - sum(durs.values())), 2)
    t0, offsets = 0.0, {}
    for n in ORDEN:
        offsets[n] = round(t0, 2)
        t0 += durs[n]
    (RAIZ / "manifest-v8.json").write_text(json.dumps(durs, indent=1))
    (RAIZ / "offsets-v8.json").write_text(json.dumps(offsets, indent=1))
    for n in ORDEN:
        print(f"{n:12s} t0={offsets[n]:6.2f}  dur={durs[n]:5.2f}")
    print(f"TOTAL {t0:.2f}s")

if __name__ == "__main__":
    main()
