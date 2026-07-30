---
created: 2026-07-30T11:44:16+00:00
modified: 2026-07-30T11:50:29+00:00
permalink: llmeon/fitfile-home-separation-data-implementation
tags: [architecture, code-review, data-vs-implementation, fitfile, linus-torvalds]
title: Fitfile Home — Separation of Data and Implementation
type: note
---

## Fitfile Home—Separation of Data and Implementation

> _"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."_—Linus Torvalds

Date: 2026-07-30
Repo: `fitfile-home` at `/Volumes/DAL/Fitfile/gitlab/fitfile-home`
Context: Developer environment bootstrapper and CLI spanning macOS/WSL, cloud tools, runtime managers, and a complex ticket-context workflow.

---

### What Gets It Right—Explicitly Naming Data

#### `config/images.yaml`—the Star of the Show

```yaml
images:
  - key: fitconnect
    context: InsightFILE
    dockerfile: Dockerfile.service
    image_name: fitconnect
    helm_values_key: fitconnectService
    recommended: true
    build_args:
      - GIT_AUTH_TOKEN
    arch_build_args:
      arm64:
        - ARCH=arm64
```

This is exactly what Torvalds means. Every Docker image the team builds is declared as a record with typed fields. The build script reads this data—it doesn't know what images exist or where their Dockerfiles live. The relationship between an image and its Dockerfile, between an image and its Helm values key, between a package and its architecture-specific build args—all named in data. Adding a new image is a YAML entry, not a code change.

#### `repos/repos.txt`

```
git@gitlab.com:fitfile/data-and-analytics.git|data-and-analytics|development
```

URL → workspace-relative path → branch. Three columns, one relationship per line. `clone-repos.sh` is a loop with zero hardcoded project names.

#### Package Manifests

`packages/Brewfile` and `packages/apt-packages.txt`—the package manifest as data. The OS install scripts each read their corresponding file. The OS-branching `if` in bootstrap is acceptable conditional logic; the _what_ to install is pure data.

#### `vscode-extensions.txt`

Flat list of extension IDs consumed by `install-vscode-extensions.sh`. The extension data lives outside the installer.

#### `dotfiles/.fitfile.env.example`

The schema for runtime secrets. Every env var the system needs, documented with _where to get it_. This is the closest thing to a type system the bash world gets.

---

### Where Data Bleeds Into Code

#### 1. `dotfiles/shared.sh`—The Orville Problem

This file is the most entangled. Three distinct roles in one file:

| Role | Content | Classification |
|---|---|---|
| PATH configuration | `~/.tfenv/bin`, `~/.krew/bin`, `/opt/homebrew/opt/libpq/bin`, pyenv shims, nvm, `$FITFILE_HOME/scripts` | Data |
| Tool initialisation | `eval "$(pyenv init -)"`, `source "$NVM_DIR/nvm.sh"`, `source "$ZSH/oh-my-zsh.sh"` | Implementation |
| Aliases | `ll=ls -lah`, `gs=git status`, `gp=git pull` | Data |
| Env var loading | `source ~/.fitfile.env` | Implementation |

The nested if/then for `JAVA_HOME` (macOS vs Linux) is a decision tree embedded in what should be a config file. The tool-init calls are side effects triggered at shell startup, not data declarations.

Torvalds would argue: all three concerns should be separated into a config file (paths, aliases, env var names) and an init script (the actual `source`/eval calls) that reads that config.

#### 2. Hardcoded Hosts Entries in `setup-hosts.sh`

```bash
ENTRIES=(
  "127.0.0.1  dev-postgresql"
  "127.0.0.1  dev-minio"
)
```

IP-to-hostname mappings baked into code. If a developer needs a different mapping, or if the local cluster moves, the script must be edited. A `config/hosts.yaml` would make this data-driven—and the script would be a generic "read file and write to /etc/hosts" utility.

#### 3. Scattered Env Var Declarations across Scripts

Each forwarding script defines its own fallback strategy:

```bash
# aws-forward.sh
INSTANCE_ID="${BASTION_INSTANCE_ID:-${EKS_BASTION_INSTANCE_ID:-}}"

# eks-forward.sh
INSTANCE_ID="${EKS_BASTION_INSTANCE_ID:-}"
```

The relationship "aws-forward falls back to EKS_BASTION_INSTANCE_ID if BASTION_INSTANCE_ID is unset" is an implicit data relationship expressed in bash fallback syntax. There is no single source of truth for all env vars the system consumes—you have to grep every script to find what is available. The `~/.fitfile.env` schema only covers three services (GitLab, ACR, Auth0, SpiceDB, Atlassian); the AWS and bastion vars are undocumented in the schema.

#### 4. `arch_build_args` In images.yaml—conditional Logic Sneaking into Data

```yaml
arch_build_args:
  arm64:
    - ARCH=arm64
```

Borderline: it encodes "on arm64 hosts, add ARCH=arm64 to build args" as a data structure. In a pure data model this would be expressed as platform-specific build args at the CI/CD level or as a compiler target in the Dockerfile. Defensible—bash has no enum type—but it is implementation-dependent conditionality leaking into data.

#### 5. `install/common.sh` Mixes Data Input with Tool Install

The script installs Oh My Zsh, nvm, krew plugins—and then prompts for git name/email:

```bash
if [[ -z "$(git config --global user.name 2>/dev/null)" ]]; then
  read -rp "Git full name: " git_name
  git config --global user.name "$git_name"
fi
```

Runtime data collection embedded in a script whose primary purpose is package installation. The git config values are data about the developer—should be declared in either `~/.fitfile.env` or `dotfiles/gitconfig`.

---

### The Relationship Map

| Relationship | Where it is named | Type |
|---|---|---|
| Image → Dockerfile → Helm values key | `config/images.yaml` | Data |
| Repo → workspace path → branch | `repos/repos.txt` | Data |
| Env var name → where to get its value | `dotfiles/.fitfile.env.example` | Data |
| Package name → OS platform | `Brewfile` vs `apt-packages.txt` | Data (by existence) |
| VS Code extension → team recommended | `vscode-extensions.txt` | Data |
| Bastion host → local tunnel port | Hardcoded in `aws-forward.sh` / `eks-forward.sh` | Code |
| Hostname → IP for local cluster | Hardcoded array in `setup-hosts.sh` | Code |
| Forwarding env vars → their defaults | Fallback operators scattered across scripts | Code |
| Shell init → PATH → tool binaries | Mixed in `dotfiles/shared.sh` | Code/Data blend |

---

### Verdict: B+

The `images.yaml` and `repos.txt` patterns prove the author gets the principle. Those files are the repo's best work—adding a new image or repo requires zero code changes. That is the Torvalds test passed.

Three sharp edges for a chezmoi-oriented developer:

1. Move the hardcoded arrays (`setup-hosts.sh` entries, port numbers in `pf.sh`) into config files—`config/hosts.yaml`, `config/ports.yaml`. These are data about your local cluster, not logic.
2. Decouple `shared.sh` into three files—a config (paths, aliases, env var names), an init (the actual `source`/eval calls), and a team defaults file that chezmoi can overlay. Right now one file does all three in one shot.
3. Document all env vars in a single schema—either extend `.fitfile.env.example` to include `EKS_BASTION_INSTANCE_ID`, `AWS_REGION`, `FORWARD_HOST`, `FORWARD_LOCAL_PORT`, or create a `config/env.yaml` that lists every env var, its purpose, and whether it has a default or is developer-supplied. A developer should be able to read one file and know every knob they can turn—not grep 15 scripts.
