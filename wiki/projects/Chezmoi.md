---
title: Chezmoi
wiki_type: dossier
entity_kind: project
created: 2026-05-18T13:40:46.636193+00:00
modified: 2026-05-29T15:33:41+00:00
tags: [wiki, dossier, project]
sources: ["raw/2026-05-18-pieces-cuh-rbac-permissions.md", "raw/2026-05-18-pieces-worker-status-reflections.md", "raw/2026-05-18-pieces-hermes-gitlab-research.md", "raw/2026-05-18-pieces-brain-mcp-integration.md", "raw/2026-05-18-pieces-hermes-diagnostic-session.md", "raw/2026-05-18-pieces-llm-mcp-chezmoi-config.md", "raw/2026-05-29-pieces-chezmoi-audit.md"]
---

## Summary

Dotfile management using chezmoi for version-controlled configuration across systems with source directory at ~/.local/share/chezmoi/.

Last audited 2026-05-29: full structural audit completed with 17 findings. Overall health: good, with mechanical cleanups recommended.

## Key Facts

> "## brain-mcp Integration — Current Status

**Confirmed: there is no `__NODE__` placeholder in your chezmoi repo.** The filesystem search across the entire chezmoi source tree returned zero results. Th..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "Let me search the filesystem to check if `__NODE__` placeholder exists in the chezmoi repository...." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "Both pagination passes returned `sufficient` / no new material changing the ledger. The second cursor still has a `fetchMore` but the candidates are all repeats from the same backlog refinement meetin..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "**Reflection 4 · on track** — Comprehensive STATUS report delivered — pagination loops still technically open but worker assessed as sufficient

**Insights:** 5/6 checklist items covered. The STATUS r..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "Now I have a complete picture. Here is the current status:

---

## brain-mcp Integration — Current Status

### What has been confirmed from your filesystem and memory

**`.chezmoidata.toml` confirmed..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "**Reflection 3 · on track** — Good STATUS report delivered but two search_memory streams still have fetchMore pending

**Insights:** 4/6 checklist items addressed. The worker produced a solid, well-st..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "**Reflection 2 · on track** — search_memory needs pagination; filesystem_search_paths needs a real path

**Insights:** 1/6 items started. search_memory returned fetchMore — worker must paginate before..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "The user has shared a summary from Hermes about the brain-mcp integration status. The evaluator feedback says I should be doing a STATUS investigation, not generating prompts. Let me search memory for..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]


- **2026-05-29**: Full structural audit of the chezmoi dotfiles repo completed — 17 findings identified: (1) `sentence-transformers` in `inventory.common` has no registry entry (HIGH — causes nil-resolution); (2) `cue` and `slack` duplicated across `common` and `work` inventories (LOW); (3) `dot_hermes_custom_skills/custom/mcp-proxy/` is empty in chezmoi source but runtime `mcp-integration/SKILL.md` is not tracked; (4) four Linux-only `run_*` scripts execute on macOS (harmless but noisy); (5) `dot_wezterm.lua` (119 lines) is vestigial since Ghostty is active — [[raw/2026-05-29-pieces-chezmoi-audit.md]] (Pieces: cf86f34c-82cc-426e-b81b-331d70267dfc)

- **2026-05-29**: A Hermes `/goal` prompt was generated from the audit findings — "CHEZMOI DOTFILES — RESILIENCE & SIMPLICITY REFACTOR" covering Phase 1: data pipeline integrity fixes (CUE/packages.yaml), atomic write approach, and staged refactor — [[raw/2026-05-29-pieces-chezmoi-audit.md]] (Pieces: fa883503-057b-4ce2-a645-f7b59eed7e55)

- **Summary updated 2026-05-29**: The dotfiles repo remains well-architected with CUE-data-driven pipeline. Overall health: good, with mechanical cleanups recommended.



## Connections

- [[Hermes-Agent]] — Agent orchestration framework that captures activity to Pieces LTM
- [[General]] — Catch-all project for uncategorised work

## Timeline

- **2026-05-18** — Project page created from Pieces LTM ingests
- **2026-05-29** — Full structural audit completed (17 findings); `/goal` prompt generated for staged refactor

## Contradictions

None identified.

## Open Questions

- What is the long-term scope and ownership of this workstream?
- Should this be merged with an existing project or remain separate?
