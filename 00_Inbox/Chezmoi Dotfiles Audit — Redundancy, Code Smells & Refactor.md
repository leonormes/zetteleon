*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday May 29, 2026 - 1:21 PM*
---
I now have substantial evidence across multiple pages. Both tools still say `fetchMore`, but the candidates are now looping — `search_memory` is returning the same events (the corpus is saturated at 500 candidates). `ask_memory` has given me 30/139 unique events with fresh signal. I have enough grounded evidence to synthesise the prompt. Here is the deliverable:

---

## Hermes Prompt: Chezmoi Dotfiles Audit — Redundancy, Code Smells & Refactor

### What your LTM tells us about the repo (evidence base)

**Repo location:** `~/.local/share/chezmoi` on branch `development`

**Confirmed top-level structure (from multiple LTM snapshots):**

```
.chezmoidata/          # generated.json lives here — CUE output, consumed by templates
.chezmoitemplates/     # manager_for.tmpl, inventory.tmpl, and others
.claude/ .gemini/      # AI agent context directories
cue/                   # main.cue, packages.yaml, schema/, bootstrap.cue, gen_install.cue
cue.mod/               # CUE module definition
Docs/                  # Architecture.md, WARP.md, PROJECT_BRAIN.md, project_journal.md, AGENTS.md
dot_claude/            # Claude Code context
dot_config/            # atuin, broot, btop, fastfetch, gh, ghostty, git, glab-cli,
                       # images, k9s, kitty, lazygit, mcphub, mise, nvim, 1Password, zellij
dot_cursor/            # Cursor agent config
dot_gemini/            # Gemini CLI config (antigravity/mcp_config.json)
dot_hammerspoon/       # Hammerflow.spoon, RecursiveBinder.spoon, init.lua, apps.txt
dot_local/             # ~/.local/bin/ binaries
private_dot_hermes/    # private_config.yaml, SOUL.md, skills/, memories/, assets/, profiles/
private_Library/       # Application Support, LaunchAgents, Preferences, espanso
qmk_firmware/          # QMK keyboard firmware
scripts/               # helper scripts
graphify-out/          # graph visualisation output (code smell: committed artefact)

# Root-level files
.chezmoi.toml.tmpl     # bootstrap entrypoint — determines profile, is_work, hostname
.chezmoidata.toml      # static data (env, mcp_servers, zsh config)
.chezmoiignore.tmpl    # templated ignore file
.gitleaks.toml         # secret scanning (recently added after commit was blocked)
.markdownlint.json
dot_Brewfile.tmpl      # generated from CUE inventory
dot_editorconfig
dot_gitconfig.tmpl
dot_gitignore_global
dot_ideavimrc
dot_wezterm.lua        # WezTerm config (may be vestigial — Ghostty is primary terminal)
dot_zprofile / dot_zshenv
install.sh
mise.toml              # mise tool version pinning
obsidian-vault-optimisation-plan.md  # code smell: stray planning doc in repo root
README.md / CLAUDE.md
run_after_99-verify.sh.tmpl
run_before_00-bootstrap.sh.tmpl
run_onchange_01-brew-bundle.sh.tmpl
run_onchange_01-install-packages-linux.sh.tmpl  # Linux-only — possible dead weight on macOS
run_onchange_01-install-curl-packages-linux.sh.tmpl
run_onchange_02-bootstrap-mise.sh.tmpl
run_onchange_restart_mcp_hub.sh.tmpl
run_onchange_rust_components.sh.tmpl
run_onchange_uv_tools.sh.tmpl
run_onchange_yazi-plugins.sh.tmpl
ssm-session-manager-policy.json  # code smell: AWS IAM policy committed to dotfiles root
test_bootstrap.sh / test_calibre_mcp.py  # test files in root
verify_state.sh / verify_casks.py  # verification scripts
stylua.toml
```

**Known pain points & code smells from LTM:**

- `inventory.personal: []` was an empty list — identified as a smell (Apr 4 refactor session)
- `sentence-transformers` in `inventory.common` had no registry entry — caused CUE export failures
- `cue` was duplicated in `inventory.work` and `inventory.common`
- `zsh.dynamic_completions` indirection — flagged as "delete or implement"
- `_inventory_check` CUE validation was insufficiently hardened
- `antigravity-cli` in Brewfile caused `brew bundle cleanup` failures (topgrade breakage, May 28)
- `mcpproxy` `"disabled"` field in template was being ignored because `ServerConfig` has no `disabled` field — mcpproxy tried all servers regardless
- `lua-language-server` reference in a config.json template was broken (not installed)
- Tree-sitter was disabled in `.chezmoidata.toml` despite being referenced
- `graphify-out/` directory with generated graph HTML committed to the repo
- `obsidian-vault-optimisation-plan.md` and planning docs in repo root
- `ssm-session-manager-policy.json` (an AWS IAM JSON) committed to the dotfiles root
- `dot_wezterm.lua` potentially vestigial (switched to Ghostty)
- `verify_state.sh` uses `mapfile` which breaks on macOS zsh (bash-only builtin)
- `dot_config/images/` directory containing wallpaper images tracked in dotfiles
- Multiple `run_onchange_01-*` scripts with the same prefix numeral (execution order ambiguity)

---

## The Hermes Prompt

Copy this verbatim into your Hermes session (or paste into Antigravity/any agent that has terminal and file tools):

---

```markdown
## HERMES DOTFILES AUDIT

**Repository:** `~/.local/share/chezmoi` (branch: `development`)
**Objective:** Produce a structured audit report covering redundancy, code smells,
and a prioritised refactor plan. Do NOT apply any changes — audit and report only.

---

### PHASE 0 — Tool discovery and repo orientation

1. Use your terminal tool to confirm current branch:
   `cd ~/.local/share/chezmoi && git status --short && git branch --show-current`
2. List all root-level files and first-level directories:
   `ls -la ~/.local/share/chezmoi && find ~/.local/share/chezmoi -maxdepth 2 -type d | sort`
3. Enumerate all `run_*` scripts:
   `find ~/.local/share/chezmoi -maxdepth 1 -name 'run_*' | sort`
4. Summarise what you find before proceeding. State your chosen tools for:
   - File content reading
   - Structural / pattern search (prefer `ast-grep` or `grep -r`)
   - Template rendering: `chezmoi execute-template`

---

### PHASE 1 — Data pipeline integrity

The pipeline is:  
`.chezmoidata.toml` + `cue/packages.yaml` → `cue/main.cue` (CUE export) →  
`.chezmoidata/generated.json` → Go templates (.tmpl files) → applied config files

Audit the following:

1. **CUE schema completeness:** Read `cue/packages.yaml`. For every package in
   `inventory.common`, `inventory.work`, and `inventory.personal`, verify it has
   a corresponding entry in `packages.registry`. Report any inventory items with
   no registry entry (these cause silent CUE export failures).

2. **Duplicate inventory entries:** Check for packages listed in more than one
   inventory group. Report them.

3. **Empty or stub groups:** Check if `inventory.personal` is an empty list `[]`.
   Report all empty groups.

4. **`generated.json` staleness:** Run:
   ```bash
   cd ~/.local/share/chezmoi
   cue export ./cue/main.cue --out json --force \
     -t os='darwin' -t hostname='FF-M07W9K7YN7' \
     -t is_work=true -t is_headless=false \
     > /tmp/cue_fresh.json 2>&1
   diff .chezmoidata/generated.json /tmp/cue_fresh.json | head -40
   ```
   Report whether `generated.json` is up to date.

5. **Template–data contract:** Read `dot_Brewfile.tmpl` and `dot_config/mise/mise.toml`
   (or equivalent). Identify any hardcoded values that should be CUE-derived
   (e.g. hardcoded paths, package names, version strings).

---

### PHASE 2 — Run-script audit

Read each `run_*` script in the repo root. For each one, report:

| Script | Trigger | Purpose | Issues found |
|--------|---------|---------|-------------|
| `run_before_00-bootstrap.sh.tmpl` | every apply | bootstrap Homebrew, CUE, mise | ? |
| `run_onchange_01-brew-bundle.sh.tmpl` | Brewfile hash change | brew bundle install | ? |
| `run_onchange_01-install-packages-linux.sh.tmpl` | Linux only? | apt/flatpak installs | ? |
| `run_onchange_01-install-curl-packages-linux.sh.tmpl` | Linux only? | curl installs | ? |
| `run_onchange_02-bootstrap-mise.sh.tmpl` | mise config change | mise install | ? |
| `run_onchange_restart_mcp_hub.sh.tmpl` | mcp config change | restart mcphub | ? |
| `run_onchange_rust_components.sh.tmpl` | ? | cargo installs | ? |
| `run_onchange_uv_tools.sh.tmpl` | ? | uv tool installs | ? |
| `run_onchange_yazi-plugins.sh.tmpl` | ? | yazi plugin install | ? |
| `run_after_99-verify.sh.tmpl` | every apply | system state verification | ? |

Flag these specific smells:
- **Prefix collision:** Multiple scripts share the `01-` prefix — document execution order.
- **`mapfile` usage:** `grep -n 'mapfile' verify_state.sh` — this breaks on macOS zsh.
- **Dead Linux scripts:** If this machine is macOS-only, flag Linux scripts as candidates
  for `.chezmoiignore` conditions.
- **Idempotency failures:** Any script that does not check before installing.

---

### PHASE 3 — Template and config smell detection

1. **Hardcoded hostnames / paths in templates:**
   ```bash
   grep -rn 'FF-M07W9K7YN7\|/Users/leon.ormes\|_PLACEHOLDER_' \
     ~/.local/share/chezmoi --include='*.tmpl' --include='*.cue'
   ```
   Report every hit. Paths should route through `resolved.*` fields in `main.cue`.

2. **`mcpproxy` `disabled` field smell:**
   Read `dot_config/mcphub/config.json.tmpl` (or `dot_config/mcpproxy/mcp_proxy.json.tmpl`).
   Check if it emits a `"disabled": true` field. Cross-reference whether the deployed
   `mcpproxy` binary actually honours this field. If not, the template produces dead config.

3. **Stray non-dotfile content in repo root:**
   List everything in repo root that is NOT a standard chezmoi file:
   ```bash
   ls ~/.local/share/chezmoi | grep -vE \
     '^(dot_|run_|\.chezmoi|cue|Docs|scripts|mise\.toml|README|CLAUDE|\.git|\.gitleaks|\.markdownlint|\.gitignore|\.gitattributes|install\.sh)'
   ```
   Likely candidates: `graphify-out/`, `obsidian-vault-optimisation-plan.md`,
   `ssm-session-manager-policy.json`, `test_bootstrap.sh`, `test_calibre_mcp.py`,
   `verify_casks.py`, `verify_state.sh`, `stylua.toml`.

4. **Images tracked in dotfiles:**
   ```bash
   find ~/.local/share/chezmoi/dot_config/images -type f | wc -l
   du -sh ~/.local/share/chezmoi/dot_config/images
   ```
   Wallpaper images in a dotfiles repo inflate clone time and diff noise.

5. **Vestigial WezTerm config:**
   Check if `dot_wezterm.lua` is still referenced anywhere or if Ghostty is the
   sole terminal. If Ghostty is primary, flag for removal or `.chezmoiignore`.

---

### PHASE 4 — private_dot_hermes audit

The Hermes agent config lives at `private_dot_hermes/`. Audit:

1. Read `private_dot_hermes/private_config.yaml`. Identify:
   - Any model references that no longer exist or are deprecated.
   - Any settings duplicated between `private_config.yaml` and `SOUL.md`.
   - Whether `auxiliary` task routing is consistent (should route lightweight tasks
     to `google/gemini-3-flash` per recent optimisation, May 18).

2. List `private_dot_hermes/skills/` — identify skills that are:
   - Empty or stub files.
   - Duplicated in purpose.
   - Referenced in `SOUL.md` but not present on disk (or vice versa).

3. Check `private_dot_hermes/memories/` — flag any large or stale memory files
   that could be pruned.

---

### PHASE 5 — Verification integrity

Read `run_after_99-verify.sh.tmpl` and `verify_state.sh`. Report:

1. What the verification protocol actually checks (list each CHECK/PASS/WARN).
2. Any checks that always pass vacuously (e.g. the `mapfile` bug means orphan ZSH
   check silently succeeds on macOS).
3. Whether the Brewfile drift warning correctly triggers `chezmoi apply` + 
   `brew bundle install --global` guidance.

---

### OUTPUT FORMAT (strict)

Produce a structured markdown report with these top-level sections:

## 1. Executive Summary
One paragraph: overall health, biggest risks, recommended priority.

## 2. Findings Table
| # | Category | Finding | Severity | File(s) | Suggested Fix |
|---|----------|---------|----------|---------|---------------|
(Severity: CRITICAL / HIGH / MEDIUM / LOW)

## 3. Refactor Plan

### Tier A — Safe, mechanical (do now)
- Concrete, one-liner changes.

### Tier B — Medium risk, high value (do this sprint)  
- Structural changes requiring careful testing.

### Tier C — Architectural (backlog)
- Design-level decisions.

## 4. Verification Checklist
Commands you can run after applying Tier A/B changes to confirm nothing broke.

---

**Constraints:**
- Use British English throughout (analyse, optimise, colour, recognise).
- Read before you patch — never guess file contents.
- Do NOT apply changes. This is an audit run only.
- Commit nothing. If you find something alarming, note it in the findings table.
- After each Phase, emit a brief "Phase N complete — [N] findings" before proceeding.
```

---

### Context notes