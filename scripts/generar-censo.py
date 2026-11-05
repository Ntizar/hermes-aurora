#!/usr/bin/env python3
"""Build the bundled census (`data/censo.json`) from Aurora's `components.json`.

The census is a trimmed, read-only snapshot: families, classes, the real markup of each
family and the class → pack map the validator needs. It is generated, never edited by hand;
regenerate it on every Aurora release and bump the plugin version.

Usage:
    python3 scripts/generar-censo.py                       # reads ~/Projects/Aurora/components.json
    python3 scripts/generar-censo.py --fuente /ruta/components.json
    python3 scripts/generar-censo.py --url                 # fetch from jsDelivr (network)

No dependencies beyond the standard library.
"""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "censo.json"
DEFAULT_SOURCE = Path.home() / "Projects" / "Aurora" / "components.json"
CDN = "https://cdn.jsdelivr.net/gh/Ntizar/Aurora@master/components.json"


def _load(args) -> dict:
    if args.url:
        with urllib.request.urlopen(CDN, timeout=45) as resp:  # noqa: S310 - fixed https URL
            return json.loads(resp.read().decode("utf-8"))
    path = Path(args.fuente).expanduser() if args.fuente else DEFAULT_SOURCE
    if not path.is_file():
        sys.exit(f"error: no encuentro {path} (usa --fuente o --url)")
    return json.loads(path.read_text(encoding="utf-8"))


def _tokens(text: str) -> list[str]:
    """Search words for the lookup: lowercase, no accents, split on anything non-alphanumeric."""
    plain = unicodedata.normalize("NFKD", str(text or ""))
    plain = "".join(ch for ch in plain if not unicodedata.combining(ch)).lower()
    out, cur = [], []
    for ch in plain:
        if ch.isalnum():
            cur.append(ch)
        elif cur:
            out.append("".join(cur))
            cur = []
    if cur:
        out.append("".join(cur))
    return out


def build(source: dict) -> dict:
    objetos = source.get("objetos") or {}
    familias: dict[str, dict] = {}
    clases: dict[str, dict] = {}

    for name, item in objetos.items():
        pack = item.get("pack") or ""
        markup = item.get("markup") or {}
        clase_list = list(dict.fromkeys(item.get("clases") or []))
        entry = {
            "pack": f"packs/{pack}" if pack and not pack.startswith("packs/") else pack,
            "categoria": str(item.get("categoria") or ""),
            "demo": item.get("demo") or markup.get("demo") or "",
            "clases": clase_list,
            "titulo": (markup.get("titulo") or "").strip(),
            "markup": (markup.get("markup") or "").strip(),
            "noUsar": [str(x) for x in (item.get("noUsar") or [])],
            "palabras": sorted({
                *[name.replace("nz-", "").replace("-", " ")],
                *_tokens(markup.get("titulo")),
                *[c.replace("nz-", "").replace("--", " ").replace("-", " ") for c in clase_list],
            }),
        }
        familias[name] = entry
        for clase in clase_list:
            clases.setdefault(clase, {"familia": name, "pack": entry["pack"]})

    packs_meta = {
        (k if k.startswith("packs/") else f"packs/{k}"): {
            "categoria": str(v.get("categoria") or ""),
            "nombre": v.get("nombre") or "",
            "descripcion": (v.get("descripcion") or "")[:280],
        }
        for k, v in (source.get("packs") or {}).items()
    }

    return {
        "sistema": source.get("name") or "Aurora",
        "version": source.get("version") or "",
        "canal": "v" + str(source.get("version") or "").split(".")[0].lstrip("v"),
        "namespace": source.get("namespace") or "nz",
        "cdn": source.get("cdn") or {},
        "lexico": source.get("lexico") or {},
        "familias": familias,
        "clases": clases,
        "packs": packs_meta,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera data/censo.json desde Aurora")
    parser.add_argument("--fuente", help="ruta a components.json")
    parser.add_argument("--url", action="store_true", help="descargar components.json de jsDelivr")
    args = parser.parse_args()

    census = build(_load(args))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(census, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    size = OUT.stat().st_size / 1024
    print(f"censo {census['sistema']} {census['version']}: "
          f"{len(census['familias'])} familias, {len(census['clases'])} clases, {size:.0f} KB → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
