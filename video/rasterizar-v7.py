#!/usr/bin/env python3
"""Rasterizador v7 — determinismo total, cero parpadeo.

Reglas:
  · El HTML base está en su estado FINAL (todo visible). Este script NUNCA escribe el
    html de slides: trabaja sobre una copia en memoria por fotograma.
  · Cada animación la calcula Python en función de t y la inyecta como style inline:
      data-d="X"      → fade-in con translateY (reveal), desde t=X, 0.55 s
      class="pz"      → push (scale .96→1 + fade), 1.1 s desde t=0
      data-ken="1.05" → ken-burns: scale 1→1.05 a lo largo de la escena
      data-tipea="…"  → tecleo a 25 caracteres/s desde su data-d
      data-claim="2.0,1.6" → blur+fade+escala del titular de la intro
    Nada de @keyframes ni setTimeout: mismo t ⇒ mismo fotograma (byte a byte).
  · 00-three es el único con JS (WebGL, PRNG con semilla fija): entra por el mismo
    file:// y su animación de claim también la controla este script.
Uso: rasterizar-v7.py [escena ...]   (sin args: todas del manifest-v6)
"""
import json, os, re, shutil, subprocess, sys, threading, http.server, socketserver
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames6"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
FPS = 20
HTTP_PORT = 8647
MANIFEST = json.loads((RAIZ / "manifest-v6.json").read_text())
REVEAL_T, PUSH_T, VELOCIDAD = 0.55, 1.10, 25.0

def ease(k):
    return 1 - (1 - k) ** 3

def atrib(attrs, nombre):
    m = re.search(r'%s="([^"]*)"' % nombre, attrs)
    return m.group(1) if m else None

def set_style(attrs, extra):
    """Fusiona `extra` con el style existente (si lo hay)."""
    m = re.search(r'style="([^"]*)"', attrs)
    if m:
        viejo = m.group(1).rstrip().rstrip(";")
        # transformar: si ambos ponen transform, se concatenan las funciones
        partes = []
        for chunk in (viejo + ";" + extra).split(";"):
            if not chunk.strip():
                continue
            k, _, v = chunk.partition(":")
            k = k.strip()
            if k == "transform" and partes and partes[-1][0] == "transform":
                partes[-1] = (k, partes[-1][1] + " " + v.strip())
            else:
                partes.append((k, v.strip()))
        nuevo = ";".join(f"{k}:{v}" for k, v in partes)
        return attrs[:m.start(1)] + nuevo + attrs[m.end(1):]
    return attrs + f' style="{extra}"'

def transformada(attrs):
    m = re.search(r'style="[^"]*transform:([^;"]+)', attrs)
    return m.group(1).strip() if m else None

def aplicar(html, t, dur):
    """Inyecta en cada elemento con data atributos de animación el style de su tiempo t."""
    def mod(m):
        nombre_tag, attrs = m.group(1), m.group(2)
        if "data-anim-aplicado" in attrs:
            return None
        extras = []
        d = atrib(attrs, "data-d")
        if d is not None and "pz" not in (attrs.split("class=")[1][:60] if "class=" in attrs else ""):
            k = min(max((t - float(d)) / REVEAL_T, 0), 1)
            if k < 1:
                e = ease(k)
                extras.append(f"opacity:{e:.3f}")
                extras.append(f"transform:translateY({26*(1-e):.1f}px)")
        if re.search(r'class="[^"]*\bpz\b[^"]*"', attrs):
            k = min(max(t / PUSH_T, 0), 1)
            if k < 1:
                e = ease(k)
                extras.append(f"opacity:{e:.3f}")
                extras.append(f"transform:scale({0.96+0.04*e:.3f})")
        claim = atrib(attrs, "data-claim")
        if claim:
            dd, durc = [float(x) for x in claim.split(",")]
            k = min(max((t - dd) / durc, 0), 1)
            if k < 1:
                s = ease(k)
                extras.append(f"opacity:{s:.3f}")
                extras.append(f"filter:blur({14*(1-s):.1f}px)")
                extras.append(f"transform:scale({0.9+0.1*s:.3f})")
        ken = atrib(attrs, "data-ken")
        if ken:
            obj = float(ken)
            prog = min(max(t / max(dur - 0.5, 1.0), 0), 1)
            extras.append(f"transform:scale({1+(obj-1)*prog:.4f})")
        if not extras:
            return None
        attrs = set_style(attrs, ";".join(extras))
        return f"<{nombre_tag}{attrs}>"
    out = html
    for m in list(re.finditer(r"<([a-zA-Z0-9]+)((?:[^<>\"]|\"[^\"]*\")*)>", html)):
        res = mod(m)
        if res and res not in out:
            out = out.replace(m.group(0), res, 1)
    return out

def tipear(html, t):
    """Prefijo tecleado de los spans data-tipea (velocidad fija, sin JS)."""
    def rep(m):
        atributos, texto_atrib, completo = m.group(1), m.group(2), m.group(3)
        texto = texto_atrib.replace("&quot;", '"').replace("&amp;", "&")
        dm = re.search(r'data-d="([\d.]+)"', atributos)
        d = float(dm.group(1)) if dm else 0.9
        n = int(max(t - d, 0) * VELOCIDAD)
        if n >= len(texto):
            return m.group(0)
        return f'<span {atributos}>{texto[:n]}</span>'
    return re.sub(r'<span (data-tipea="([^"]*)"[^>]*)>([^<]*)</span>', rep, html)

def capturar(nombre, dur):
    total = round(dur * FPS)
    destino = FRAMES / nombre
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)
    base_html = (SLIDES / (nombre + ".html")).read_text()
    tmpf = SLIDES / ("_frame%d.html" % os.getpid())
    for i in range(total):
        t = round(i / FPS, 3)
        cuerpo = tipear(aplicar(base_html, t, dur), t)
        if nombre == "00-three":
            # reloj virtual único: el canvas pinta con t en vez de performance.now()
            cuerpo = cuerpo.replace("<head>", f'<head><script>window.__t={t};</script>', 1)
        tmpf.write_text(cuerpo)
        r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                            "--window-size=1600,900", "--hide-scrollbars",
                            "--virtual-time-budget=" + str(int(t * 1000) + 300),
                            "--screenshot=" + str(destino / ("%04d.png" % i)),
                            tmpf.resolve().as_uri()],
                           capture_output=True, text=True, timeout=90)
        if not (destino / ("%04d.png" % i)).exists():
            print("FALLO %s f%d: %s" % (nombre, i, r.stderr[:200]), file=sys.stderr)
            sys.exit(1)
    tmpf.unlink(missing_ok=True)
    print("ok", nombre, total)

if __name__ == "__main__":
    FRAMES.mkdir(exist_ok=True)
    for nombre in (sys.argv[1:] or list(MANIFEST)):
        capturar(nombre, MANIFEST[nombre])
