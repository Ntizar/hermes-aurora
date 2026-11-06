#!/usr/bin/env python3
"""Reemplaza el reveal CSS por reveal JS (por reloj rAF) en las slides con <img>
(05-trio, 07-limpio, 08-dark): el patrón determinista que ya funciona."""
import re
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")

REVEAL_JS = """
<script>
  // Reveal por reloj: determinista bajo virtual-time (el CSS+img compuesto cuelga
  // el rasterizador: nz-reveal sobre contenedor con <img> sale negro).
  (function () {
    const t0 = performance.now();
    const objetivos = [];
    document.querySelectorAll('[data-reveal]').forEach(function (el) {
      objetivos.push([el, parseFloat(el.getAttribute('data-reveal')) || 0]);
    });
    function paso(ahora) {
      const t = (ahora - t0) / 1000;
      for (const par of objetivos) {
        const k = Math.min(Math.max((t - par[1]) / 0.9, 0), 1);
        par[0].style.opacity = 1 - Math.pow(1 - k, 3);
      }
      requestAnimationFrame(paso);
    }
    requestAnimationFrame(paso);
  })();
</script>
"""

for nombre in ["05-trio", "07-limpio", "08-dark"]:
    f = SLIDES / (nombre + ".html")
    src = f.read_text()
    # 1) quitar las clases nz-reveal/ken de los shot-wrap y pasar el --d a data-reveal
    def cambia(m):
        d = re.search(r"--d:\s*([\d.]+)s", m.group(0))
        clase = "shot-wrap ken" if "ken" in m.group(0) else "shot-wrap"
        return '<div class="%s" data-reveal="%s">' % (clase, d.group(1) if d else "0")
    src = re.sub(r'<div class="shot-wrap ken nz-reveal"[^>]*>', cambia, src)
    # 2) inyectar el script antes de </body>
    if "data-reveal" in src and "requestAnimationFrame" not in src:
        src = src.replace("</body>", REVEAL_JS + "\n</body>")
    f.write_text(src)
    print(nombre, "parcheado")
