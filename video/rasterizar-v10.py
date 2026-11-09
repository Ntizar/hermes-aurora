#!/usr/bin/env python3
"""Rasterizador v9 — «The recipe». Un solo dueño del tiempo.

Por fotograma, en Python (forma cerrada de t), se inyecta style inline:
  data-d="t[,dur]"        fade + rise (o solo fade si dur)
  data-out="t,dur"        fade out
  data-claim="t,dur"      golpe: blur+scale
  data-ken="escala"       ken burns
  data-tipea="texto"      máquina de escribir (25 c/s)
  data-shard="d,dur,dx,dy,rot"  hoja de cristal que entra volando
  data-sweep="d,dur"      barrido especular
  data-count="d,dur,desde,hasta"  contador con separador de miles
  data-shake="t,dur,amp"  sacudida de cámara (sobre .marco)

Uso: rasterizar-v9.py [escena ...]
"""
import json, math, os, re, shutil, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SLIDES = RAIZ / "slides"
FRAMES = RAIZ / "frames9"
CHROME = "/home/nan/.cache/chrome/chrome-headless-shell-linux64/chrome-headless-shell"
LIBS = "/home/nan/.chrome-libs/usr/lib/x86_64-linux-gnu:/home/nan/.chrome-libs/lib/x86_64-linux-gnu"
FPS = 20
MANIFEST = json.loads((RAIZ / "manifest-v9.json").read_text())
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

def contar(html, t):
    def rep(m):
        attrs, viejo = m.group(1), m.group(2)
        d, dur, a, b = [float(x) for x in atrib(attrs, "data-count").split(",")]
        k = min(max((t - d) / dur, 0), 1)
        v = a + (b - a) * ease(k)
        return f'<span{attrs}>{int(round(v)):,}</span>'
    return re.sub(r'<span([^>]*data-count="[^"]*"[^>]*)>([^<]*)</span>', rep, html)

def aplicar(html, t, dur):
    for m in list(re.finditer(r"<([a-zA-Z0-9]+)((?:[^<>\"]|\"[^\"]*\")*)>", html)):
        tag, attrs = m.group(1), m.group(2)
        extras = []

        d = atrib(attrs, "data-d")
        out = atrib(attrs, "data-out")
        op = None
        if d is not None and not re.search(r'class="[^"]*\bpz\b', attrs):
            trozos = d.split(",")
            t0, durc = float(trozos[0]), (float(trozos[1]) if len(trozos) > 1 else REVEAL_T)
            k = min(max((t - t0) / max(durc, 0.01), 0), 1)
            if k < 1:
                e = ease(k)
                op = e
                extras.append(f"transform:translateY({26*(1-e):.1f}px)")

        if re.search(r'class="[^"]*\bpz\b', attrs):
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

        claim = atrib(attrs, "data-claim")
        if claim:
            dd, durc = [float(x) for x in claim.split(",")]
            k = min(max((t - dd) / durc, 0), 1)
            if k < 1:
                s = ease(k)
                op = s if op is None else op * s
                extras.append(f"filter:blur({14*(1-s):.1f}px)")
                extras.append(f"transform:scale({0.88+0.12*s:.3f})")

        shard = atrib(attrs, "data-shard")
        if shard:
            dd, durc, dx, dy, rot = [float(x) for x in shard.split(",")]
            k = min(max((t - dd) / durc, 0), 1)
            e = ease(k)
            op = e if op is None else op * e
            extras.append(f"transform:translate({dx*(1-e):.1f}px,{dy*(1-e):.1f}px) rotate({rot*(1-e):.2f}deg)")

        sweep = atrib(attrs, "data-sweep")
        if sweep:
            dd, durc = [float(x) for x in sweep.split(",")]
            k = min(max((t - dd) / durc, 0), 1)
            extras.append(f"transform:translateX({-160+320*ease(k):.1f}%)")

        shake = atrib(attrs, "data-shake")
        if shake:
            dd, durc, amp = [float(x) for x in shake.split(",")]
            if dd <= t <= dd + durc:
                k = (t - dd) / durc
                dx = amp * (1 - k) * math.sin(t * 46)
                dy = amp * 0.7 * (1 - k) * math.cos(t * 37)
                extras.append(f"transform:translate({dx:.2f}px,{dy:.2f}px) scale(1.012)")

        ken = atrib(attrs, "data-ken")
        if ken:
            obj = float(ken)
            prog = min(max(t / max(dur - 0.4, 1.0), 0), 1)
            extras.append(f"transform:scale({1+(obj-1)*prog:.4f})")

        if not extras:
            continue
        if op is not None:
            extras.insert(0, f"opacity:{max(op,0):.3f}")
        nuevo = set_style(attrs, ";".join(extras))
        html = html.replace(m.group(0), f"<{tag}{nuevo}>", 1)
    return html

def tipear(html, t):
    def rep(m):
        atributos, texto_atrib = m.group(1), m.group(2)
        texto = texto_atrib.replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        dm = re.search(r'data-d="([\d.]+)"', atributos)
        d = float(dm.group(1)) if dm else 0.9
        n = int(max(t - d, 0) * VELOCIDAD)
        if n >= len(texto):
            return m.group(0)
        return f'<span {atributos}>{texto[:n]}</span>'
    return re.sub(r'<span (data-tipea="[^"]*"[^>]*)>([^<]*)</span>', rep, html)

def pagina(nombre, t):
    base = (SLIDES / f"{nombre}.html").read_text()
    cuerpo = tipear(contar(aplicar(base, t, MANIFEST[nombre]), t), t)
    t0 = re.search(r'data-t0="([\d.]+)"', base)
    t0 = t0.group(1) if t0 else "0"
    return cuerpo.replace("<head>", f"<head><script>window.__t={t};window.__T0={t0};</script>", 1)

def capturar(nombre, dur):
    total = round(dur * FPS)
    destino = FRAMES / nombre
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    tmpf = SLIDES / f"_frame8_{os.getpid()}.html"
    env = dict(os.environ, LD_LIBRARY_PATH=LIBS)
    for i in range(total):
        t = round(i / FPS, 3)
        tmpf.write_text(pagina(nombre, t), encoding="utf-8")
        out = destino / f"{i:04d}.png"
        r = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                            "--window-size=1600,900", "--hide-scrollbars",
                            "--virtual-time-budget=2000", "--screenshot=" + str(out),
                            tmpf.resolve().as_uri()], capture_output=True, text=True, timeout=90, env=env)
        if not out.exists():
            print(f"FALLO {nombre} f{i}: {r.stderr[:300]}", file=sys.stderr)
            sys.exit(1)
        if i % 40 == 0:
            print(f"  {nombre} {i}/{total}", flush=True)
    tmpf.unlink(missing_ok=True)
    print("ok", nombre, total, flush=True)

if __name__ == "__main__":
    FRAMES.mkdir(exist_ok=True)
    for nombre in (sys.argv[1:] or list(MANIFEST)):
        capturar(nombre, MANIFEST[nombre])
    print("rasterizado completo")
