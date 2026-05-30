---
tags: [chezmoi, audit, dotfiles, refactor]
source: OWL (Mechanical Lead, local audit)
date: 2026-05-29
---

# Chezmoi Dotfiles Audit Report

**Repository:** `~/.local/share/chezmoi` (branch: `development`)
**Date:** 2026-05-29
**Scope:** Full structural audit — data pipeline, run scripts, templates, Hermes config, verification.
**Constraint:** Read-only. No changes applied.

---

## 1. Executive Summary

The dotfiles repository is well-architected with a clean CUE-data-driven pipeline and sensible chezmoi conventions. The `generated.json` is in sync with the CUE source, and no hardcoded hostnames or paths leak into templates. The three critical findings are: (1) `sentence-transformers` is listed in `inventory.common` but has **no registry entry**, which will cause silent resolution failures in any template that iterates inventory; (2) two packages (`cue`, `slack`) are **duplicated** across `common` and `work` inventories; (3) the `dot_hermes_custom_skills/custom/mcp-proxy/` directory is an **empty directory** in chezmoi source, yet the runtime `~/.hermes_custom_skops/custom/mcp-integration/SKILL.md` (v3.0.0) is not tracked — this skill would be lost on a fresh `chezmoi apply`. Additionally, four Linux-only `run_*` scripts execute on every macOS apply (harmless but noisy), and `dot_wezterm.lua` (119 lines) is vestigial since Ghostty is the active terminal. Overall health: **good**, with mechanical cleanups recommended.

---

## 2. Findings Table

| # | Category | Finding | Severity | File(s) | Suggested Fix |
|---|----------|---------|----------|---------|---------------|
| 1 | Data Pipeline | `sentence-transformers` in `inventory.common` but **absent from registry** | HIGH | `cue/packages.yaml` | Add a registry entry or remove from inventory. Currently causes nil-resolution in `resolved_packages` loop. |
| 2 | Data Pipeline | `cue` and `slack` duplicated in both `common` and `work` inventories | LOW | `cue/packages.yaml` | Deduplicate; `_inventory_set` in main.cue masks this at runtime but it's a maintenance hazard. |
| 3 | Data Pipeline | `inventory.personal` is an empty list `[]` | LOW | `cue/packages.yaml` | Either populate or remove the key to avoid confusion. |
| 4 | Skills | `dot_hermes_custom_skills/custom/mcp-proxy/` is an **empty directory**; runtime `mcp-integration/SKILL.md` is untracked | **CRITICAL** | `dot_hermes_custom_skills/custom/mcp-proxy/` | Move or copy the runtime `~/.hermes_custom_skills/custom/mcp-integration/` skill into the chezmoi source tree so it survives `chezmoi apply`. |
| 5 | Skills | SOUL.md references `skill_view("custom/mcp-integration")` 5× but no `mcp-proxy` SKILL.md exists in chezmoi source | HIGH | `private_dot_hermes/SOUL.md`, `dot_hermes_custom_skills/` | Same as #4 — the skill body must be tracked in source. |
| 6 | Scripts | Three `run_onchange_01-*` scripts share prefix `01-` — execution order is undefined | MEDIUM | `run_onchange_01-brew-bundle.sh.tmpl`, `run_onchange_01-install-packages-linux.sh.tmpl`, `run_onchange_01-install-curl-packages-linux.sh.tmpl` | Rename to `01-`, `02-`, `03-` to guarantee order. |
| 7 | Scripts | Two Linux-only scripts (`run_onchange_01-install-packages-linux.sh.tmpl`, `run_onchange_01-install-curl-packages-linux.sh.tmpl`) run on macOS (guarded by template but still processed) | LOW |同上 | Add `{{- if eq .chezmoi.os "linux" -}}` guards at the top level, or move to `.chezmoiinclude`/`.chezmoiignore` conditionally. |
| 8 | Templates | `dot_wezterm.lua` (119 lines) is vestigial — Ghostty is the active terminal | LOW | `dot_wezterm.lua`, `dot_config/wezterm/` | Either remove or add to `.chezmoiignore` if WezTerm is no longer used. Still in CUE inventory (`work`) and registry. |
| 9 | Templates | Hardcoded `/Users/leon.ormes` in `dot_config/zellij/config.kdl.tmpl` (lines 295-296) — even though commented out | LOW | `dot_config/zellij/config.kdl.tmpl` | Replace with `{{ .chezmoi.homeDir }}` or remove the commented lines. |
| 10 | Config | `goal_judge` uses `openrouter/owl-alpha` — SOUL.md and MEMORY.md reference `gemini-3-flash` as the intended lightweight judge | MEDIUM | `private_dot_hermes/private_config.yaml:224` | Align with intended routing: either update config to `google/gemini-3-flash` or update documentation to reflect owl-alpha as intentional. |
| 11 | Config | All `auxiliary` tasks route to `openrouter/owl-alpha` — no lightweight/cost-sensitive auxiliary model configured | LOW | `private_dot_hermes/private_config.yaml:139-210` | Consider routing `approval`, `title_generation`, `profile_describer` to a cheaper/faster model (e.g. `google/gemini-3-flash`). |
| 12 | Config | `delegation.model` set to `anthropic/claude-sonnet-4-6` via OpenRouter — verify this is intentional and the model exists | LOW | `private_dot_hermes/private_config.yaml:301` | Confirm OpenRouter model name; may need `openrouter/anthropic/claude-sonnet-4-6`. |
| 13 | Repo Hygiene | `dot_config/images/` — 31 files, 84 MB of wallpapers tracked in dotfiles repo | MEDIUM | `dot_config/images/` | Move to external storage or `.gitignore`; 84 MB inflates clone and diff. |
| 14 | Repo Hygiene | `qmk_firmware/` directory in repo root is unconventional for a dotfiles repo | LOW | `qmk_firmware/` | Either move to a dedicated repo or add to `.chezmoiignore` if managed elsewhere. |
| 15 | Verification | Check 1.4 (Node resolution) uses `which node` — on a fresh mise install, node may not exist yet, causing a false FAIL on first run | LOW | `verify_state.sh:56-65` | Add a "not installed" vs "shadowed" distinction; or skip if `mise ls node` shows it's configured but not installed. |
| 16 | CUE | `cue vet` fails with "undefined field: work_mac" and "undefined field: features" — this is because `cue vet` doesn't auto-discover `profiles.yaml` as a data file; only `cue export` with explicit file args works | LOW | `cue/main.cue:128,149-158` | Document the correct vet command: `cue vet ./cue/main.cue ./cue/packages.yaml ./cue/profiles.yaml .chezmoidata.toml -t ...` |
| 17 | Registry drift | 14 registry entries exist but are never used by any inventory (e.g. `ast-grep-mcp`, `chromadb`, `copyq`, `dust`, `fastfetch`, `kitty`, `libomp`, `mactop`, `mcp-hub`, `mdns-scanner`, `ruamel-yaml`, `surgeon`, `tree`, `cleaner-one-pro`, `cloudhop`) | LOW | `cue/packages.yaml` | Prune unused registry entries or add to an inventory group. |

---

## 3. Refactor Plan

### Tier A — Safe, mechanical (do now)

1. **Add `sentence-transformers` to registry** — add a stub entry in `cue/packages.yaml` under `packages.registry` with at least a `common` or `darwin` target (even if it's a no-op manager). Or remove from `inventory.common` if not actually needed.
2. **Deduplicate inventory entries** — remove `cue` and `slack` from `inventory.work` (keep in `common` since they're shared).
3. **Fix run-script prefixes** — rename:
   - `run_onchange_01-brew-bundle.sh.tmpl` → keep as `01-`
   - `run_onchange_01-install-packages-linux.sh.tmpl` → `02-`
   - `run_onchange_01-install-curl-packages-linux.sh.tmpl` → `03-`
   - `run_onchange_02-bootstrap-mise.sh.tmpl` → `04-`
4. **Guard Linux scripts** — wrap entire body of `run_onchange_01-install-packages-linux.sh.tmpl` and `run_onchange_01-install-curl-packages-linux.sh.tmpl` in `{{- if eq .chezmoi.os "linux" -}}...{{- end -}}`.
5. **Remove commented hardcoded paths** in `dot_config/zellij/config.kdl.tmpl` lines 295-296, or replace with template variables.
6. **Prune `inventory.personal`** if unused — remove the empty `[]` from `cue/packages.yaml` to avoid confusion.

### Tier B — Medium risk, high value (do this sprint)

1. **Backfill `mcp-integration` skill into chezmoi source** — copy the runtime `~/.hermes_custom_skills/custom/mcp-integration/` directory into `dot_hermes_custom_skills/custom/mcp-integration/` (note: rename from `mcp-proxy` to `mcp-integration`, or consolidate). This is the single most impactful fix.
2. **Remove or ignore WezTerm config** — if Ghostty is the sole terminal, move `dot_wezterm.lua` and `dot_config/wezterm/` to `.chezmoiignore`, remove `wezterm` from CUE inventory, and clean up `dot_config/ghostty/` to remove any residual cross-references.
3. **Migrate `dot_config/images/` out of the repo** — move wallpapers to external storage (e.g. `~/Pictures/` or `~/.dotfiles-assets/`), add to `.gitignore`, and optionally link via a run script.
4. **Align `goal_judge` model** — decide: either change `private_config.yaml` `goal_judge.model` to `google/gemini-3-flash`, or update SOUL.md/MEMORY.md to reflect owl-alpha as the intentional choice.
5. **Route lightweight auxiliary tasks to a cheaper model** — change `approval`, `title_generation` to `google/gemini-3-flash` for cost savings.

### Tier C — Architectural (backlog)

1. **Consolidate unused registry entries** — audit the 14 orphan registry packages; either add to inventories or remove.
2. **Move `qmk_firmware/` to a dedicated repo** — QMK configs belong in their own repository, not in dotfiles.
3. **Document the CUE export command** — the correct command requires explicit file args. Add a comment at the top of `main.cue` or in a `Makefile`:
   ```bash
   cue export ./cue/main.cue ./cue/packages.yaml ./cue/profiles.yaml .chezmoidata.toml --out json --force -t os=darwin -t ...
   ```
4. **Add a `Makefile` or `justfile`** for common operations: `cue export`, `chezmoi apply`, `brew bundle`, `verify_state.sh`.

---

## 4. Verification Checklist

After applying Tier A/B changes, run these commands to confirm nothing broke:

```bash
# 1. CUE export still works
cd ~/.local/share/chezmoi
cue export ./cue/main.cue ./cue/packages.yaml ./cue/profiles.yaml .chezmoidata.toml \
  --out json --force \
  -t os=darwin -t hostname=FF-M07W9K7YN7 -t is_work=true -t is_headless=false \
  -t home_dir=/Users/leon.ormes > /tmp/cue_fresh.json 2>&1
echo "Exit: $?"

# 2. generated.json is still in sort
diff <(jq -S . .chezmoidata/generated.json) <(jq -S . /tmp/cue_fresh.json)

# 3. No inventory orphans remain
python3 -c "
import yaml
with open('cue/packages.yaml') as f: d = yaml.safe_load(f)
reg = set(d['packages']['registry'].keys())
for g in ['common','work','personal']:
    for item in d['packages'].get('inventory',{}).get(g,[]):
        assert item in reg, f'Orphan: {item} in {g}'
print('All inventory items have registry entries.')
"

# 4. No duplicate inventory entries
python3 -c "
import yaml
from collections import Counter
with open('cue/packages.yaml') as f: d = yaml.safe_load(f)
items = []
for g in ['common','work','personal']:
    items.extend(d['packages'].get('inventory',{}).get(g,[]))
for item, cnt in Counter(items).items():
    if cnt > 1: print(f'DUPLICATE: {item} x{cnt}')
print('Duplicate check complete.')
"

# 5. Verify script is syntactically valid
bash -n ~/.local/share/chezmoi/run_after_99-verify.sh.tmpl 2>&1 || echo "TMPL not directly bash-parsable (expected)"

# 6. Run the verification script
bash ~/.local/share/chezmoi/verify_state.sh

# 7. Dry-run chezmoi apply
chezmoi diff

# 8. Confirm mcp-integration skill is tracked
ls ~/.local/share/chezmoi/dot_hermes_custom_skills/custom/mcp-integration/SKILL.md 2>/dev/null \
  && echo "TRACKED" || echo "MISSING — fix required"
```

---

*Report compiled by OWL (Mechanical Lead). Read-only audit. No files modified.*
