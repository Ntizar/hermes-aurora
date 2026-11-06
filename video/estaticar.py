#!/usr/bin/env python3
"""data-reveal JS sobre <img> compone negro en este headless. Solución final:
revelar con opacity en el ESTILO (sin JS ni CSS-anim): el rasterizador escribe
style="opacity:k" directo por fotograma. Elimino data-reveal/JS de 05/07/08 y
rasterizar-v5 calculará la opacidad. Aquí dejo los HTML estáticos (opacity 1)."""
import re
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
for nombre in ["05-trio", "07-limpio", "08-dark"]:
    f = SLIDES / (nombre + ".html")
    src = f.read_text()
    # quitar el bloque <script> del reveal JS
    src = re.sub(r"<script>\s*// Reveal por reloj.*?</script>", "", src, flags=re.S)
    # quitar data-reveal (revelado lo controlará el rasterizador con opacity)
    src = re.sub(r' data-reveal="[\d.]+"', "", src)
    # asegurarse de que los shot-wrap no tienen clase de animación
    src = src.replace(' class="shot-wrap ken" ', ' class="shot-wrap" ')
    f.write_text(src)
    print(nombre, "estático (opacity la pone el rasterizador)")
