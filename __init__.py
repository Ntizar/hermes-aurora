"""Aurora design system — Hermes plugin.

Ships four read-only skills plus two offline tools:

    skills/aurora ............. core doctrine: resolve version, link, rules, census
    skills/aurora-pages ....... page archetypes and layout / typography recipes
    skills/aurora-validate .... audit a generated page (lint + browser measurement)
    skills/aurora-generative .. openui-lang: let a model compose Aurora markup

    aurora_search(need) ....... query the bundled census, get the real markup of an object
    aurora_validate(path|html). validate a page against the census, offline

Both tools read ``data/censo.json``, a generated snapshot of the design system's
``components.json``. No network, no subprocess, no writes: the plugin only answers.
"""

from __future__ import annotations

from pathlib import Path

from .tools.aurora import (
    AURORA_SEARCH_SCHEMA,
    AURORA_VALIDATE_SCHEMA,
    aurora_search,
    aurora_validate,
)

_HERE = Path(__file__).resolve().parent
_SKILLS_ROOT = _HERE / "skills"

TOOLSET = "aurora"

# name -> (description, frontmatter extras)
SKILLS = {
    "aurora": (
        "Use when building or editing any web UI with Aurora (Ntizar). Resolve the "
        "live version from the repo first, then compose with census objects only.",
        {
            "version": "1.1.0",
            "license": "MIT",
            "tags": ["design-system", "css", "frontend", "aurora", "tokens"],
        },
    ),
    "aurora-pages": (
        "Use when choosing the shape of an Aurora page: archetypes, layout, "
        "desktop canvas, mobile stacking and typographic scale.",
        {
            "version": "1.1.0",
            "license": "MIT",
            "tags": ["design-system", "css", "layout", "responsive", "aurora"],
        },
    ),
    "aurora-validate": (
        "Use before delivering any Aurora page: run the validator and measure the "
        "render instead of trusting the markup.",
        {
            "version": "1.1.0",
            "license": "MIT",
            "tags": ["design-system", "css", "qa", "audit", "aurora"],
        },
    ),
    "aurora-generative": (
        "Use when a model must generate Aurora UI at runtime: openui-lang prompt, "
        "spec, runtime and static baking.",
        {
            "version": "1.1.0",
            "license": "MIT",
            "tags": ["design-system", "css", "openui", "generative", "aurora"],
        },
    ),
}


def register(ctx) -> None:
    """Register the bundled skills and the two tools. Nothing else is registered."""
    for name, (description, frontmatter) in SKILLS.items():
        path = _SKILLS_ROOT / name / "SKILL.md"
        if not path.is_file():
            # A packaging mistake must be loud, not a silently missing skill.
            raise FileNotFoundError(f"aurora-design-system: missing skill file {path}")
        ctx.register_skill(
            name=name,
            path=path,
            description=description,
            frontmatter=frontmatter,
        )

    ctx.register_tool(
        "aurora_search",
        TOOLSET,
        AURORA_SEARCH_SCHEMA,
        aurora_search,
        description=AURORA_SEARCH_SCHEMA["description"],
    )
    ctx.register_tool(
        "aurora_validate",
        TOOLSET,
        AURORA_VALIDATE_SCHEMA,
        aurora_validate,
        description=AURORA_VALIDATE_SCHEMA["description"],
    )
