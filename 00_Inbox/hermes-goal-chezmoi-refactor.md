---
created: 2026-05-29T15:13:02+00:00
date: 2026-05-29
modified: 2026-05-29T15:13:38+00:00
source: derived from 2026-05-29-chezmoi-dotfiles-audit.md
tags: [2, chezmoi, goal, hermes, refactor]
title: hermes-goal-chezmoi-refactor
---

## Hermes `/goal`—Chezmoi Dotfiles Refactor

A standing goal for Hermes to clear the audit findings autonomously, tier by tier, with commits as rollback points and explicit completion criteria for the judge model.

### How to Run it

1. In Hermes, run `/stop` first (a new goal can't be set while a goal is live).
2. Paste the single block below (from `/goal` to the end of the fenced block).
3. The default turn budget is 20—this scope fits, but if Hermes pauses on budget,
   `/goal resume`. Use `/goal status` to check, `/goal pause` to checkpoint.
4. Prefer the infra profile (this is infrastructure work).

> The "Decisions flagged for me" come back in Hermes' final summary—you don't need to
> answer anything mid-run. The agent takes the conservative, non-destructive path on each
> and tells you what it assumed.

---

### The Goal (copy This block)

```
/goal Refactor my chezmoi dotfiles repo at ~/.local/share/chezmoi to clear the findings in the 2026-05-29 audit. Work autonomously on the `development` branch only.

CONTEXT
The repo is healthy. This is debt-paydown plus ONE data-loss risk: the live skill at ~/.hermes_custom_skills/custom/mcp-integration/SKILL.md (v3.0.0) is NOT tracked in chezmoi source, so a future `chezmoi apply` would delete it. SOUL.md calls skill_view("custom/mcp-integration") 5x. Fixing that is Step 0, before anything else.

GUARDRAILS (do not violate)
- Branch `development` only. Never touch `main`. Do not push.
- Do NOT run `chezmoi apply` at any point this run. Use `chezmoi diff` for verification only. Editing the source tree is enough; applying is the only thing that could clobber the untracked skill.
- Never `rm -rf` tracked content. Use `git mv` for renames and `.chezmoiignore` for removals.
- After any CUE edit, regenerate generated.json and confirm the diff shows ONLY the intended change.
- Commit after each tier with a clear conventional-commit message. These are my rollback points.
- If any verification step fails, STOP, report exactly what failed, and do not proceed to the next tier.
- British English in any new comments or docs.
- The correct CUE command needs explicit file args (vet does NOT auto-discover profiles.yaml):
  cue export ./cue/main.cue ./cue/packages.yaml ./cue/profiles.yaml .chezmoidata.toml --out json --force -t os=darwin -t hostname=FF-M07W9K7YN7 -t is_work=true -t is_headless=false -t home_dir=/Users/leon.ormes

STEP 0 — Protect the at-risk skill (CRITICAL, do first)
1. Confirm the runtime skill exists: ls ~/.hermes_custom_skills/custom/mcp-integration/SKILL.md
2. Copy the whole runtime dir into source: cp -R ~/.hermes_custom_skills/custom/mcp-integration/ dot_hermes_custom_skills/custom/mcp-integration/
3. Remove the empty placeholder dir dot_hermes_custom_skills/custom/mcp-proxy/ — consolidate onto mcp-integration, which is what SOUL.md actually references.
4. Verify: ls dot_hermes_custom_skills/custom/mcp-integration/SKILL.md must exist.
5. Commit: "fix(skills): track mcp-integration skill v3.0.0 in source (was untracked, lost on apply)"

TIER A — Safe mechanical
A1. cue/packages.yaml: resolve the `sentence-transformers` orphan. DEFAULT ACTION: add a stub registry entry so inventory resolution stops failing (non-destructive). Do NOT remove it from inventory. Flag in the final summary that I should confirm whether it should actually install.
A2. cue/packages.yaml: deduplicate `cue` and `slack` — remove both from inventory.work, keep them in inventory.common.
A3. cue/packages.yaml: remove the empty `inventory.personal: []` key.
A4. Regenerate generated.json with the export command above (> .chezmoidata/generated.json) and confirm the diff is only the intended A1-A3 delta.
A5. Fix the run-script prefix collision (three scripts share 01-). Rename via `git mv`:
    run_onchange_01-brew-bundle.sh.tmpl              -> keep as 01-
    run_onchange_01-install-packages-linux.sh.tmpl   -> 02-
    run_onchange_01-install-curl-packages-linux.sh.tmpl -> 03-
    run_onchange_02-bootstrap-mise.sh.tmpl           -> 04-
A6. Guard the two Linux-only scripts: wrap the ENTIRE body of the (now) 02- and 03- scripts in {{- if eq .chezmoi.os "linux" -}} ... {{- end -}}.
A7. dot_config/zellij/config.kdl.tmpl lines 295-296: delete the two commented-out hardcoded /Users/leon.ormes lines.
VERIFY TIER A: run the orphan check, the duplicate check, and `cue export` (must exit 0). Commit: "refactor(cue,scripts): clear Tier A audit findings — dedupe inventory, fix run-script ordering, guard linux scripts"

TIER B — Medium value
B1. Already done in Step 0.
B2. Retire WezTerm (Ghostty is the active terminal): add dot_wezterm.lua and dot_config/wezterm/ to .chezmoiignore, remove `wezterm` from the CUE inventory AND registry, and scrub any residual wezterm cross-references in dot_config/ghostty/. Flag for my confirmation that WezTerm is truly retired. Commit separately: "chore(term): retire vestigial WezTerm config"
B3. goal_judge model mismatch — private_config.yaml line 224 uses openrouter/owl-alpha, but SOUL.md + MEMORY.md say gemini-3-flash. DEFAULT ACTION: update the DOCS (SOUL.md, MEMORY.md) to reflect owl-alpha, preserving current runtime behaviour. Do NOT change the live routing. Flag that if I intended gemini-3-flash for cost, that's a separate change. Commit: "docs(hermes): align goal_judge docs with actual owl-alpha routing"

OUT OF SCOPE THIS RUN — record as a durable checklist (a BACKLOG.md in the repo root, or my task system) but DO NOT execute:
- Prune the 14 orphan registry entries.
- Move qmk_firmware/ to its own repo.
- Move dot_config/images/ (84 MB of wallpapers) out of the repo.
- Add a Makefile/justfile and document the CUE export command.
- (Optional cost tweak) route approval/title_generation to a cheaper model such as gemini-3-flash.

COMPLETION CRITERIA — you are DONE only when ALL of these are true. State each one explicitly, with its result, in your final message:
- dot_hermes_custom_skills/custom/mcp-integration/SKILL.md exists and is committed.
- `cue export ...` (the command above) exits 0.
- Orphan check passes: every inventory item resolves to a registry entry.
- Duplicate check passes: no inventory item appears more than once.
- `chezmoi diff` shows only the intended changes — nothing unexpected.
- Each tier is its own commit on `development`; nothing pushed to main; `chezmoi apply` was never run; no `rm -rf` of tracked content.
- The five backlog items are filed somewhere durable, not executed.
- A short closing summary lists: the commits you made, and the three decisions flagged for me (sentence-transformers install-or-not, WezTerm truly-retired, goal_judge owl-vs-gemini).
```

---

### Why This Ordering (the principle)

The audit tiers by risk of the change. I've re-tiered by risk of inaction:

- Step 0 is the only irreversible risk. Every Tier A item is cosmetic—a bad rename
  is trivially reverted. But the untracked `mcp-integration` skill is the one artefact a
  stray `chezmoi apply` deletes with no copy in source. You protect the irreplaceable thing
  first, then tidy the cheap stuff. Doing it as its own commit also means that even if the
  rest of the run goes sideways, the data-loss hole is already closed.
- No `chezmoi apply` this run. A common reflex is "apply to test it". Don't—applying is
  the exact operation that's dangerous until Step 0 lands, and you don't need it: you're
  editing the _source_, and `chezmoi diff` shows you the effect without writing anything.
- `generated.json` must be regenerated, not just diffed. The audit's check 2 diffs it
  against a fresh export. After legitimate CUE edits that check _should_ fail until you
  regenerate—so the goal regenerates it and confirms the delta is only what you intended.
- Judgement calls are pre-decided conservatively, not left to the agent. In goal mode
  there's no human in the loop mid-run, so an undecided "register or remove?" becomes a coin
  flip. Each one defaults to the non-destructive choice (add a stub, update docs, ignore not
  delete) and is surfaced for your sign-off afterwards.

---

### Optional: Run it in Three Stages instead

The judge model gives you a clean "done" per goal, and smaller goals are easier to review

(and each is a discrete win). If you'd rather stage it, run `/stop` between each:

Stage 1—the critical fix only (≈2 min, biggest payoff):

```
/goal On the `development` branch of ~/.local/share/chezmoi, track the untracked mcp-integration skill in source. The live skill ~/.hermes_custom_skills/custom/mcp-integration/SKILL.md (v3.0.0) is NOT in chezmoi source and a `chezmoi apply` would delete it. Copy the whole runtime dir to dot_hermes_custom_skills/custom/mcp-integration/, remove the empty placeholder dot_hermes_custom_skills/custom/mcp-proxy/, verify dot_hermes_custom_skills/custom/mcp-integration/SKILL.md exists, and commit as "fix(skills): track mcp-integration skill v3.0.0 in source". Do NOT run `chezmoi apply`. Do not push. Done when the file is committed on `development`.
```

Stage 2—Tier A mechanical (same GUARDRAILS, STEP 0 already done): paste the main

block but delete Step 0 and Tier B.

Stage 3—Tier B (same GUARDRAILS): paste the main block but delete Step 0 and Tier A.
