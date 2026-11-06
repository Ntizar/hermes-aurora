#!/usr/bin/env python3
"""El head de 08 (copiado de HEAD_DARK de slides-v4) vs el head de 01 (que pinta).
DIFF REAL de los dos <style> para ver la diferencia que rompe el render."""
import difflib
import re
from pathlib import Path

SLIDES = Path("/home/nan/Projects/hermes-aurora/video/slides")
def head_style(f):
    src = (SLIDES / f).read_text()
    return re.search(r"<style>(.*?)</style>", src, re.S).group(1)

a = head_style("01-beat1.html")
b = head_style("08-dark.html")
for l in difflib.unified_diff(a.splitlines(), b.splitlines(), "01", "08", lineterm=""):
    print(l[:120])
