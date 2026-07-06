---
auditor: Claude (Fable 5)
created: 2026-07-02T12:55:43+00:00
date: 2026-07-02
modified: 2026-07-04T10:49:23+00:00
permalink: llmeon/security/chezmoi-cli-security-audit-2026-07-02
repo: git@github.com:leonormes/chezmoi.git (private)
scope: ~/.local/share/chezmoi dotfiles, CLI environment
tags: [audit, chezmoi, cli, dotfiles, security]
title: Chezmoi CLI Security Audit 2026-07-02
---

## Chezmoi CLI Security Audit—2026-07-02

Read-only audit of the chezmoi source tree (`~/.local/share/chezmoi`),

focused on the CLI environment: secrets handling, shell init, bootstrap

scripts, MCP configuration, service accounts, and permission surfaces.

### Summary

The current working tree is clean—no live secrets are present in any

tracked file today. Secret injection is done properly: 1Password `op://`

references resolved just-in-time via `op run`, a service-account token held

in Keychain, and `secrets_filter`/`redact_secrets` enabled downstream.

The material problem is historical: `gitleaks` finds 51 genuine

secret exposures across 28 commits in git history (plus 416 false

positives from `Brewfile.lock.json` hashes and a docs example). Because the

repo is private the blast radius is limited, but several of these are

real, long-lived credentials that were committed in plaintext and remain

recoverable from history until rotated and purged.

| Severity | Count | Theme |
|----------|-------|-------|
| 🔴 High | 3 | Live secrets in git history (rotate + purge) |
| 🟠 Medium | 4 | Service-account & MCP trust surface |
| 🟡 Low | 5 | Hardening / hygiene |

---

### 🔴 High Severity

#### H1—51 Real Secrets in Git History across 28 Commits

`gitleaks git --config.gitleaks.toml` reports 467 findings. Filtering the

false positives (415 Telegram-token matches in `Brewfile.lock.json` SHA

hashes, 1 in `yazi_docs.md`) leaves 51 genuine leaks:

| Type | Count | Notable files (historical) |
|------|-------|----------------------------|
| generic-api-key | 28 | `dot_gemini/settings.json`, `dot_codeium/windsurf/mcp_config.json`, `.chezmoidata.toml`, `dot_config/mcphub/config.json.tmpl`, `private_dot_hermes/private_dot_env` |
| gitlab-pat | 10 | `zshenv/work.sh`, `zshenv/base.sh`, `dot_config/zsh/dot_zshenv`, `dot_config/glab-cli/private_config.yml` |
| google-api-key | 4 | `dot_config/zsh/dot_zshenv` + `.bak.20250922_*` copies |
| gcp-api-key | 4 | same as above |
| atlassian-api-token | 2 | `dot_gemini/settings.json`, `private_dot_hermes/private_dot_env` |
| github-oauth | 2 | `dot_config/gh/hosts.yml` |
| anthropic-api-key | 1 | `dot_config/zsh/dot_zshenv` |

Exposure spans 2024-03-29 → 2026-06-10. The most recent leaks:

- `2026-06-10`—Atlassian API token in `private_dot_hermes/private_dot_env`
- `2026-05-22`—generic key in `private_dot_hermes/private_dot_env`
- `2026-01-17`—GitLab PAT in `dot_config/glab-cli/private_config.yml`
- `2026-01-16`—generic key in `.chezmoidata.toml`
- `2026-01-12`—keys in `mcphub/config.json.tmpl`, `gemini/antigravity/mcp_config.json`

Impact: Anyone with clone access (now or historically—collaborators,

forks, CI, machine backups, a compromised laptop) can recover these. The

GitLab PATs, Atlassian token, GCP/Google API keys and the Anthropic key are

the highest value.

Fix: rotate every credential type listed, then purge history. See the

remediation plan below.

#### H2—Anthropic + GCP + GitLab Credentials Committed in Plaintext `dot_zshenv`

The pre-2025 shell env (`dot_config/zsh/dot_zshenv` and the

`dot_zshenv.bak.20250922_*` snapshots) held an Anthropic API key, GCP/Google

API keys and a GitLab PAT inline. These were later migrated to the current

`op://` model—good—but the plaintext values remain in history and the

`.bak` snapshot files were themselves committed. These specific keys should

be treated as compromised and rotated regardless of purge.

#### H3—`private_dot_hermes/private_dot_env` Leaked an Atlassian Token as Recently as 2026-06-10

This is the newest leak and sits in the Hermes agent env file. The live

`~/.hermes/.env` on disk is correctly `-rw-------` (600) and is git-ignored

now, but the committed history entry means the token that was live in June

2026 is exposed. Rotate the Atlassian API token.

---

### 🟠 Medium Severity

#### M1—1Password Service-account Token in Keychain Grants Broad Vault Access

`~/.config/1mcp/run-1mcp.sh` pulls `OP_SERVICE_ACCOUNT_TOKEN` from Keychain

(`security find-generic-password`) and runs `op run` against `secrets.env`.

This is a sound pattern (token never on disk in plaintext, never in git),

but a service-account token is a standing bearer credential: any process

running as your user can read it from Keychain without prompting, and it can

read every `op://` reference the account is scoped to (`ff`, `Leon`,

`Private` vaults observed). Confirm the service account is scoped to only the

vaults/items 1MCP needs, and rotate it on a schedule.

#### M2—1MCP Listens Unauthenticated on 127.0.0.1:3050

The gateway runs with `authEnabled: false` (confirmed via `/health`) and

binds loopback only—so not network-reachable, which is the right default.

But any local process or browser tab (via DNS-rebinding-style requests

to `127.0.0.1:3050`) can call every MCP tool: Jira/Confluence write,

Obsidian vault read/write, memory, filesystem-adjacent tools. On a

single-user Mac this is acceptable; be aware that "no auth on loopback" means

the trust boundary is "anything running as you."

#### M3—Antigravity/Gemini MCP Config Sets `"trust": true`

`dot_gemini/config/mcp_config.json` marks the 1mcp server as `trust: true`,

which typically disables per-tool confirmation prompts. Combined with M2,

an agent (or prompt-injected agent) can invoke destructive MCP tools without

a human gate. Consider leaving trust off for write-capable servers.

#### M4—Bootstrap Scripts Pipe Remote Installers to a Shell

`run_before_00-bootstrap.sh.tmpl` runs the Homebrew installer via

`bash -c "$(curl -fsSL …)"` and downloads `https://mise.run`. The Linux

curl-package installer (`run_onchange_03-*`) does the same for arbitrary

`id` URLs from `packages.yaml`. There is a light guard (`head -1 | grep

'^#!'`) but no checksum or signature pinning—a compromised upstream or

MITM (for any non-TLS-pinned host) executes as you. This is standard

dotfiles practice, but it is the highest-trust step in the whole pipeline.

---

### 🟡 Low Severity / Hygiene

- L1—`~/.config/1mcp/secrets.env` is `0644`. It contains only `op://`
  references (no secrets), so this is low risk, but `0600` is tidier and
  matches `~/.hermes/.env` (correctly 600) and `~/.config/gh/hosts.yml` (600).
- L2—`.bak` env snapshots were committed. The 2025-09-22 timestamped
  backups of `dot_zshenv` are the kind of file that should never be tracked;
  add `*.bak` / `*.bak.*` to `.chezmoiignore` and `.gitignore`.
- L3—`dot_claude/settings.json` pins `"model": "sonnet"` and runs
  several `shale capture` / `zellij-claude-status` hooks on every tool call.
  Not a vulnerability, but every hook is code that runs automatically—keep
  the list auditable.
- L4—`.claude/settings.local.json` allow-list is very broad. It
  includes `Bash(curl:*)`, `Bash(brew *)`, `Bash(op read *)`,
  `Bash(chezmoi destroy *)`, `Bash(cp:*)`, `Bash(xargs cat *)` and wildcard
  `Bash(…)`. These auto-approve powerful commands without a prompt. Prune to
  what you actually rely on; `curl:*` + `op read *` together are enough to
  exfiltrate a resolved secret with no confirmation.
- L5—Pre-commit gitleaks hook is local-only. `.git/hooks/pre-commit`
  runs gitleaks and is good, but it is not enforced in CI and can be bypassed
  with `--no-verify`. The hook also isn't itself managed by chezmoi, so a
  fresh clone starts with no protection until manually installed.

---

### What is Already Good

- Current working tree has zero live secrets (verified with `gitleaks dir`).
- Just-in-time secret injection via `op run` + Keychain service account.
- `op:core` zsh module centralises secret access; no secrets cached to disk.
- `secrets_filter = true` (atuin), `redact_secrets: true` (hermes).
- Custom `.gitleaks.toml` with sensible placeholder allow-listing.
- MCP gateway bound to loopback only; most optional servers `disabled`.
- Repo is private on GitHub.
- Sensitive live files (`~/.hermes/.env`, `gh/hosts.yml`) are `0600`.

---

### Remediation Plan

See companion note: [[Chezmoi Security Remediation Plan 2026-07-02]]
