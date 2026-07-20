---
created: 2026-05-21T13:12:28+00:00
modified: 2026-07-20T16:33:05+00:00
permalink: llmeon/raw/2026-05-21-pieces-zsh-edit-command-line-response
pieces_ids: [5c936938-42de-45e9-9566-df1888aa2567]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-21-pieces-zsh-edit-command-line-response
---

## Asset 1 (Pieces: 5c936938-42de-45e9-9566-df1888aa2567)—13:12:28

I have everything I need. Here's the full picture and the Hermes prompt.

---

## Opening a Zsh Command in Vim to Edit It: `vared` + `edit-command-line`

The native zsh mechanism is `edit-command-line`—a ZLE widget that opens the current command buffer in your `$VISUAL` / `$EDITOR`. You bind it to a key, and pressing it mid-command fires up vim (or nvim) with the full command, saves, and drops you back at the prompt ready to execute.

### How it Works

```zsh
autoload -Uz edit-command-line
zle -N edit-command-line
bindkey '^X^E' edit-command-line   # Ctrl-X Ctrl-E, same as bash
# Or if you use zsh-vi-mode (you do), bind to 'v' in NORMAL mode:
bindkey -M vicmd 'v' edit-command-line
```

After pressing the key, your command opens in the editor defined by `$VISUAL` (or `$EDITOR`). Since your `v` alias points to `nvim`, you want to make sure the env var is set correctly—`VISUAL=nvim` or `VISUAL=vim`.

> Note: You already have `jeffreytse/zsh-vi-mode` loaded via Zinit with `ZVM_INIT_MODE=sourcing`. `zsh-vi-mode` overrides ZLE keymaps after initialisation, so the binding must be registered in `zvm_after_init_commands` or the `ZVM_AFTER_INIT` hook—otherwise `zvm` will clobber it.

---

## Hermes Prompt

Paste this into a new Hermes session with your chezmoi repo as the working directory:

```text
You are operating inside my chezmoi-managed dotfiles repository at ~/.local/share/chezmoi.

## Task
Add `edit-command-line` support to my zsh config so I can press a key to open the current command buffer in nvim.

## Constraints
- The feature must be registered AFTER zsh-vi-mode initialises, using `zvm_after_init_commands` (or equivalent ZVM hook), so zsh-vi-mode doesn't clobber the binding.
- Bind `edit-command-line` to `v` in vicmd mode (matching zsh-vi-mode's normal-mode keymap).
- Also bind `^X^E` in viins mode as a fallback for muscle memory / when in insert mode.
- `VISUAL` must be set to `nvim` if not already set. Check `dot_config/zsh/modules/00-preflight.zsh.tmpl` or `05-runtime.zsh` and add `export VISUAL="${VISUAL:-nvim}"` there if missing.
- Do NOT add new files. The correct home for ZLE widget configuration is `dot_config/zsh/modules/10-core.zsh`. Add the `autoload` + `zle -N` + binding registration there.
- After making changes, run `chezmoi apply` and verify with: `zsh -c 'source ~/.config/zsh/.zshrc; zle -la | grep edit-command-line'`

## Files to read first
- `dot_config/zsh/modules/10-core.zsh` — add the widget registration here
- `dot_config/zsh/terminal/plugins.zsh.tmpl` (or the rendered `plugins.zsh`) — verify zsh-vi-mode is present and confirm which ZVM hook to use
- `dot_config/zsh/modules/00-preflight.zsh.tmpl` or `05-runtime.zsh` — check for VISUAL/EDITOR exports

## Expected result
After `chezmoi apply` and `exec zsh`, pressing `Esc` then `v` on any buffered command opens it in nvim. Editing and saving drops the modified command back to the prompt. Pressing `Ctrl-X Ctrl-E` in insert mode does the same.

## Apply and verify
Run `chezmoi apply` then test with:
```zsh
exec zsh
# Type a long command, press Esc, press v — should open nvim
```

If `zsh-vi-mode` overrides the binding (symptom: pressing `v` doesn't open nvim), add the binding inside a `zvm_after_init_commands` block in `10-core.zsh`:

```zsh
zvm_after_init_commands+=(
  'autoload -Uz edit-command-line; zle -N edit-command-line; bindkey -M vicmd v edit-command-line; bindkey "^X^E" edit-command-line'
)
```

---

### What the Change to `10-core.zsh` Should Look like

For reference, the block Hermes will add looks like this:

```zsh
# Open current command buffer in $VISUAL (nvim).
# Must register AFTER zsh-vi-mode init or it gets clobbered.
autoload -Uz edit-command-line
zle -N edit-command-line

# zsh-vi-mode hook — fires after ZVM overwrites ZLE keymaps
zvm_after_init_commands+=(
    'bindkey -M vicmd v edit-command-line'
    'bindkey "^X^E" edit-command-line'
)
```

And in whichever preflight/runtime module you export `EDITOR`:

```zsh
export VISUAL="${VISUAL:-nvim}"
export EDITOR="${EDITOR:-nvim}"
```

After `chezmoi apply` + `exec zsh`, pressing `Esc` → `v` on any buffered command opens it in nvim, exactly as you'd expect from vi-mode muscle memory.
