# Catalog submission

Entry ready at [`aurora-design-system.yaml`](aurora-design-system.yaml). It is pinned to a full
commit SHA and the plugin validates green at that pin.

```bash
hermes plugins validate ~/.hermes/plugins/aurora-design-system --install-deps   # Validation passed
```

## Local checks already run

| Check | Result |
|---|---|
| `hermes plugins validate` (manifest, loadable, capabilities, security scan) | passed |
| `hermes plugins doctor` | import + registration OK |
| Install from the public repo (community source, scanner on) | installed, `caution` cleared by fixing the demo pages |

## Opening the PR (one file)

1. Fork `NousResearch/hermes-agent` and create a branch.
2. Add `plugin-catalog/aurora-design-system.yaml` (this file, unchanged).
3. PR title: `catalog: add aurora-design-system`.
4. PR body:

> Adds `aurora-design-system`, a skills-only plugin (four SKILL.md files) that teaches an agent
> to build UI with the Aurora CSS design system. `register()` calls `ctx.register_skill()` four
> times and nothing else.
>
> **Surfaces used:** plugin skill registration only. No tools, hooks, middleware, providers,
> system-prompt sections, desktop `plugin.js`, dashboard routes, env vars or Python dependencies.
>
> **Disclosures (rule 13):** the plugin performs no network calls, reads no files outside its own
> directory and starts no processes. Its skills instruct the agent to fetch the design system's
> public documentation (`cdn.jsdelivr.net/gh/Ntizar/Aurora@master/LLM.md` and `components.json`)
> the way a person would, and to link the design system from jsDelivr in the pages it builds;
> that traffic happens in the agent's own tools, not inside the plugin. Three demo pages under
> `demo/` are static HTML with no JavaScript. Screenshots: `docs/screenshots/*.png`.
>
> `hermes plugins validate --install-deps` passes at the pinned SHA.

## After merge

- The entry renders at `/docs/plugins/` and installs by name: `hermes plugins install aurora-design-system`.
- Future releases: SHA-bump PR (new pin + `version`). Never a self-updater.
