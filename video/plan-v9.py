#!/usr/bin/env python3
"""Plan v9 — 70,0 s exactos con las duraciones reales de audio9/."""
import json, subprocess
from pathlib import Path
RAIZ = Path(__file__).resolve().parent
AUDIO = RAIZ / "audio9"
FFPROBE = "/home/nan/Projects/subtitulador-brutal/bin/ffprobe"
TOTAL = 70.0
ORDEN = ["00-open", "01-acabada", "02-inventa", "03-llano", "04-tecnico",
         "05-planos", "06-juez", "07-bucle", "08-tema", "09-receta", "10-cierre"]
def dur(f):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(out.stdout.strip())
def main():
    durs = {"00-open": 4.00}
    for n in ORDEN[1:]:
        durs[n] = round(dur(AUDIO / f"{n}.mp3") + 0.45, 3)
    diff = round(TOTAL - sum(durs.values()), 2)
    durs["03-llano"] = round(durs["03-llano"] + diff * 0.6, 3)
    durs["05-planos"] = round(durs["05-planos"] + diff * 0.4, 3)
    for n in durs:
        durs[n] = round(round(durs[n] / 0.05) * 0.05, 2)
    durs["10-cierre"] = round(durs["10-cierre"] + (TOTAL - sum(durs.values())), 2)
    t0, offsets = 0.0, {}
    for n in ORDEN:
        offsets[n] = round(t0, 2); t0 += durs[n]
    (RAIZ / "manifest-v9.json").write_text(json.dumps(durs, indent=1))
    (RAIZ / "offsets-v9.json").write_text(json.dumps(offsets, indent=1))
    for n in ORDEN:
        print(f"{n:11s} t0={offsets[n]:6.2f} dur={durs[n]:5.2f}")
    print(f"TOTAL {t0:.2f}s")
if __name__ == "__main__":
    main()
