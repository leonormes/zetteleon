---
tags:
- hermes
- solution
- fitfile
- refactoring
source: hermes (deepseek/deepseek-v4-flash)
date: 2026-07-30
permalink: llmeon/wiki/2026-07-30-fitfile-home-data-implementation-separation
---

# Data/Implementation Separation Plan — fitfile-home

**Context:** The `fitfile-home` repo is the central developer environment bootstrap for Fitfile. New devs follow `GETTING_STARTED.md` → `bootstrap.sh` to get set up. The repo mixed declarative data (package lists, host entries, tool manifests, env var specs) with shell implementation (scripts that install, validate, forward ports). A new dev had to grep through shell scripts to discover what would be installed.

**Approach:** Extract all hardcoded data into YAML config files under `config/`, make scripts read them via `yq`. Replace `install/ubuntu-tools.sh` (17 individual tool install blocks × 50 lines each) with a single generic `install/tools.sh` that reads `config/tools.yaml` and dispatches to one of 6 install strategies.

**What changed (planned):**

| Pattern | Before | After |
|---------|--------|-------|
| Host entries | Hardcoded array in `scripts/setup-hosts.sh` | `config/hosts.yaml` |
| Required env vars | Hardcoded array in `scripts/validate-env.sh` | `config/required-env.yaml` |
| Tool manifest | 17 individual curl/gh-release blocks in `install/ubuntu-tools.sh` | `config/tools.yaml` + generic `install/tools.sh` |
| Krew plugins | Hardcoded array in `install/common.sh` | `config/krew-plugins.yaml` |
| Runtimes | Hardcoded in `scripts/setup-versions.sh` | `config/runtimes.yaml` |
| Port forwards | Hardcoded in `scripts/commands/pf.sh` + `stop_pf.sh` | `config/port-forward.yaml` |
| Local-dev constants | Hardcoded in `start-local-dev.sh` | `config/local-dev.yaml` |
| Customer sites | Hardcoded in `create-release.sh` | `config/customer-sites.yaml` |
| API endpoints | Hardcoded in `create-release.sh` + `fitfile-context.sh` | `config/release.yaml` |

**File count:** 9 new config files, 1 new generic script (`install/tools.sh`), 10 modified scripts, 1 deleted (`install/ubuntu-tools.sh`).

**Key pattern:** `config/tools.yaml` uses an `install_via` strategy system (`curl_binary`, `gh_latest_release`, `script`, `git_clone`, `apt_repo`, `curl_zip`). Adding a tool = 5-line YAML entry + possibly a new strategy case. No more 50-line copy-paste blocks per tool.

**Why yq:** Already installed via Brewfile and ubuntu-tools.sh before any config-reading script runs. No new dependency.

**Risks:** `yq` API compatibility, install strategy pattern being too opinionated, mongodb pod name in port-forward config being unstable (it's `dev-mongodb-b17ef-0` — a pod, not a service).