---
title: Maintenance Run 2026-09-25
type: note
permalink: llmeon/maintenance/maintenance-run-2026-09-25
tags:
- maintenance
- chezmoi
- topgrade
- brew
---

Maintenance run completed 2026-09-25 (08:43-09:00).

**chezmoi apply**: ✅ SYSTEM CONVERGED (exit 0). 82 mise tools, uv tools, needle catalogue regenerated.

**topgrade**: ⚠️ Exit 1 (brew cask transient failure + containers expected). 9 formulas + 13 casks upgraded. Hermes v0.21.3→v0.21.5+2144. agy v1.2.10→v1.2.11. ~1.33GB freed.

**Fault filed**: GitHub #13 — brew 6.0.0+ tap trust reset during upgrade. 8 formula taps + 1 cask tap needed re-trust. Brewfile now satisfied.