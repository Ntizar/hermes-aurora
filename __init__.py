"""Aurora design system — skills-only Hermes plugin.

The plugin ships four read-only skills under ``skills/`` and registers each one
with the host, so they resolve as ``aurora-design-system:<name>`` from
``skill_view()`` / ``skills_list()``:

    aurora ............. core doctrine: resolve version, link, rules, census
    aurora-pages ....... page archetypes and layout / typography recipes
    aurora-validate .... audit a generated page (lint + browser measurement)
    aurora-generative .. openui-lang: let a model compose Aurora markup

Nothing here executes at import time: no tools, no hooks, no network, no files
written. ``register()`` only tells the host where the SKILL.md files live, which
is why this plugin is safe to enable in any profile.
"""

from __future__ import annotations

from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILLS_ROOT = _HERE / "skills"

# name -> (description, frontmatter extras)
SKILLS = {
    "aurora": (
        "Use when building or editing any web UI with Aurora (Ntizar). Resolve the "
        "live version from the repo first, then compose with census objects only.",
        {
            "version": "1.0.0",
            "license": "MIT",
            "tags": ["design-system", "css", "frontend", "aurora", "tokens"],
        },
    ),
    "aurora-pages": (
        "Use when choosing the shape of an Aurora page: archetypes, layout, "
        "desktop canvas, mobile stacking and typographic scale.",
        {
            "version": "1.0.0",
            "license": "MIT",
            "tags": ["design-system", "css", "layout", "responsive", "aurora"],
        },
    ),
    "aurora-validate": (
        "Use before delivering any Aurora page: run the repo auditor and measure "
        "the render instead of trusting the markup.",
        {
            "version": "1.0.0",
            "license": "MIT",
            "tags": ["design-system", "css", "qa", "audit", "aurora"],
        },
    ),
    "aurora-generative": (
        "Use when a model must generate Aurora UI at runtime: openui-lang prompt, "
        "spec, runtime and static baking.",
        {
            "version": "1.0.0",
            "license": "MIT",
            "tags": ["design-system", "css", "openui", "generative", "aurora"],
        },
    ),
}


def register(ctx) -> None:
    """Register the bundled skills. Nothing else is registered on purpose."""
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
