"""Aurora tools for Hermes: census search and offline validation.

Both tools run entirely in-process against `data/censo.json` (a generated snapshot of
Aurora's `components.json`). No network, no subprocess, no writes.

Why they exist: a skill can tell a model the rules; only code can *guarantee* that the
class it just wrote exists and that the packs it needs are actually linked. That is the
difference the judges of a plugin contest ask for, and the difference a user feels when
the page renders instead of showing naked HTML.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_CENSO_PATH = Path(__file__).resolve().parent.parent / "data" / "censo.json"
_CENSO: dict[str, Any] | None = None

MAX_INPUT = 2_000_000  # 2 MB of HTML is already a very large page

AURORA_SEARCH_SCHEMA = {
    "name": "aurora_search",
    "description": (
        "Look up Aurora design-system objects by what you need (Spanish or English: "
        "'tabla que se apila en movil', 'kpi', 'chat', 'alert'). Returns the family, the CSS "
        "pack to link, every class and the REAL markup extracted from the catalogue demo. "
        "Offline: the census ships with the plugin. Use it instead of guessing class names."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "need": {"type": "string", "description": "What you need to build, in plain words."},
            "limit": {"type": "integer", "description": "Max families to return (default 5, max 20)."},
            "with_markup": {
                "type": "boolean",
                "description": "Include the canonical markup of each family (default true).",
            },
        },
        "required": ["need"],
    },
}

AURORA_VALIDATE_SCHEMA = {
    "name": "aurora_validate",
    "description": (
        "Validate an Aurora page offline and return failures (must fix) and warnings (read them). "
        "Checks invented classes against the bundled census, packs used but not linked, "
        "gradients, backdrop-filter, !important, hand-written colours, emojis in UI, duplicate "
        "h1 and the attribution footer. Pass either a file path or the HTML itself."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to the HTML file to validate."},
            "html": {"type": "string", "description": "HTML source, when there is no file on disk."},
        },
    },
}


def _censo() -> dict[str, Any]:
    global _CENSO
    if _CENSO is None:
        if not _CENSO_PATH.is_file():
            raise FileNotFoundError(f"censo no encontrado en {_CENSO_PATH}")
        _CENSO = json.loads(_CENSO_PATH.read_text(encoding="utf-8"))
    return _CENSO


def _norm(text: str) -> str:
    import unicodedata

    plain = unicodedata.normalize("NFKD", str(text or ""))
    plain = "".join(ch for ch in plain if not unicodedata.combining(ch))
    return plain.lower()


# Spanish is how people actually ask ("aviso de error", "tabla que se apila"); the census is
# named in a mix. Expanding the query beats asking the model to translate first.
SINONIMOS = {
    "aviso": ["alert", "callout", "alerta"],
    "alerta": ["alert", "aviso"],
    "error": ["danger", "error", "fallo"],
    "acceso": ["login", "acceso", "sesion", "auth"],
    "entrar": ["login", "acceso"],
    "login": ["login", "acceso"],
    "formulario": ["form", "formgrid", "field", "input", "campo"],
    "campo": ["field", "input", "campo"],
    "tabla": ["table", "tabla"],
    "boton": ["btn", "boton"],
    "grafico": ["chart", "grafico", "barras", "linea"],
    "grafica": ["chart", "grafico"],
    "tarjeta": ["article", "card", "bento", "kpi", "tarjeta"],
    "chat": ["chat", "msg", "prompt", "mensaje"],
    "conversacion": ["chat", "msg"],
    "menu": ["nav", "navbar", "menu", "tabs"],
    "navegacion": ["nav", "navbar", "breadcrumb", "tabs"],
    "cargando": ["carga", "skeleton", "spinner", "loading"],
    "modal": ["modal", "drawer", "sheet", "dialogo"],
    "dialogo": ["modal", "drawer", "sheet"],
    "fichero": ["file", "zona", "upload", "fichero"],
    "subir": ["upload", "file", "zona"],
    "precio": ["plan", "precio", "price", "pricing"],
    "icono": ["icon", "icono"],
    "buscador": ["search", "buscador", "buscar"],
    "pasos": ["wizard", "stepper", "pasos", "formgrid"],
    "metrica": ["kpi", "metrica", "stat", "tendencia"],
    "calendario": ["calendar", "calendario"],
    "etiqueta": ["badge", "tag", "etiqueta"],
    "desplegable": ["dropdown", "select", "desplegable"],
    "acordeon": ["acordeon", "preguntas", "faq", "details"],
    "informe": ["informe", "report", "print"],
    "panel": ["dash", "panel", "appshell", "kanban"],
    "esqueleto": ["skeleton", "carga"],
    "apila": ["apilable", "responsive"],
    "apilable": ["apilable"],
    "movil": ["apilable", "responsive"],
    "responsive": ["responsive", "apilable"],
    "peligroso": ["danger"],
}

STOPWORDS = {"con", "sin", "que", "los", "las", "del", "para", "una", "uno", "por", "como",
             "mas", "muy", "the", "and", "for", "with", "que", "sus", "este", "esta"}

_INDICE: list[tuple[str, dict, str, set[str], str]] | None = None


def _indice() -> list[tuple[str, dict, str, set[str], str]]:
    """Precomputed search index: family, entry, normalised family, classes, haystack."""
    global _INDICE
    if _INDICE is None:
        census = _censo()
        packs = census.get("packs") or {}
        rows = []
        for family, entry in census["familias"].items():
            pack = packs.get(entry.get("pack", ""), {})
            haystack = _norm(" ".join([
                entry.get("titulo", ""),
                " ".join(entry.get("palabras", [])),
                " ".join(entry.get("noUsar", [])[:3]),
                pack.get("nombre", ""),
                pack.get("descripcion", ""),
            ]))
            clases = {_norm(c) for c in entry.get("clases", [])}
            rows.append((family, entry, _norm(family), clases, haystack))
        _INDICE = rows
    return _INDICE


def _score(words: list[str], family: str, familia_norm: str, clases: set[str], haystack: str) -> tuple[int, list[str]]:
    """Return a score and the terms that matched, so the caller can see *why*."""
    score, matched = 0, []
    base = family.replace("nz-", "")
    for word in words:
        if len(word) < 3:
            continue
        for term in [word, *SINONIMOS.get(word, [])]:
            if term in familia_norm:
                score += 10
                matched.append(term)
            elif any(term in clase for clase in clases):
                score += 6
                matched.append(term)
            elif len(term) > 3 and term in haystack:
                score += 2
                matched.append(term)
    if base in {c.replace("nz-", "") for c in clases}:
        score += 2  # the family's own base class exists: it is a first-class object
    return score, sorted(set(matched))


def aurora_search(args: dict, **_: Any) -> str:
    query = str(args.get("need") or args.get("consulta") or "").strip()
    if not query:
        return json.dumps({"error": "empty query"}, ensure_ascii=False)
    limit = max(1, min(int(args.get("limit") or args.get("limite") or 5), 20))
    with_markup = args.get("with_markup", args.get("con_markup", True))
    census = _censo()

    words = [w for w in re.split(r"[^0-9a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+", _norm(query))
             if len(w) > 2 and w not in STOPWORDS]
    ranked = []
    for family, entry, familia_norm, clases, haystack in _indice():
        score, matched = _score(words, family, familia_norm, clases, haystack)
        if score:
            ranked.append((score, len(family), family, entry, matched))
    ranked.sort(key=lambda item: (-item[0], item[1], item[2]))

    results = []
    for score, _largo, family, entry, matched in ranked[:limit]:
        item = {
            "family": family,
            "pack": entry["pack"],
            "classes": entry["clases"][:25],
            "demo": entry["demo"],
            "title": entry.get("titulo", ""),
            "avoid": entry.get("noUsar", [])[:3],
            "score": score,
            "matched": matched,
        }
        if with_markup:
            item["markup"] = entry.get("markup", "")
        results.append(item)

    return json.dumps({
        "system": census["sistema"],
        "version": census["version"],
        "channel": census["canal"],
        "query": query,
        "results": results,
        "hint": (
            "Link only the packs you use: "
            f"https://cdn.jsdelivr.net/gh/Ntizar/Aurora@{census['canal']}/packs/<pack>.css"
        ),
    }, ensure_ascii=False)


_COLOR_RE = re.compile(r"(#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\()")
_GRADIENT_RE = re.compile(r"(linear-gradient|radial-gradient|conic-gradient)")
_EMOJI_RE = re.compile(
    "[" "\U0001F300-\U0001FAFF" "\U00002600-\U000027BF" "\U0001F1E6-\U0001F1FF" "\u2b00-\u2bff" "]"
)
_STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
_CODE_RE = re.compile(r"<(pre|code|samp|kbd|textarea)[^>]*>.*?</\1>", re.S | re.I)
_FOOTER = "Hecho con ❤️ por David Antizar"


def _text_only(html: str) -> str:
    """Visible-ish text: drop comments, style/script/code blocks and tags."""
    text = _COMMENT_RE.sub(" ", html)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    text = _CODE_RE.sub(" ", text)
    return re.sub(r"<[^>]+>", " ", text)


def aurora_validate(args: dict, **_: Any) -> str:
    source = args.get("html")
    ruta = args.get("path") or args.get("ruta")
    if source is None and ruta:
        path = Path(str(ruta)).expanduser()
        if not path.is_file():
            return json.dumps({"error": f"no such file: {path}"}, ensure_ascii=False)
        if path.stat().st_size > MAX_INPUT:
            return json.dumps({"error": "file too large (2 MB)"}, ensure_ascii=False)
        source = path.read_text(encoding="utf-8", errors="replace")
    if not source:
        return json.dumps({"error": "pass 'path' or 'html'"}, ensure_ascii=False)
    html = str(source)
    if len(html) > MAX_INPUT:
        return json.dumps({"error": "html too large (2 MB)"}, ensure_ascii=False)

    census = _censo()
    known: dict[str, dict] = census["clases"]
    fallos: list[str] = []
    avisos: list[str] = []

    # 1 · classes must exist in the census
    used: dict[str, int] = {}
    for attr in re.findall(r'class\s*=\s*"([^"]*)"', html):
        for token in attr.split():
            if token.startswith("nz-"):
                used[token] = used.get(token, 0) + 1
    invented = sorted(c for c in used if c not in known)
    if invented:
        fallos.append("unknown class(es), not in the census: " + ", ".join(invented[:12]))

    # 2 · every pack a used class belongs to must be linked
    packs = sorted({known[c]["pack"] for c in used if c in known and known[c]["pack"]})
    linked = {href for href in re.findall(r'href\s*=\s*"([^"]*\.css)"', html)}
    all_css = any(h.endswith("packs/all.css") for h in linked)
    missing = [] if all_css else [p for p in packs if not any(h.endswith(p) or h.endswith("/" + p) for h in linked)]
    if missing:
        fallos.append("pack(s) used but not linked: " + ", ".join(missing))

    styles = "\n".join(_STYLE_RE.findall(html))
    css = _COMMENT_RE.sub(" ", styles)

    # 3 · gradients / backdrop-filter / !important
    if _GRADIENT_RE.search(css) and "nz-cristal" not in html:
        fallos.append("gradient in page CSS (Aurora uses none; the crystal layer ships as p16-cristal.css)")
    if "backdrop-filter" in css and "nz-cristal" not in html:
        fallos.append("backdrop-filter in page CSS (only the .nz-cristal layer uses it)")
    if "!important" in css and not re.search(r"nz-(visually-hidden|vh|print-hide)", html):
        fallos.append("!important in page CSS (only the hiding helpers carry it)")

    # 4 · hand-written colours inside the page's own CSS
    hand = _COLOR_RE.findall(css)
    if hand:
        fallos.append(f"{len(hand)} hand-written colour(s) in <style>: use var(--nz-*)")

    # 5 · emojis in UI, outside the attribution
    visible = _text_only(html).replace(_FOOTER, " ")
    emojis = _EMOJI_RE.findall(visible)
    if emojis:
        sample = "".join(sorted(set(emojis))[:6])
        fallos.append(f"emoji in the UI ({sample}): use an SVG icon from the sprite")

    # 6 · attribution footer
    if _FOOTER not in html:
        fallos.append(f"missing the exact footer: «{_FOOTER}»")

    # 7 · structure
    if len(re.findall(r"<h1\b", html, re.I)) > 1:
        fallos.append("more than one <h1>: one heading per page")
    if not re.search(r'<html[^>]*lang\s*=\s*"', html, re.I):
        avisos.append('missing lang on <html>')
    if not re.search(r'<html[^>]*data-nz-theme\s*=\s*"(light|dark)"', html, re.I):
        avisos.append('missing data-nz-theme="light|dark" on <html>')
    if not re.search(r'<body[^>]*class\s*=\s*"[^"]*\bnz\b', html, re.I):
        avisos.append('missing class="nz" on <body>')
    if re.search(r"@media[^{]*max-width", css) and "max-width: 639px" not in css:
        avisos.append("@media (max-width): Aurora is mobile-first (base + min-width)")

    return json.dumps({
        "ok": not fallos,
        "system": census["sistema"],
        "version": census["version"],
        "failures": fallos,
        "warnings": avisos,
        "measured": {
            "nz_classes": len(used),
            "families": len({known[c]["familia"] for c in used if c in known}),
            "linked_packs": sorted(p.split("/")[-1] for p in packs),
        },
        "next": (
            "Fix the failures and validate again. Warnings are read, they do not block."
            if fallos else "No failures. Now measure the render in a browser (mobile 320/360/390)."
        ),
    }, ensure_ascii=False)
