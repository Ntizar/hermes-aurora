#!/usr/bin/env python3
"""Rasterizador v8 — para el v7 portal de cristal. Igual de determinista que v7:
un solo dueño del tiempo (Python), inyecta style por fotograma, nada de @keyframes.

Añade sobre v7:
  · data-out="t0,dur" → fade-OUT (para el fantasma refractado que se materializa:
    opacity = fade-in[data-d] × fade-out[data-out]).
  · El JS del cielo pinta con window.__t (se inyecta en el <head> de cada fotograma),
    incluso en los clones de los vidrios (todos los canvas .cielo reciben el mismo t).
  · Escenas 00 y 03 usan el mismo file:// (sin ES modules ya).

Uso: rasterizar-v8.py [escena ...]  (sin args: todas las del manifest-v6)
"""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames7"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
FPS = 20
MANIFEST = json.loads((RAIZ / "manifest-v6.json").read_text())
REVEAL_T, PUSH_T, VELOCIDAD = 0.55, 1.10, 25.0

def ease(k):
    return 1 - (1 - k) ** 3

def atrib(attrs, nombre):
    m = re.search(r'%s="([^"]*)"' % nombre, attrs)
    return m.group(1) if m else None

def set_style(attrs, extra):
    m = re.search(r'style="([^"]*)"', attrs)
    if m:
        viejo = m.group(1).rstrip().rstrip(";")
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

def aplicar(html, t, dur):
    for m in list(re.finditer(r"<([a-zA-Z0-9]+)((?:[^<>\"]|\"[^\"]*\")*)>", html)):
        tag, attrs = m.group(1), m.group(2)
        extras = []
        d = atrib(attrs, "data-d")
        out = atrib(attrs, "data-out")
        es_pz = bool(re.search(r'class="[^"]*\bpz\b[^"]*"', attrs))
        op = None
        if d is not None and not es_pz:
            k = min(max((t - float(d)) / REVEAL_T, 0), 1)
            if k < 1:
                e = ease(k)
                op = e
                extras.append(f"transform:translateY({26*(1-e):.1f}px)")
        if es_pz:
            k = min(max(t / PUSH_T, 0), 1)
            if k < 1:
                op = ease(k) if op is None else op * ease(k)
                extras.append(f"transform:scale({0.96+0.04*ease(k):.3f})")
        if out:
            t0, durc = [float(x) for x in out.split(",")]
            k = min(max((t - t0) / durc, 0), 1)
            if k > 0:
                op = (1 - ease(k)) if op is None else op * (1 - ease(k))
            if k == 1:
                extras.append("display:none")
        if op is not None:
            extras.insert(0, f"opacity:{max(op,0):.3f}")
        claim = atrib(attrs, "data-claim")
        if claim:
            dd, durc = [float(x) for x in claim.split(",")]
            k = min(max((t - dd) / durc, 0), 1)
            if k < 1:
                s = ease(k)
                extras = [f"opacity:{s:.3f}", f"filter:blur({14*(1-s):.1f}px)",
                          f"transform:scale({0.9+0.1*s:.3f})"]
        ken = atrib(attrs, "data-ken")
        if ken:
            obj = float(ken)
            prog = min(max(t / max(dur - 0.5, 1.0), 0), 1)
            extras.append(f"transform:scale({1+(obj-1)*prog:.4f})")
        if not extras:
            continue
        nuevo = set_style(attrs, ";".join(extras))
        html = html.replace(m.group(0), f"<{tag}{nuevo}>", 1)
    return html

def tipear(html, t):
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
        cuerpo = cuerpo.replace("<head>", f'<head><script>window.__t={t};</script>', 1)
        tmpf.write_text(cuerpo)
        r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                            "--window-size=1600,900", "--hide-scrollbars",
                            "--virtual-time-budget=1500",
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
