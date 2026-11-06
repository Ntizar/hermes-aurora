#!/usr/bin/env python3
"""QA de parpadeo v2: distingue FUNDIDO (monótono, ok) de PARPADEO (oscilación, mal).

Definición operativa de parpadeo: la serie de brillo da un salto > UMBRAL y, en la
ventana siguiente, el nivel REGRESA cerca del valor anterior al salto (un fundido
nunca regresa; un flicker sí). Sin.args → frames5 (histórico, debe fallar).
Salida: 0 si ninguna escena rebota; 1 en caso contrario.
"""
import sys, os
from PIL import Image

UMBRAL = 6.0     # niveles de gris (0-255)
VENTANA = 8      # muestras hacia delante (8*2/20 fps = 0.8 s)
dirs = sys.argv[1:] or ["/home/nan/Projects/hermes-aurora/video/frames5"]
mal = False
for d in dirs:
    entradas = sorted(os.listdir(d))
    escenas = entradas if os.path.isdir(os.path.join(d, entradas[0])) else [""]
    for esc in escenas:
        ruta = os.path.join(d, esc) if esc else d
        fs = sorted(f for f in os.listdir(ruta) if f.endswith(".png"))
        if len(fs) < 6:
            continue
        vals = []
        for f in fs[::2]:
            img = Image.open(os.path.join(ruta, f)).convert("L").resize((100, 57))
            px = list(img.getdata())
            vals.append(sum(px) / len(px))
        saltos = rebotes = 0
        for i in range(len(vals) - 1):
            delta = vals[i + 1] - vals[i]
            if abs(delta) <= UMBRAL:
                continue
            saltos += 1
            destino = vals[i + 1]
            for j in range(i + 2, min(i + 1 + VENTANA, len(vals))):
                if abs(vals[j] - vals[i]) < UMBRAL and abs(destino - vals[i]) > UMBRAL * 2:
                    rebotes += 1
                    break
        flag = "PARPADEO" if rebotes else "ok"
        if rebotes:
            mal = True
        print("%-14s saltos=%2d rebotes=%d  %s" % (esc or os.path.basename(d), saltos, rebotes, flag))
print("RESULTADO:", "FALLO — parpadeo detectado" if mal else "VÁLIDO — sin parpadeo")
sys.exit(1 if mal else 0)
