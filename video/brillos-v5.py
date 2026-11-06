#!/usr/bin/env python3
"""Brillo medio de TODAS las escenas v5 (primer, medio y último fotograma)."""
import os
from PIL import Image

base = "/home/nan/Projects/hermes-aurora/video/frames5"
for carpeta in sorted(os.listdir(base)):
    d = os.path.join(base, carpeta)
    ficheros = sorted(os.listdir(d))
    muestra = [ficheros[0], ficheros[len(ficheros)//2], ficheros[-1]]
    brillos = []
    for f in muestra:
        img = Image.open(os.path.join(d, f)).convert("L")
        px = list(img.getdata())
        brillos.append(round(sum(px)/len(px), 1))
    print(carpeta, brillos)
