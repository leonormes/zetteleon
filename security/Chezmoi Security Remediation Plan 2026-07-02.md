---
created: 2026-07-02 13:05:14+00:00
date: 2026-07-02
modified: 2026-07-20 16:32:34+00:00
permalink: llmeon/security/chezmoi-security-remediation-plan-2026-07-02
source: Chezmoi CLI Security Audit 2026-07-02
tags:
- chezmoi
- plan
- remediation
- security
title: Chezmoi Security Remediation Plan 2026-07-02
type: note
---

## Chezmoi Security Remediation Plan—2026-07-02

Companion to [[Chezmoi CLI Security Audit 2026-07-02]]. Ordered by priority.

Rotation comes before history purge—purging without rotating leaves the

already-exposed credential valid.

---

### Phase 0—Rotate Exposed Credentials (Do fIrst, tOday)

These were in git history in plaintext; assume compromised. Rotate at the

provider, not just in the vault.

- [ ] GitLab PATs—revoke all tokens in GitLab → Settings → Access
      Tokens; issue new ones; update the `op://ff/…` items they back.
      (Leaked in `zshenv/*.sh`, `dot_zshenv`, `glab-cli/private_config.yml`.)
- [ ] Atlassian / Jira API token—revoke at
      id.atlassian.com → Security → API tokens; reissue; update
      `op://ff/JIRA_API_TOKEN`. (Leaked 2026-06-10, most recent.)
- [ ] Anthropic API key—rotate in the Anthropic console; update vault.
- [ ] Google / GCP API keys—regenerate in Google Cloud console; the
      old `AIza…` keys in history are recoverable.
- [ ] GitHub OAuth token in `gh/hosts.yml` history—run
      `gh auth refresh` / re-login to invalidate the old token.
- [ ] Any generic keys in `gemini/settings.json`,
      `codeium/windsurf/mcp_config.json`, `mcphub/config.json.tmpl`,
      `private_dot_hermes/private_dot_env`—identify the providers and rotate.

> Tip: `gitleaks git --config.gitleaks.toml --redact -v` prints file + commit
> for each finding so you can trace which provider each key belongs to
> (redacted, so no plaintext is shown).

### Phase 1—Stop the Bleeding (Config, fAst)

- [ ] Add to `.chezmoiignore.tmpl` and `.gitignore`:
      `*.bak`, `*.bak.*`, `/*.env` (except `*.env.tmpl`), `private_dot_env`.
- [ ] `chmod 600 ~/.config/1mcp/secrets.env` and set the source file mode via
      chezmoi attributes (rename to `private_secrets.env` so chezmoi applies
      `0600`). _(fixes L1)_
- [ ] Prune `.claude/settings.local.json` allow-list: remove the wildcard
      `Bash(…)`, and tighten `Bash(curl:*)`, `Bash(cp:*)`,
      `Bash(op read *)`, `Bash(chezmoi destroy *)` to specific forms you use.
      _(fixes L4)_
- [ ] Reconsider `"trust": true` in `dot_gemini/config/mcp_config.json` for
      write-capable MCP servers. _(fixes M3)_

### Phase 2—Purge Git History

Only after Phase 0 rotation is confirmed. This rewrites history—force-push

required, and any other clones must be re-cloned.

- [ ] Back up the repo first: `git clone --mirror …/chezmoi-backup.git`.
- [ ] Install `git-filter-repo` (`brew install git-filter-repo`).
- [ ] Build a paths/regex file of the leaked files and purge, e.g.:

  ```bash
  git filter-repo \
    --path zshenv/ \
    --path dot_config/zsh/dot_zshenv.bak.20250922_163218 \
    --path dot_config/zsh/dot_zshenv.bak.20250922_163617 \
    --path dot_config/zsh/dot_zshenv.bak.20250922_164106 \
    --path private_dot_hermes/private_dot_env \
    --path dot_config/glab-cli/private_config.yml \
    --path dot_gemini/settings.json \
    --path dot_codeium/windsurf/mcp_config.json \
    --invert-paths
  ```

  For secrets that lived in files you want to _keep_, use

  `--replace-text replacements.txt` with the redacted patterns instead.

- [ ] Re-run `gitleaks git` until it reports 0 real findings.
- [ ] `git push --force-with-lease origin development` (and any other branches).
- [ ] Re-clone on every machine; delete the old working copies.

### Phase 3—Prevent Recurrence

- [ ] Make the pre-commit hook part of the managed config so a fresh clone is
      protected: ship it via chezmoi and set `core.hooksPath`, or adopt
      `pre-commit` framework with a `.pre-commit-config.yaml` running gitleaks.
      _(fixes L5)_
- [ ] Add a CI check (GitHub Actions) that runs `gitleaks` on push/PR so a
      `--no-verify` bypass is still caught server-side.
- [ ] Scope-audit the 1Password service account: confirm it only has
      read access to the specific items 1MCP needs (Obsidian, Jira,
      OpenAI), not whole vaults; set a rotation reminder. _(addresses M1)_
- [ ] Add checksum/pin verification to the bootstrap installers, or at
      minimum document the trust assumption in the script header. _(addresses M4)_
- [ ] Optional: enable 1MCP auth (token/header) even on loopback if you run
      untrusted local processes or browser-based agents. _(addresses M2)_

### Verification Checklist

- [ ] `gitleaks dir --config.gitleaks.toml` → 0 real findings (already true).
- [ ] `gitleaks git --config.gitleaks.toml` → 0 real findings (after Phase 2).
- [ ] All Phase 0 credentials confirmed rotated at provider side.
- [ ] `ls -l ~/.config/1mcp/secrets.env` → `-rw-------`.
- [ ] Fresh clone runs the gitleaks hook without manual setup.